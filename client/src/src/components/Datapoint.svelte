<script lang="ts">
  import { createEventDispatcher } from 'svelte';
  const dispatch = createEventDispatcher();

  export let run = 0;
  export let selected = 0;

  function set_selected(way: number) {
    selected = selected === way ? 0 : way;
    dispatch('selected', selected);
  }
</script>

<div class="container">
  <div>Run #{run}</div>
  {#each [1, 2, 3, 4] as way}
    <button
      on:click={() => set_selected(way)}
      class:selected={selected === way}>{way}</button>
  {/each}
  <div class="delete" on:click={() => dispatch('delete')}>✕</div>
</div>

<style>
  div.container {
    display: flex;
    justify-content: center;
    align-items: center;
    border-top-right-radius: 2px;
    border-top-left-radius: 2px;
    background-color: #7e918e;
    padding-left: 0.6em;
    border-left: 0.6em solid #cad0d7;
    margin: 0.15em auto;
  }

  div.container div {
    font-size: 1.5em;
  }

  div.container div.delete {
    cursor: pointer;
    color: rgb(83, 83, 83);
    padding-right: 0.1em;
    font-size: 3em;
    transition: color 0.12s ease-out;
  }

  div.container div.delete:hover {
    color: rgb(227, 47, 47);
  }

  button {
    padding: 0.4em 0.9em;
    border: 1px solid #464241;
    margin: 0.15em;
    box-shadow: none;
    background-color: #52624e;
    transition: background-color 0.12s ease-in;
  }
  
  button.selected:nth-of-type(1) { background-color: #8fd780; }
  button.selected:nth-of-type(2) { background-color: #8880ea; }
  button.selected:nth-of-type(3) { background-color: #ea80c1; }
  button.selected:nth-of-type(4) { background-color: #ea8080; }
</style>
