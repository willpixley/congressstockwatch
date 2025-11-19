<script lang="ts">
	import { formatDate, getPctChange } from '../../../utils/lib';
	export let data: any;
	const { trades, member, history } = data;
</script>

<div class="w-full bg-gray-100 px-4 sm:px-8">
	<!-- Member + Stats -->
	<div
		class="my-8 flex flex-col gap-4 rounded-2xl bg-white p-4 shadow-lg md:flex-row md:items-stretch md:justify-between md:p-6"
	>
		<!-- Member Info -->
		<div class="flex flex-1 flex-col items-center rounded-md border-2 border-gray-100 p-4">
			<div class="relative h-32 w-32 overflow-hidden rounded-full">
				<img
					src={member.depiction.imageUrl}
					alt={member.directOrderName}
					class="h-full w-full object-cover object-top"
				/>
			</div>
			<p class="mt-2 text-center text-xl font-bold">{member.directOrderName}</p>
			<p class="text-center font-semibold text-gray-500">
				{member.partyHistory.at(-1).partyAbbreviation} | {member.state}
			</p>
		</div>

		<!-- Stats Cards -->
		<div class="grid w-full grid-cols-2 gap-4 md:flex md:flex-1 md:gap-5">
			{#each [{ label: 'Total Trade Volume', value: `~${history.volume.toLocaleString()}` }, { label: 'Purchases', value: history.purchases }, { label: 'Sales', value: history.sales }, { label: 'Weighted Returns', value: `${Number(history.weighted_return).toFixed(2)}%` }, { label: 'Weighted Returns (Flagged)', value: Number(history.weighted_flagged_return) === 0 ? 'N/A' : `${Number(history.weighted_flagged_return).toFixed(2)}%` }] as stat}
				<div
					class="flex flex-1 flex-col items-center justify-center gap-2 rounded-md border-2 border-gray-100 bg-gray-50 p-3"
				>
					<p class="text-center text-sm font-bold sm:text-base">{stat.label}</p>
					<p class="text-center text-sm sm:text-base">{stat.value}</p>
				</div>
			{/each}
		</div>
	</div>

	<!-- Trades Section -->
	{#if trades?.length}
		<div class="flex w-full flex-col items-center pb-10 text-gray-800">
			<h1 class="mb-4 text-center text-3xl font-bold">All Trades</h1>

			<!-- Mobile Card Layout -->
			<div class="flex w-full flex-col gap-3 md:hidden">
				{#each trades as trade}
					<div
						class={`flex flex-col rounded-lg  p-4 shadow-md ${trade.flagged ? 'bg-red-300' : 'bg-gray-200'}`}
					>
						<div class="mb-2 flex items-center justify-between">
							<a
								href={`/stocks/${trade.stock.ticker}`}
								class="font-bold text-blue-600 hover:underline">{trade.stock.ticker}</a
							>

							<p
								class={`rounded-lg px-2 py-1 text-sm text-white ${(getPctChange(trade.price_at_trade, trade.current_price) > 0 && trade.type == 'b') || (getPctChange(trade.price_at_trade, trade.current_price) < 0 && trade.type == 's') ? 'bg-green-500' : 'bg-red-500'}`}
							>
								{getPctChange(trade.price_at_trade, trade.current_price) > 0
									? '+'
									: ''}{getPctChange(trade.price_at_trade, trade.current_price).toFixed(1)}%
							</p>
						</div>
						<p><span class="font-semibold">Type:</span> {trade.type == 'b' ? 'Buy' : 'Sell'}</p>
						<p><span class="font-semibold">Amount:</span> ~${trade.amount.toLocaleString()}</p>
						<p><span class="font-semibold">Date:</span> {formatDate(trade.date)}</p>
						<p><span class="font-semibold">Traded By:</span> {trade.traded_by}</p>
						<a href={`/trades/${trade.id}`} class="mt-2 text-center text-blue-600 hover:underline"
							>More</a
						>
					</div>
				{/each}
			</div>

			<!-- Desktop Grid Layout -->
			<div class="hidden w-full grid-cols-7 gap-2 pb-10 md:grid">
				<p class="rounded-xl bg-slate-800 py-2 text-center font-bold text-slate-200">Stock</p>
				<p class="rounded-xl bg-slate-800 py-2 text-center font-bold text-slate-200">Type</p>
				<p class="rounded-xl bg-slate-800 py-2 text-center font-bold text-slate-200">Amount</p>
				<p class="rounded-xl bg-slate-800 py-2 text-center font-bold text-slate-200">Date</p>
				<p class="rounded-xl bg-slate-800 py-2 text-center font-bold text-slate-200">Traded By</p>
				<p class="rounded-xl bg-slate-800 py-2 text-center font-bold text-slate-200">Performance</p>
				<p class="rounded-xl bg-slate-800 py-2 text-center font-bold text-slate-200">More</p>

				{#each trades as trade}
					<div
						class="col-span-7 grid grid-cols-7 items-center justify-center rounded-md bg-gray-200 py-3 shadow-md"
					>
						<a
							href={`/stocks/${trade.stock.ticker}`}
							class={`col-span-1 text-center text-blue-600 hover:underline ${trade.flagged ? 'mx-2 bg-red-400' : ''}`}
							>{trade.stock.ticker}</a
						>
						<p class="col-span-1 text-center">{trade.type == 'b' ? 'Buy' : 'Sell'}</p>
						<p class="col-span-1 text-center">~${trade.amount.toLocaleString()}</p>
						<p class="col-span-1 text-center">{formatDate(trade.date)}</p>
						<p class="col-span-1 text-center">{trade.traded_by}</p>
						<p
							class={`col-span-1 rounded-lg text-center ${(getPctChange(trade.price_at_trade, trade.current_price) > 0 && trade.type == 'b') || (getPctChange(trade.price_at_trade, trade.current_price) < 0 && trade.type == 's') ? 'bg-green-500' : 'bg-red-500'}`}
						>
							{getPctChange(trade.price_at_trade, trade.current_price) > 0 ? '+' : ''}{getPctChange(
								trade.price_at_trade,
								trade.current_price
							).toFixed(1)}%
						</p>
						<a
							class="col-span-1 text-center text-blue-600 hover:underline"
							href={`/trades/${trade.id}`}>More</a
						>
					</div>
				{/each}
			</div>
		</div>
	{:else}
		<p class="mt-4 text-center">No trades on file for this member</p>
	{/if}
</div>
