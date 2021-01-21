<script lang="ts">
  import { onMount } from 'svelte';

  const server_url = "http://localhost:8000";

  // data we will recieve from the api
  // lucky = #1st ways + #2nd ways > #3rd ways + #4th ways
  //   that is, considered "lucky" if more early ways (1st, 2nd),
  //   and unlucky if more later (3rd, 4th) ways
  let p = -1;
  let records = [0, 0, 0, 0];

  const ways = ["1st", "2nd", "3rd", "4th"];

  let verdict = "(waiting for api...)";

  function determine_verdict() {
    verdict = "";

    let anyunder10 = records.some(val => val < 10);
    let anyunder20 = records.some(val => val < 20);
    let anyunder40 = records.some(val => val < 40);
    let anyunder75 = records.some(val => val < 75);

    let anyunderx = [anyunder10, anyunder20, anyunder40, anyunder75, true];

    // 0, 1, 2, 3, 4
    let idx = anyunderx.indexOf(true);
    switch (idx) {
      case 0:
        verdict = "Undetermined. Needs more data!";
        return;
      case 1:
        verdict = "It's possible that";
        break;
      case 2:
        verdict = "It's likely that";
        break;
      case 3:
        verdict = "It's very likely that";
        break;
      case 4:
        verdict = "It's practically confirmed that";
        break;
    }

    if (p < 0.05) {
      // reject h0 (distribution non-uniform)

      // define "lucky" to be more 1st and 2nd ways, and
      // "unlucky" to be more 3rd and 4th ways
      const lucky = records[0] + records[1] > records[2] + records[3]
      verdict += `MrLlama is truly ${lucky ? '' : 'un'}lucky`;
    } else {
      // accept h0 (distribution is uniform)
      verdict += `MrLlma sees an equal amount of ways.`;
    }
  }

  onMount(async () => {
    let response = await fetch(server_url + "/");

    if (response.status === 200) {
      let data = await response.json();
      records = [
        data.first,
        data.second,
        data.third,
        data.fourth
      ];
      p = data.p;
      determine_verdict();
    }
  });
</script>


<div class="container">
  <div class="ways centered">
    {#each ways as way, i}
      <div class="way">
        <h2>{records[i]}</h2>
        <p>Number of {way} ways on record</p>
      </div>
    {/each}
  </div>

  <div id="verdict" class="centered">
    <h1>&#187; Verdict</h1>
    <p>{verdict}</p>
  </div>

  <div id="verdict_how" class="centered">
    <p>
      Results based on a Chi-square independency test of 2 variables,
      one of which are these numbers above, and the other a "correction"
      result which is uniform with cell values equal to the average of
      the sum of the 4 column points above.
    </p>

    <p>
      Disclaimer: I have no clue about statistics, I relied on the
      interwebs to come up with this. I encourage anyone who actually
      knows statistics to reach out for me, and yell at me, or tell me
      that I actually was correct (not likely).</p>
  </div>

  <div>
    <button>more stats</button>
  </div>
</div>

<style>
  .container {
    height: 100%;
    display: flex;
    flex-direction: column;
    justify-content: space-evenly;
    align-items: center;
  }

  .centered {
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
  }

  .ways {
    display: flex;
    flex-direction: row;
    justify-content: space-evenly;
    align-items: space-evenly;
    width: 100%;
    height: 25vh;
  }

  .way {
    border: 2px solid #2b2424;
    box-shadow: 3px 3px 20px 1px rgb(17, 15, 15);
    border-radius: 8px;
    height: 100%;
    width: 20vw;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
  }

  .way:nth-child(1) { background-color: #8fd780; }
  .way:nth-child(2) { background-color: #8880ea; }
  .way:nth-child(3) { background-color: #ea80c1; }
  .way:nth-child(4) { background-color: #ea8080; }

  .way > h2 {
    font-weight: normal;
    color: rgb(35, 35, 35);
    font-size: 3em;
  }

  .way > p {
    text-align: center;
    color: rgb(40, 40, 40);
    font-size: 1.1em;
    font-style: italic;
  }

  #verdict > h1 {
    padding: 1em 10em 1em 3em;
    color: #20071b;
    border-left: 0.5em solid #732b2b;
    border-top-left-radius: 5%;
    border-bottom-left-radius: 1%;
    margin-bottom: 0;
    background:
      linear-gradient(40deg, rgba(240, 194, 135, 0.2) 70%, 70%, rgba(30, 38, 37, 0)),
      linear-gradient(80deg, rgba(240, 224, 89, 0.7) 60%, 60%, rgba(30, 38, 37, 0)),
      linear-gradient(60deg, rgba(240, 194, 155, 0.4) 70%, 70%, rgba(30, 38, 37, 0)),
      linear-gradient(135deg, rgba(240, 194, 135, 0.3) 70%, 70%, rgba(30, 38, 37, 0));
  }

  #verdict > p {
    padding: 1em 5em 1em 8em;
    color: #20071b;
    font-size: 1.5em;
    border-top-right-radius: 25%;
    background:
      linear-gradient(40deg, rgba(30, 38, 37, 1) 20%, 20%, rgba(175, 195, 220, 0.3), 90%, rgba(0, 0, 0, 0) 90%),
      linear-gradient(80deg, rgba(30, 38, 37, 1) 20%, 20%, rgba(175, 195, 220, 0.8), 90%, rgba(0, 0, 0, 0) 90%),
      linear-gradient(140deg, rgba(30, 38, 37, 1) 10%, 10%, rgba(175, 195, 220, 0.4));
  }

</style>
