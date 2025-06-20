<script lang="ts">
	export let name: string;
	export let value: string = '';
	export let checked: boolean = false;
	export let onClick: (e: MouseEvent) => void = () => {};
	export let id: string = '';
</script>

<label class="flex items-center gap-2 cursor-pointer select-none">
	<input
		type="radio"
		class="form-radio accent-primary w-5 h-5 cursor-pointer"
		{id}
		{value}
		{checked}
		on:click={onClick}
		{...$$restProps}
	/>
	<span class="text-base text-primary">{name}</span>
</label>
