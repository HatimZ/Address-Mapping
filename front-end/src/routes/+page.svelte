<script lang="ts">
	import Card from '$lib/components/Card.svelte';
	import Input from '$lib/components/Input.svelte';
	import Button from '$lib/components/Button.svelte';
	import RadioButton from '$lib/components/RadioButton.svelte';
	import type { DistanceRequest, DistanceResponse } from '$lib/types';
	import { calculateDistance } from '$lib/api/distance';
	import { CalculatorIcon } from '$lib/icons';
	import { DistanceType } from '$lib/types';

	let selected: DistanceType = DistanceType.Miles;
	let address1 = '';
	let address2 = '';
	let distance: DistanceResponse | null = null;
	let loading = false;
	let errorMsg = '';
	let showToast = false;

	function addressEmpty() {
		return !address1.trim() || !address2.trim();
	}

	async function calculateDistanceHandler() {
		loading = true;
		errorMsg = '';
		showToast = false;
		distance = null;
		try {
			const body: DistanceRequest = { address1, address2 };
			distance = await calculateDistance(body);
		} catch (err) {
			errorMsg = err instanceof Error ? err.message : 'Unknown error';
			showToast = true;
		} finally {
			loading = false;
		}
	}
</script>

<Card>
	<div class="flex flex-col md:flex-row gap-8">
		<Input
			title="Source Address"
			placeholder="Input address"
			id="source-address"
			bind:value={address1}
		/>
		<Input
			title="Destination Address"
			placeholder="Input address"
			id="destination-address"
			bind:value={address2}
		/>
		<span>
			<div class="text-sm font-medium text-secondary">Unit</div>
			<RadioButton
				name="Miles"
				value={DistanceType.Miles}
				checked={selected === DistanceType.Miles}
				onClick={() => (selected = DistanceType.Miles)}
			/>
			<RadioButton
				name="Kilometers"
				value={DistanceType.Kilometers}
				checked={selected === DistanceType.Kilometers}
				onClick={() => (selected = DistanceType.Kilometers)}
			/>
			<RadioButton
				name="Both"
				value={DistanceType.All}
				checked={selected === DistanceType.All}
				onClick={() => (selected = DistanceType.All)}
			/>
		</span>
		<span class="min-w-[200px] flex flex-col">
			<div class="text-sm font-medium text-secondary">Distance</div>
			{#if loading}
				<span class=" text-gray-400">Calculating...</span>
			{:else if distance !== null && selected == DistanceType.Kilometers}
				<span class=" text-primary font-bold">{distance.kilometers} km</span>
			{:else if distance !== null && selected == DistanceType.Miles}
				<span class=" text-primary font-bold">{distance.miles} miles</span>
			{:else if distance !== null && selected == DistanceType.All}
				<span class=" text-primary font-bold">{distance.miles} miles {distance.kilometers} km</span>
			{/if}
		</span>
	</div>
	<Button
		name="Calculate Distance"
		variant="primary-button"
		onClick={calculateDistanceHandler}
		disabled={loading || addressEmpty()}
	>
		<span slot="icon">{@html CalculatorIcon()}</span>
	</Button>
</Card>

{#if showToast}
	<div
		class="fixed bottom-6 right-6 z-50 bg-red-600 text-white px-6 py-3 rounded shadow-lg animate-fade-in"
	>
		{errorMsg}
	</div>
{/if}

<style>
	@keyframes fade-in {
		from {
			opacity: 0;
			transform: translateY(20px);
		}
		to {
			opacity: 1;
			transform: translateY(0);
		}
	}
	.animate-fade-in {
		animation: fade-in 0.3s ease;
	}
</style>
