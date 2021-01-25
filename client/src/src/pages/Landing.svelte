<script lang="ts">
  import { push } from 'svelte-spa-router';
</script>

<div class="container">
  <div>
    <h1>Is the 4th way real?</h1>
    <h3>- Is MrLlama really as unlucky as one may be lead to believe?</h3>
  </div>

  <div class="buttons">
    <div>
      <button on:click={() => push('/explanation')}>What?</button>
      <p>Tell me how it works</p>
    </div>
    <div>
      <button on:click={() => push('/submit')}>Submit information</button>
      <p>Submit run information for a video</p>
    </div>
  </div>
</div>

<style>
  .container {
    color: white;
    display: flex;
    flex-direction: column;
    justify-content: space-evenly;
    align-items: center;
    height: 70vh;
  }

  h3 {
    font-style: italic;
    margin-left: 20vw;
  }

  .buttons {
    width: 80vw;
    display: flex;
    justify-content: space-evenly;
  }

  .buttons div {
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
  }

  .buttons div p {
    color: rgb(220, 220, 220);
  }
</style>
