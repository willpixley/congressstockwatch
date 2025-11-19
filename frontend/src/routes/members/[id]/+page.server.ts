import axios from 'axios';

export async function load({ params }: { params: any }) {
	const searchParams = { id: params.id };
	const BASE_URL = import.meta.env.VITE_BACKEND_API_URL ?? 'https://api.congressstockwatch.com';
	const CONGRESS_KEY = 'Fi7HCmCMb9tmK780KedcRG0diNx4TT0z6YJxiyzv';

	try {
		const trades = await axios.get(`${BASE_URL}/trades/member`, {
			params: searchParams
		});

		const memberSearchParams = { api_key: CONGRESS_KEY };

		const member = await axios.get(`https://api.congress.gov/v3/member/${params.id}`, {
			params: memberSearchParams
		});

		return {
			member: member.data.member,
			trades: trades.data.trades,
			history: trades.data.history
		};
	} catch (e) {
		console.log(e);
	}
}
