import axios from 'axios';

export async function load({ params }: { params: any }) {
	const BASE_URL = import.meta.env.VITE_BACKEND_API_URL ?? 'https://api.congressstockwatch.com';

	try {
		const trades = await axios.get(`${BASE_URL}/trades`);
		return {
			trades: trades.data.results
		};
	} catch (e) {
		console.log(e);
	}
}
