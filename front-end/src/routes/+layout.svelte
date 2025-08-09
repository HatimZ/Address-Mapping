<script lang="ts">
	import '../app.css';
	import PageLayout from '$lib/components/PageLayout.svelte';
import { getTitle } from '$lib/state.svelte';
</script>

<PageLayout
 title= {getTitle()}
	subtitle="Prototype web application for calculating the distance between addresses."
>
	<slot />
</PageLayout>
