<script lang="ts">
  import { push } from 'svelte-spa-router';
</script>

Landing page

<button on:click={() => push('/explanation')}>What?</button>
<button on:click={() => push('/submit')}>Submit information</button>
