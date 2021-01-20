import Landing from './pages/Landing.svelte';
import Explanation from './pages/Explanation.svelte';
import Submit from './pages/Submit.svelte';
import Stats from './pages/Stats.svelte';
import NotFound from './pages/NotFound.svelte';

export const routes = {
    '/': Landing,
    '/explanation': Explanation,
    '/submit': Submit,
    '/stats': Stats,

    '*': NotFound,
}
