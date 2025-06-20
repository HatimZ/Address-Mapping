<script lang="ts">
	import Button from './Button.svelte';
	import { page } from '$app/stores';
	import { goto } from '$app/navigation';
	import { derived } from 'svelte/store';

	export let title: string;
	export let subtitle: string = '';

	// Simple SVG icons
	const ClockIcon = () =>
		`<svg xmlns='http://www.w3.org/2000/svg' fill='none' viewBox='0 0 24 24' stroke='currentColor' class='w-5 h-5'><path stroke-linecap='round' stroke-linejoin='round' stroke-width='2' d='M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z'/></svg>`;
	const CalculatorIcon = () =>
		`<svg xmlns='http://www.w3.org/2000/svg' fill='none' viewBox='0 0 24 24' stroke='currentColor' class='w-5 h-5'><rect width='16' height='20' x='4' y='2' rx='2' stroke='currentColor' stroke-width='2' fill='none'/><path stroke='currentColor' stroke-width='2' d='M8 6h8M8 10h8M8 14h2m4 0h2m-6 4h2m4 0h2'/></svg>`;

	// Derived store for current path
	const currentPath = derived(page, ($page) => $page.url.pathname);
</script>

<div class="min-h-screen w-full bg-[#F8F8F6] font-inter px-12 py-8" {...$$restProps}>
	<div class="flex flex-col sm:flex-row justify-between items-start px-4 py-8 w-full">
		<div class="flex-1">
			<h1 class="text-4xl text-primary mb-2">{title}</h1>
			{#if subtitle}
				<p class="text-base text-secondary mb-8">{subtitle}</p>
			{/if}
		</div>
		{#if $currentPath === '/'}
			<Button
				name="View Historical Queries"
				variant="secondary-button"
				onClick={() => goto('/history')}
			>
				<span slot="icon">{@html ClockIcon()}</span>
			</Button>
		{:else if $currentPath === '/history'}
			<Button name="Back to Calculator" variant="tertiary-button" onClick={() => goto('/')}>
				<span slot="icon">{@html CalculatorIcon()}</span>
			</Button>
		{/if}
	</div>
	<slot />
</div>
