<script lang="ts">
  import { link } from 'svelte-spa-router';
</script>

<nav>
  <a use:link href="/">Landing</a>
  <a use:link href="/explanation">What</a>
  <a use:link href="/submit">Submit</a>
  <a use:link href="/stats">Stats</a>
</nav>

<style>
  nav {
    background-color: rgb(166, 49, 49);
    padding: 2vh 0;
  }

  nav a {
    text-decoration: none;
    padding-left: 0.5em;
    color: rgb(7, 2, 30);
    font-size: 1.4em;
    font-weight: bold;
  }

  nav a::before {
    content: '•';
    text-decoration: none;
    padding-left: 0.9em;
    color: rgb(50, 50, 50);
  }
</style>
