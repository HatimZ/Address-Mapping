import type { DistanceRequest, DistanceResponse } from '$lib/types';
import { API_URL } from './config';

// Define a type for the detail error array
interface DetailError {
	msg: string;
}

export async function calculateDistance(
	body: DistanceRequest
): Promise<DistanceResponse | { errors: string[] }> {
	const res = await fetch(`${API_URL}/api/v1/distance/calculate`, {
		method: 'POST',
		headers: { 'Content-Type': 'application/json' },
		body: JSON.stringify(body)
	});
	const data = await res.json();
	if (!res.ok) {
		if (data.errors) return { errors: data.errors };
		if (data.detail) return { errors: data.detail.map((d: DetailError) => d.msg) };
		throw new Error('Failed to calculate distance.');
	}
	return data;
}
