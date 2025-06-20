<script lang="ts">
	export let headers: string[] = [];
	export let data: any[] = [];
	export let title: string | null = null;
	export let subtitle: string | null = null;
	export let page: number = 1;
	export let pageSize: number = 5;
	export let total: number = 0;
	export let onPageChange: (page: number) => void = () => {};

	$: pageCount = Math.ceil(total / pageSize);

	function gotoPage(p: number) {
		if (p >= 1 && p <= pageCount) onPageChange(p);
	}
</script>

<div class="bg-white rounded-xl shadow-sm p-8 w-full">
	{#if title}
		<h2 class="text-2xl font-medium text-primary mb-1">{title}</h2>
	{/if}
	{#if subtitle}
		<p class="text-base text-secondary mb-6">{subtitle}</p>
	{/if}
	<div class="overflow-x-auto">
		<table class="min-w-full border-separate border-spacing-0">
			<thead>
				<tr class="bg-gray-200">
					{#each headers as header}
						<th class="px-4 py-3 text-left font-semibold text-sm text-primary w-[200px]">
							{header}
						</th>
					{/each}
				</tr>
			</thead>
			<tbody>
				{#each data as row, i}
					<tr class="border-b last:border-b-0">
						{#each headers as header, j}
							<td class="px-4 py-3 text-sm text-secondary w-[200px]" title={row[header]}>
								{row[header]}
							</td>
						{/each}
					</tr>
				{/each}
			</tbody>
		</table>
	</div>
	<!-- Pagination Controls -->
	<div class="flex justify-end items-center gap-2 mt-4">
		<button
			class="px-3 py-1 rounded bg-gray-200"
			on:click={() => gotoPage(page - 1)}
			disabled={page === 1}>&lt;</button
		>
		<span>Total {total}, Page {page} of {pageCount}</span>
		<button
			class="px-3 py-1 rounded bg-gray-200"
			on:click={() => gotoPage(page + 1)}
			disabled={page === pageCount}>&gt;</button
		>
	</div>
</div>
