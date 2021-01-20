<script lang="ts">
  import { onMount } from 'svelte';

  const server_url = "http://localhost:8000";

  let records = [0, 0, 0, 0];
  let ways = ["1st", "2nd", "3rd", "4th"];

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
    <h1>Verdict</h1>
    <p>Currently, Mr Llama is NOT unlucky</p>
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


</style>
