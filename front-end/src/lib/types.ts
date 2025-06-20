// Interfaces for API
export interface DistanceRequest {
	address1: string;
	address2: string;
}
export interface Address {
	latitude: number;
	longitude: number;
	address: string;
}
export interface DistanceResponse {
	kilometers: number;
	miles: number;
	address1: Address;
	address2: Address;
	query_id: string;
}

export interface Query {
	query_id: string;
	kilometers: number | null;
	miles: number | null;
	address1: string;
	address2: string;
	timestamp: string;
}
export interface HistoryResponse {
	items: Query[];
	pagination: Pagination;
}

export interface Pagination {
	total: number;
	page: number;
	page_size: number;
	total_pages: number;
}

export enum DistanceType {
	Miles = 'miles',
	Kilometers = 'kilometers',
	All = 'all'
}
