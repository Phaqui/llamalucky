import sys
import os
import asyncio
from typing import Optional
import datetime
from urllib.parse import urlparse
from collections import defaultdict

from pydantic import BaseModel, conlist
from fastapi import FastAPI, Header, Request
from fastapi.middleware.cors import CORSMiddleware
import sqlalchemy
from sqlalchemy.sql import text
from sqlalchemy.sql.expression import insert
import databases
from scipy.stats import chi2_contingency

DATABASE_URL = "postgresql://postgres:password@db/postgres"

app = FastAPI()



# yeah, this'll have to do for now...
try:
    origin = os.environ["ORIGIN"]
except KeyError:
    # maybe a warning?
    origin = "http://localhost:8080"

origins = [
    origin
]



app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

database = databases.Database(DATABASE_URL)

metadata = sqlalchemy.MetaData()

submissions = sqlalchemy.Table(
    "submissions",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("ytid", sqlalchemy.String),
    # NOTE: default= NOT supported by "databases" !
    sqlalchemy.Column("created_at", sqlalchemy.DateTime, nullable=False),
    sqlalchemy.Column("ip", sqlalchemy.String),
    sqlalchemy.Column("datapoints", sqlalchemy.String),
)

engine = sqlalchemy.create_engine(DATABASE_URL)
metadata.create_all(engine)

def log(*msg, **kwargs):
    return
    print(*msg, **kwargs)
    sys.stdout.flush()

# To deal with caching of the value
cached_result = None
calculate_queue = asyncio.Queue()
tasks = []

@app.on_event("startup")
async def startup():
    await database.connect()
    task = asyncio.create_task(worker('statistics_worker', calculate_queue))
    tasks.append(task)

    # To populate our cache
    calculate_queue.put_nowait(0)

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

    # Finish what's in the queue..
    log("About to join queue...", end="")
    await calculate_queue.join()
    log("queue joined.")

    log("About to cancel task...", end="")
    # Then cancel the task
    for task in tasks:
        task.cancel()
    log("Task was cancelled")

    # once it has cancelled, we should be ready to catch
    # the returned CancelledError, at which point the task is complete
    log("About to gather tasks...", end="")
    await asyncio.gather(*tasks, return_exceptions=True)
    log("Done")

# prolly won't need this
def _get_defaults(db_table):
    defaults = {}
    for column in db_table.columns:
        if column.default is not None:
            value = column.default.arg
            if callable(value):
                value = value()
            defaults[column.name] = value
    return defaults

class SubmissionItem(BaseModel):
    ytid: str
    datapoints: conlist(int, min_items=1, max_items=500)

    #@validator('datapoints', pre=True)
    #def split_str(cls, v):
    #    if isinstance(v, str):
    #        return v.split('')
    #    return v


@app.get("/")
async def get_index():
    return cached_result

async def calculate_p():
    log("Entering calculate_p()")
    rows = await database.fetch_all(query=text("""
        SELECT
            ytid, datapoints, COUNT(ytid) as num_confirmed
        FROM
            submissions
        GROUP BY
            ytid, datapoints
        HAVING
            COUNT(ytid) >= 5
    """))

    log("sql query done")
    if len(rows) == 0:
        log("Rows had no results")
        return dict(first=0, second=0, third=0, fourth=0, p=-1)

    # results: dict that maps ytid -> list of result tuples
    # a particular ytid *could* in theory have multiple, conflicting
    # datapoints - but when that happens, we only want to select
    # the result dataset that most people voted for
    results = defaultdict(list)
    for row in rows:
        ytid = row["ytid"]
        incr = row["num_confirmed"]
        first = second = third = fourth = 0
        for num in row["datapoints"]:
            if num == "1":
                first += incr
            elif num == "2":
                second += incr
            elif num == "3":
                third += incr
            elif num == "4":
                fourth += incr
        results[ytid].append((incr, first, second, third, fourth))

    # want to sort every ytid, so that the most common result
    # is what we report
    for res in results.values():
        res.sort(key=lambda tup: tup[0])

    first = second = third = fourth = 0
    # calculate totals
    for res in results.values():
        incr, a, b, c, d = res[0]
        first += a
        second += b
        third += c
        fourth += d

    tot = first + second + third + fourth
    avg = tot / 4
    table = [
        [first, second, third, fourth],
        [avg]*4
    ]
    stat, p, dof, expected = chi2_contingency(table)
    
    return dict(
        first=first,
        second=second,
        third=third,
        fourth=fourth,
        p=p,
    )

async def worker(name, queue):
    global cached_result
    log("Worker started")
    while True:
        log("worker: About to wait for work")

        await queue.get()

        log("worker: Got some work!")

        try:
            cached_result = await calculate_p()
        except Exception as e:
            log("worker: Exception encountered in calculate_p()")
            log(e)
        queue.task_done()

        log("worker: Finished working")


@app.post("/", status_code=201)
async def post_new_result(
    item: SubmissionItem,
    request: Request,
    origin: Optional[str] = Header(None),
    #x_forwarded_for: Optional[str] = Header(None),
):
    values = item.dict()

    # the list of ints (datapoints) is stored as a string
    datapoints_stringified = "".join(str(x) for x in values["datapoints"])
    values.update(datapoints=datapoints_stringified)

    ip = urlparse(origin).netloc
    if ":" in ip:
        ip = ip.split(":")[0]

    # since "databases" does not support default column values,
    # we have to do it ourselves
    # (https://github.com/encode/databases/issues/72)
    # ... no, "databases" authors, default values is not "out of scope")
    now = datetime.datetime.now()
    values.update(ip=ip, created_at=now)

    query = submissions.insert().values(values)

    # TODO error handling
    async with database.transaction():
        await database.execute(query=query)

    # I need to put something into the queue, but I'm not using the value,
    # so I just put a 0 every time
    calculate_queue.put_nowait(0)

    return { "result": "ok" }
