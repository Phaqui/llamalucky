<script lang='typescript'>
  import Router, { location } from 'svelte-spa-router';
  import Navbar from './components/Navbar.svelte';
  import { routes } from './routes';
</script>
  
<style>
</style>
  
{#if $location !== "/"}
  <Navbar />
{/if}

<Router {routes} />
