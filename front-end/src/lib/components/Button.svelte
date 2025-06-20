<script lang="ts">
	export let name: string;
	export let onClick: (e: MouseEvent) => void = () => {};
	export let disabled: boolean = false;
	export let type: 'button' | 'submit' | 'reset' = 'button';
	export let variant: 'primary-button' | 'secondary-button' | 'tertiary-button' = 'primary-button';
</script>

<button
	class="flex items-center justify-between gap-2 px-6 py-3 w-[237px] h-12 font-inter cursor-pointer font-normal text-[14px] leading-[18px] tracking-[0.16px] transition-colors focus:outline-none disabled:opacity-50 disabled:cursor-not-allowed {variant}"
	{type}
	on:click={onClick}
	{disabled}
	{...$$restProps}
>
	<span>{name}</span>
	<slot name="icon" />
</button>
