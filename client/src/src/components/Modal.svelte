<script lang="ts">
  import { createEventDispatcher } from 'svelte';
  import { fade } from 'svelte/transition';
  import { quintOut } from 'svelte/easing';
  const dispatch = createEventDispatcher();
</script>

<!-- disable erroronous warning, this is a svelte bug -->
{#if false}<slot></slot>{/if}

<div id="container">
  <div id="backdrop"
    in:fade={{ duration: 250, delay: 50, easing: quintOut }}
    out:fade={{ duration: 75, easing: quintOut }}
    on:click={() => dispatch('close')}>
  </div>
  <div id="inner">
    <slot name="content"></slot>
  </div>
</div>

<style>
  #container {
    position: absolute;
    height: 100%;
    width: 100%;
    top: 0;
    left: 0;
    display: flex;
    justify-content: center;
    align-items: center;
  }

  #backdrop {
    position: absolute;
    height: 100%;
    width: 100%;
    background-color: rgba(0, 0, 0, 0.35);
    z-index: 50;
  }

  #inner {
    position: relative;
    z-index: 51;
  }
</style>
