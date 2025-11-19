<script lang="ts">
	import TradeList from '../../components/TradeList.svelte';
	import MobileTradeList from '../../components/MobileTradeList.svelte';
	const tableHeading = 'col-span-1 text-center font-bold bg-green-500 rounded-xl mx-2 py-2';
	export let data: any;
	const trades = data.trades;
</script>

<div class="flex w-full flex-col items-center bg-gray-100 px-4 pb-10 text-gray-800 sm:px-8">
	<h1 class="mb-6 mt-8 text-3xl font-bold">Flagged Trades</h1>

	<div class="py-5 text-sm sm:text-base">
		<p>
			This system detects potential insider trading by analyzing the GICS sector of stocks traded by
			members of Congress and comparing them to the committees they serve on. Congressional
			committees oversee specific industries, giving members access to non-public information that
			could influence stock prices. If a lawmaker trades a stock in a sector that falls under their
			committee’s jurisdiction, the trade is flagged as a potential conflict of interest. This
			allows for greater transparency and helps identify trades that may warrant further scrutiny.
		</p>
		<br />
		<p>
			Members of Congress have access to sensitive information through their committee work,
			including upcoming regulations, industry developments, and government contracts. This
			privileged access creates opportunities for insider trading, where lawmakers could use
			non-public knowledge to make profitable trades before the information becomes public. By
			monitoring these trades, this system helps highlight patterns and potential ethical concerns
			in congressional stock activity.
		</p>
	</div>

	<!-- Desktop / Tablet -->
	<div class="hidden w-full md:block">
		<TradeList {trades} />
	</div>

	<!-- Mobile -->
	<div class="block w-full md:hidden">
		<MobileTradeList {trades} />
	</div>
</div>
