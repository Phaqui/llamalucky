from typing import List, Optional
import datetime
from urllib.parse import urlparse

from pydantic import BaseModel
from fastapi import FastAPI, Header, Request
from fastapi.middleware.cors import CORSMiddleware
import sqlalchemy
from sqlalchemy.sql.expression import insert
import databases

DATABASE_URL = "postgresql://postgres:password@db/postgres"

app = FastAPI()

origins = [
    "http://localhost:8080"
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

@app.on_event("startup")
async def startup():
    await database.connect()

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

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
    datapoints: List[str]

    def dict(self):
        res = super().dict()
        res["datapoints"] = "".join(res["datapoints"])
        return res



@app.get("/")
async def get_index():
    query = submissions.select()
    rows = await database.fetch_all(query=query)

    first = second = third = fourth = 0
    for row in rows:
        for num in row["datapoints"]:
            if num == "1":
                first += 1
            elif num == "2":
                second += 1
            elif num == "3":
                third += 1
            elif num == "4":
                fourth += 1

    return dict(
        first=first,
        second=second,
        third=third,
        fourth=fourth
    )


@app.post("/", status_code=201)
async def post_new_result(
    item: SubmissionItem,
    request: Request,
    origin: Optional[str] = Header(None),
    #x_forwarded_for: Optional[str] = Header(None),
):
    values = item.dict()

    ip = urlparse(origin).netloc
    if ":" in ip:
        ip = ip.split(":")[0]

    # since "databases" does not support default column values,
    # we have to do it ourselves
    # (https://github.com/encode/databases/issues/72)
    # ... no, "databases" authors, it is not "out of scope"
    now = datetime.datetime.now()
    values.update(ip=ip, created_at=now)
    query = submissions.insert().values(values)

    # TODO error handling
    await database.execute(query=query)

    return { "result": "ok" }
