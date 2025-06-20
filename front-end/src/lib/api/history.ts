import type { HistoryResponse } from '$lib/types';
import { API_URL } from './config';

export async function getHistoricalQueries(page = 1, page_size = 5): Promise<HistoryResponse> {
	const res = await fetch(`${API_URL}/api/v1/history?page=${page}&page_size=${page_size}`, {
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
