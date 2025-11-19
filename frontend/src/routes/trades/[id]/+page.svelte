<script lang="ts">
	import StockChart from '../../../components/StockChart.svelte';
	import StockProfile from '../../../components/StockProfile.svelte';
	import { formatDate } from '../../../utils/lib';
	let regionNames = new Intl.DisplayNames(['en'], { type: 'region' });

	export let data: any;
	const { trade, stock, member, stockHistory } = data;
</script>

<div
	class="flex min-h-screen flex-col gap-6 bg-gray-100 p-4 md:flex-row md:items-start md:justify-center"
>
	<!-- Member + Trade Info -->
	<div class="flex w-full flex-col gap-6 rounded-2xl bg-white p-4 shadow-lg md:w-[65%] md:flex-row">
		<!-- Member Info -->
		<div class="flex flex-col items-center gap-4 rounded-md border-2 border-gray-100 p-4 md:w-1/3">
			<div class="relative h-32 w-32 overflow-hidden rounded-full">
				<img
					src={member.depiction.imageUrl}
					alt={member.directOrderName}
					class="h-full w-full object-cover object-top"
				/>
			</div>
			<div>
				<p class="text-center text-xl font-bold">{member.directOrderName}</p>
				<p class="text-md text-center font-semibold text-gray-500">
					{trade.member.party} | {member.state}
				</p>
			</div>
		</div>

		<!-- Trade Info Grid -->
		<div
			class="grid w-full grid-cols-1 gap-4 rounded-md border-2 border-gray-100 p-4 sm:grid-cols-2 md:grid-cols-4 md:grid-rows-2"
		>
			<div class="flex flex-col items-center gap-1">
				<p class="text-center font-bold">Ticker</p>
				<a href={`/stocks/${trade.stock.ticker}`} class="text-center text-blue-500 underline"
					>{trade.stock.ticker}</a
				>
			</div>
			<div class="flex flex-col items-center gap-1">
				<p class="text-center font-bold">Sector</p>
				<p class="text-center">{trade.sector.sector_name}</p>
			</div>
			<div class="flex flex-col items-center gap-1">
				<p class="text-center font-bold">Type</p>
				<p class="text-center">{trade.type == 'B' ? 'Buy' : 'Sell'}</p>
			</div>
			<div class="flex flex-col items-center gap-1">
				<p class="text-center font-bold">Amount</p>
				<p class="text-center">${trade.amount.toLocaleString()}</p>
			</div>
			<div class="flex flex-col items-center gap-1">
				<p class="text-center font-bold">Bought At</p>
				<p class="text-center">${trade.price_at_trade.toLocaleString()}</p>
			</div>
			<div class="relative flex flex-col items-center gap-1">
				<p class="text-center font-bold">Current Price</p>
				<p class="text-center">${trade.current_price.toLocaleString()}</p>
				<p class=" top-0 pt-1 text-center text-xs italic text-gray-600">
					{`Updated on ${formatDate(trade.updated_at)}`}
				</p>
			</div>
			<div class="flex flex-col items-center gap-1">
				<p class="text-center font-bold">Date</p>
				<p class="text-center">{formatDate(trade.date)}</p>
			</div>
			<div class="flex flex-col items-center gap-1">
				<p class="text-center font-bold">Traded By</p>
				<p class="text-center">{trade.traded_by}</p>
			</div>
		</div>
	</div>
	<div class="flex w-full flex-col gap-6 rounded-2xl bg-white p-4 shadow-lg md:w-[65%]">
		<h1 class="text-center font-bold">Past 6 months</h1>
		<StockChart dates={stockHistory.dates} prices={stockHistory.prices} tradeDate={trade.date} />
	</div>
</div>
