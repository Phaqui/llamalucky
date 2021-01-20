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
    <h1>&#187; Verdict</h1>
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

  #verdict > h1 {
    padding: 1em 10em 1em 3em;
    color: #20071b;
    border-left: 0.5em solid #732b2b;
    border-top-left-radius: 5%;
    border-bottom-left-radius: 1%;
    background:
      linear-gradient(40deg, rgba(240, 194, 135, 0.2) 70%, 70%, rgba(30, 38, 37, 0)),
      linear-gradient(80deg, rgba(240, 224, 89, 0.7) 60%, 60%, rgba(30, 38, 37, 0)),
      linear-gradient(60deg, rgba(240, 194, 155, 0.4) 70%, 70%, rgba(30, 38, 37, 0)),
      linear-gradient(135deg, rgba(240, 194, 135, 0.3) 70%, 70%, rgba(30, 38, 37, 0));
  }

</style>
