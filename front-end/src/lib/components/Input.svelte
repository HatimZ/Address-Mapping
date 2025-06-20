<script lang="ts">
	import { createEventDispatcher } from 'svelte';
	export let title: string;
	export let value: string = '';
	export let id: string = '';
	export let type: string = 'text';
	export let placeholder: string = '';
	export let disabled: boolean = false;
	export let required: boolean = false;
	const dispatch = createEventDispatcher();

	function onInput(event: Event) {
		const target = event.target as HTMLInputElement;
		value = target.value;
		dispatch('input', value);
	}
</script>

<div class="flex flex-col gap-1 w-full">
	<label class="text-sm font-medium text-secondary" for={id}>{title}</label>
	<input
		class="w-full px-4 py-3 bg-[#F8F8F6] border-0 border-b border-gray-300 focus:outline-none font-inter text-base transition-colors disabled:opacity-50"
		{id}
		{type}
		{placeholder}
		bind:value
		{disabled}
		{required}
		on:input={onInput}
		{...$$restProps}
	/>
</div>
