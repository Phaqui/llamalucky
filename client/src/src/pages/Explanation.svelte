<script lang="ts">
  import { link } from 'svelte-spa-router';
</script>

<blockquote>
  <h2>ELI5, please</h2>

  <p>
    A site where watchers of MrLlama
    (<a href="https://youtube.com/mrllamasc">youtube</a>,
    <a href="https://www.twitch.tv/mrllamasc">twitch</a>)
    can submit results about MrLlama's luck in the Arcane Sanctuary,
    and together, once and for all, find out if MrLlama really is as
    unlucky as he makes the impression of being.
  </p>
</blockquote>

<blockquote>
  <h2>I am committed to truth! How do I contribute?</h2>
  <p>
    Head over to the <a use:link href="/submit">submit page</a>, enter a
    youtube link (or just youtube video id) where MrLlama plays Diablo II,
    and for each time he has to go through the Arcane Sanctuary in that
    video, mark which "way" he got (1st through 4th way). (One video may
    feature several or many runs through the Arcane, so be sure to get
    them all before you submit!).
  </p>
</blockquote>

<blockquote>
  <h2>But wait, how can you determine his luck from this?</h2>
  <p>Statistics.</p>
  <p class="italic gray">
    (Disclaimer: I have no clue about statistics, I relied on the
    interwebs to come up with this. I encourage anyone who actually
    knows statistics to reach out, so we can correct my mistakes (or
    tell me that I, somehow, got it right (not likely)). You'll find
    the github repo on the top right.
  </p>
  <p>
    Results are based on a Chi-square independency test of 2 variables,
    one of which are the numbers of confirmed "ways" (number of 1st ways,
    2nd ways, etc), and the other a "correction"
    result which is uniform with cell values equal to the average of
    the sum of the 4 column points above. Using a significance (p-level)
    of 0.05, we can determine if the results of "ways" we have gotten
    indicates that the true distrubtion of Mrllama's runs through the
    arcane sanctuary is uniform or not. (As a side note, I have assumed
    them to be, which I believe is a reasonable assumption).
  </p>
  <p>
    Additionally, when we have less data, we are more unsure, and that
    fact is reflected in the wording of the verdict that you see on
    the Stats page. Again, refer to the code on github to see exactly
    what's going on.
  </p>
</blockquote>

<style>
  blockquote {
    font-size: 1.3em;
    border-left: 10px solid #5239ff;
    background-color: rgb(81, 166, 90);
    padding: 1em;
  }

  blockquote h2 {
    font-size: 1.2em;
    margin: 0 auto 0.5em auto;
  }

  p.italic { font-style: italic; }
  p.gray { color: #3e2323; }
</style>
