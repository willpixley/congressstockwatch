<script lang="ts">
	import { formatDate } from '../utils/lib';
	import TradeList from '../components/TradeList.svelte';
	import MobileTradeList from '../components/MobileTradeList.svelte';
	export let data: any;
	const trades = data.trades;
</script>

<div class="flex w-full flex-col justify-center bg-gray-100 px-4 sm:px-8">
	<h1 class="mb-8 mt-8 text-center text-3xl font-bold">Recent Trades</h1>

	<!-- Desktop / Tablet -->
	<div class="hidden md:block">
		<TradeList {trades} />
	</div>

	<!-- Mobile -->
	<div class="block md:hidden">
		<MobileTradeList {trades} />
	</div>
</div>
