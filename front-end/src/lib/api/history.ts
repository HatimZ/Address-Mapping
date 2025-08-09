import type { HistoryResponse } from '$lib/types';
import { PUBLIC_API_BASE_URL } from '$env/static/public';

export async function getHistoricalQueries(page = 1, page_size = 5): Promise<HistoryResponse> {
	const res = await fetch(`${PUBLIC_API_BASE_URL}/history?page=${page}&page_size=${page_size}`, {
		method: 'GET',
		headers: {
			Accept: 'application/json',
			'Content-Type': 'application/json'
		}
	});

	if (!res.ok) {
		throw new Error('Failed to fetch history.');
	}
	return await res.json();
}
