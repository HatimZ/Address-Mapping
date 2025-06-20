<script lang="ts">
	// No required props, but accept $$restProps for flexibility
</script>

<div
	class="bg-white w-full rounded-xl shadow-sm p-8 font-inter gap-8 flex flex-col"
	{...$$restProps}
>
	<slot />
</div>
