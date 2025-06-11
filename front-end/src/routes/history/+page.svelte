<script lang="ts">
	import { onMount } from 'svelte';
	import Card from '$lib/components/Card.svelte';
	import Table from '$lib/components/Table.svelte';
	import type { HistoryResponse, Query } from '$lib/types';
	import { getHistoricalQueries } from '$lib/api/history';

	let historicalQueries: Query[] = [];
	let loading = true;
	let errorMsg = '';
	let page = 1;
	let pageSize = 5;
	let total = 0;

	const headers = [
		'Source Address',
		'Destination Address',
		'Distance in Miles',
		'Distance in Kilometers'
	];

	async function fetchPage(p: number) {
		loading = true;
		errorMsg = '';
		try {
			const data: HistoryResponse = await getHistoricalQueries(p, pageSize);
			historicalQueries = data.items;
			total = data.pagination.total;
			page = p;
		} catch (err) {
			errorMsg = err instanceof Error ? err.message : 'Unknown error';
		} finally {
			loading = false;
		}
	}

	onMount(() => {
		fetchPage(1);
	});

	function handlePageChange(p: number) {
		fetchPage(p);
	}

	$: tableData = historicalQueries.map((q) => ({
		'Source Address': q.address1,
		'Destination Address': q.address2,
		'Distance in Miles': q.miles?.toFixed(2) || '-',
		'Distance in Kilometers': q.kilometers?.toFixed(2) || '-'
	}));
</script>

<Card>
	<Table
		{headers}
		data={tableData}
		title="Historical Queries"
		subtitle="History of the user's queries."
		{page}
		{pageSize}
		{total}
		onPageChange={handlePageChange}
	/>
	{#if loading}
		<div class="mt-4 text-gray-500">Loading...</div>
	{:else if errorMsg}
		<div class="mt-4 text-red-600">{errorMsg}</div>
	{/if}
</Card>
