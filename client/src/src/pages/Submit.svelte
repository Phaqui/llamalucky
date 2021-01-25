<script lang="ts">
  type EvType = KeyboardEvent & { target: EventTarget & HTMLInputElement };
  import Modal from './../components/Modal.svelte';
  import Datapoint from './../components/Datapoint.svelte';
  const server_url = "http://localhost:8000";

  let modal_showing = false;
  enum YTID_STATE {
    NotInitd = "notinitd",
    ParseError = "parseerror",
    Waiting = "waiting",
    Err = "error",
    Ok = "ok",
    NotOk = "notok"
  };

  let ytid_input = "";
  let ytid_status: YTID_STATE = YTID_STATE.NotInitd;
  $: can_submit = datapoints.length > 0 && ytid_status === YTID_STATE.Ok;
  $: ytid_status_text = get_ytid_status_text(ytid_status);

  let timeout_id: number | null = null;
  function on_input_keyup(ev: EvType) {
    if (timeout_id !== null) {
      window.clearTimeout(timeout_id);
    }
    const text = ev.target.value;
    console.log(text);

    if (text === "") {
      ytid_status = YTID_STATE.NotInitd;
      return;
    }

    const parsed = parse_input(text);
    if (parsed === null) {
      ytid_status = YTID_STATE.ParseError;
      return;
    }

    ytid_status = YTID_STATE.Waiting;
    timeout_id = window.setTimeout(async function () {
      ytid_status = await ytapi_verify_ytid(text);
    }, 1500);
  }

  function get_ytid_status_text(status: YTID_STATE) {
    switch (status) {
      case YTID_STATE.NotInitd:
        return '';
      case YTID_STATE.ParseError:
        return 'Cannot understand that youtube-link or video id.';
      case YTID_STATE.Waiting:
        return '...waiting for youtube-api...';
      case YTID_STATE.Err:
        return "⚠ Couldn't reach youtube api for verification!";
      case YTID_STATE.Ok:
        return "✔ Yep, looks like a legit MrLlamaSC video!";
      case YTID_STATE.NotOk:
        return "☹ That's not a MrLlamaSC video!";
    }
  }

  function parse_input(input: string): string | null {
    let url;

    try {
      url = new URL(input);
    } catch (err) {
      // - Should be 11 characters (or around there, but we're being safe)
      // - Allowed symbols: a-z, A-Z, 0-9, -, and _
      return /^[a-zA-Z0-9_\-]{7,14}$/.test(input) ? input : null;
    }

    return url.searchParams.get('v');
  }

  async function ytapi_verify_ytid(ytid: string): Promise<YTID_STATE> {
    // @ts-ignore
    let response = await gapi.client.youtube.videos.list({
      "part": ["snippet"],
      "id": [ ytid ]
    });

    if (response.status !== 200) {
      console.debug("gapi client call returned non-200 status");
      console.debug(response.status);
      return YTID_STATE.Err;
    }
    const data = response.result;

    const ok = (data.items.length > 0) &&
               (data.items[0].kind === "youtube#video") &&
               (data.items[0].snippet.channelTitle === "MrLlamaSC");

    return ok ? YTID_STATE.Ok : YTID_STATE.NotOk;
  }

  let datapoints: Array<number> = [1];

  function remove(idx: number) {
    datapoints.splice(idx, 1);
    datapoints = datapoints;
  }

  function add() {
    datapoints.push(1);
    datapoints = datapoints;
  }

  function set_selected(run: number, way: number) {
    datapoints[run] = way;
    console.log(datapoints);
  }

  async function submitResults() {
    if (!can_submit) return;

    let response = await fetch(server_url + "/", {
      method: "POST",
      mode: "cors",
      body: JSON.stringify({ ytid: ytid_input, datapoints }),
    });

    if (response.status === 201) {
      datapoints = [1];
      ytid_input = '';
      modal_showing = true;
    } else {
      // do something...
    }
  }
</script>

{#if modal_showing}
  <Modal on:close={() => modal_showing = false}>
    <div id="modal-container" slot="content">
      <div>
        <h2>Thank you</h2>

        <p>Your submission to this great cause has been recorded.</p>
        <p>Feel free to feel good about yourself.</p>

        <button on:click={() => modal_showing = false}>Great</button>
      </div>
    <div>
  </Modal>
{/if}

<div class="container">
  <div style="text-align: center">
    <label>
      YouTube-link or video id: 
      <input bind:value={ytid_input} on:keyup={on_input_keyup}>
    </label>

    <span id="ytid-status" class={ytid_status}>
      <p>{ytid_status_text}</p>
    </span>
  </div>

  <div id="datapoints">
    {#each datapoints as dp, i}
      <Datapoint
        run={i + 1}
        on:selected={way => set_selected(i, way.detail)}
        on:delete={() => remove(i)}
      />
    {/each}

    <button class="add" on:click={add}>Add row</button>
  </div>

  <button on:click={submitResults} disabled={!can_submit}>
    Submit findings
  </button>
</div>

<style>
  .container {
    display: flex;
    flex-direction: column;
    justify-content: space-evenly;
    align-items: center;
    height: 100%;
  }

  label {
    font-size: 1.5em;
    color: white;
    text-align: center;
  }

  label > input {
    display: block;
    padding: 0.7em;
    margin-top: 2em;
    border: 0;
    font-size: 1em;
    width: 45rem;
    background-color: rgb(202, 208, 215);
  }

  #ytid-status {
    size: 1.2em;
    font-weight: bold;
  }

  #ytid-status.notinitd { display: none; }
  #ytid-status.waiting { color: #b7b6b6; letter-spacing: 0.05em; }
  #ytid-status.ok { color: #2fbd2a; }
  #ytid-status.notok { color: #d33; }
  #ytid-status.parseerror { color: #d33; }
  #ytid-status.error { color: orange; }

  #datapoints {
    display: flex;
    flex-direction: column;
    padding: 1em;
    border: 0;
    margin: 0.3em;
  }

  button.add {
    padding: 2px;
    font-size: 1.5em;
    background-color: rgb(50, 100, 100);
    border: 1px solid transparent;
    box-shadow: none;
  }

  /* the modal */
  #modal-container {
    padding: 2em;
    background-color: rgb(178, 159, 202);
    border-radius: 10%;
  }

  #modal-container > div {
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    
  }
</style>
