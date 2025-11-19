import axios from 'axios';

export async function load({ params }: { params: any }) {
	const CONGRESS_KEY = 'Fi7HCmCMb9tmK780KedcRG0diNx4TT0z6YJxiyzv';
	const searchParams = { trade_id: params.id };
	const BASE_URL = import.meta.env.VITE_BACKEND_API_URL ?? 'https://api.congressstockwatch.com';
	try {
		const trade = await axios.get(`${BASE_URL}/trades`, {
			params: searchParams
		});
		const profileSearchParams = {
			ticker: trade.data.stock.ticker
		};
		const profile = await axios.get(`${BASE_URL}/stock/profile`, {
			params: profileSearchParams
		});
		const memberSearchParams = { api_key: CONGRESS_KEY };

		const member = await axios.get(
			`https://api.congress.gov/v3/member/${trade.data.member.bio_guide_id}`,
			{ params: memberSearchParams }
		);

		const stockData = await axios.get(`${BASE_URL}/stock/history`, {
			params: profileSearchParams
		});

		return {
			member: member.data.member,
			trade: trade.data,
			stock: profile.data,
			stockHistory: stockData.data.data
		};
	} catch (e) {
		console.log(e);
	}
}
