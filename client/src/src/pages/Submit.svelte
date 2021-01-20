<script lang="ts">
  const server_url = "http://localhost:8000";

  let ytid_input = "";
  $: ytid = parse_input(ytid_input);
  $: cant_parse_url = ytid === null;
  $: can_submit = datapoints.length > 0 && !cant_parse_url;

  function parse_input(input: string) {
    // TODO do more parsing, to retrieve only the ID
    let url;
    try {
      url = new URL(input);
    } catch (err) {
      // yeah, we're just gonna assume this format of a valid youtube video id for now:
      // - 11 characters (or at least around there..)
      // - Allowed symbols: a-z, A-Z, 0-9, -, and _
      
      /* see: https://webapps.stackexchange.com/questions/54443/format-for-id-of-youtube-video
         If you need to validate that random user input corresponds to a valid video id,
         I'd recommend doing an empirical test. Attempt to access
         http://gdata.youtube.com/feeds/api/videos/VIDEO_ID
         If you get a 200 response, then VIDEO_ID is valid. If you get a non-200 response,
         you have an invalid id. There are some edge cases for newly uploaded videos or private
         videos, but for most purposes I'd assume that would be okay.*/
      return /^[a-zA-Z0-9]{6,15}$/.test(input) ? input : null;
    }

    return url.searchParams.get('v');
  }

  let datapoints = [1];

  function remove(idx: number) {
    datapoints.splice(idx, 1);
    datapoints = datapoints;
  }

  function add() {
    datapoints.push(1);
    datapoints = datapoints;
  }

  async function submitResults() {
    if (datapoints.length === 0) return;

    let response = await fetch(server_url + "/", {
      method: "POST",
      mode: "cors",
      body: JSON.stringify({ ytid, datapoints }),
    });

    if (response.status === 201) {
      datapoints = [1];
      ytid_input = '';
      console.log("success");
    } else {
      // do something...
    }
  }
</script>

<div class="container">
  <label>
    YouTube-link or video id: 
    <input bind:value={ytid_input}>
  </label>

  {#if ytid_input !== "" && cant_parse_url}
    <p style="color: red">Cannot understand that youtube-link or video id.</p>
  {/if}

  <button on:click={submitResults} disabled={!can_submit}>Submit findings</button>

  {#each datapoints as dp, i}
    <div>
      <select bind:value={dp}>
        <option value="1">1st way</option>
        <option value="2">2nd way</option>
        <option value="3">3rd way</option>
        <option value="4">4th way</option>
      </select>
      <button class="remove" on:click={() => remove(i)}>✖</button>
    </div>
  {/each}

  <button on:click={add}>Add</button>
</div>

<style>
  .container {
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
  }

  button.remove {
    padding: 2px;
    background-color: transparent;
    color: rgb(230, 110, 110);
    font-size: 1.5em;
    border: 1px solid transparent;
    box-shadow: none;
  }
</style>
