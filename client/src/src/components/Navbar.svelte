<script lang="ts">
  import { link } from 'svelte-spa-router';
</script>

<nav>
  <a class="menuitem" use:link href="/">Llamalucky</a>
  <a class="menuitem" use:link href="/explanation">What</a>
  <a class="menuitem" use:link href="/submit">Submit</a>
  <a class="menuitem" use:link href="/stats">Stats</a>
  <a class="push" href="https://github.com/phaqui">
    <img src="/GitHub-Mark-64px.png" alt="GitHub Mark" />
  </a>
</nav>

<style>
  nav {
    background-color: rgb(166, 49, 49);
    padding: 1.5vh 0;
    display: flex;
    justify-content: center;
    align-items: center;
  }

  nav a {
    text-decoration: none;
    padding-left: 0.5em;
    color: rgb(7, 2, 30);
    font-size: 1.4em;
    font-weight: bold;
  }

  nav a:last-child {
    margin-right: 0.6em;
  }

  nav a.menuitem::before {
    content: '•';
    text-decoration: none;
    padding-left: 0.6em;
    color: rgb(50, 50, 50);
  }

  nav a.push {
    margin-left: auto;
  }

  nav a img {
    height: 3.5vh;
    filter: drop-shadow(0px 0px 20px #c2c0d0);
  }

  nav a img:hover {
    filter: drop-shadow(0 0 0 white);
  }
</style>
