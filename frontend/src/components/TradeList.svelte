<script lang="ts">
	import { convertToReadableAmount, formatDate, getPctChange } from '../utils/lib';
	let { trades } = $props();

	const tableHeading =
		'col-span-1 text-center font-bold bg-slate-800 text-slate-200 rounded-xl mx-2 py-2';
</script>

<div class="flex h-full w-full flex-col items-center bg-inherit px-8 text-gray-800">
	<div class="grid w-full grid-cols-8 pb-20">
		<p class={tableHeading}>Stock</p>
		<p class={tableHeading}>Member</p>
		<p class={tableHeading}>Type</p>
		<p class={tableHeading}>Amount</p>
		<p class={tableHeading}>Date</p>
		<p class={tableHeading}>Traded By</p>
		<p class={tableHeading}>Performance</p>
		<p class={tableHeading}>More</p>

		{#each trades as trade}
			<div class="col-span-8 my-2 grid grid-cols-8 rounded-md bg-gray-200 py-3 shadow-md">
				<a
					href={`/stocks/${trade.stock__ticker}`}
					class="col-span-1 flex items-center justify-center text-center text-blue-600 hover:underline"
					>{trade.stock__ticker}</a
				>
				<a
					href={`/members/${trade.member__bio_guide_id}`}
					class="col-span-1 flex items-center justify-center text-center text-blue-600 hover:underline"
					>{trade.member__first_name} {trade.member__last_name} | {trade.member__party}</a
				>
				<p class="col-span-1 flex items-center justify-center text-center">
					{trade.type == 'b' ? 'Buy' : 'Sell'}
				</p>
				<p class="col-span-1 flex items-center justify-center text-center">
					~${trade.amount.toLocaleString()}
				</p>
				<p class="col-span-1 flex items-center justify-center text-center">
					{formatDate(trade.date)}
				</p>
				<p class="col-span-1 flex items-center justify-center text-center">{trade.traded_by}</p>
				<p
					class={`col-span-1 flex items-center justify-center rounded-lg text-center ${(getPctChange(trade.price_at_trade, trade.current_price) > 0 && trade.type == 'b') || (getPctChange(trade.price_at_trade, trade.current_price) < 0 && trade.type == 's') ? 'bg-green-500' : 'bg-red-500'}`}
				>
					{getPctChange(trade.price_at_trade, trade.current_price) > 0 ? '+' : ''}{getPctChange(
						trade.price_at_trade,
						trade.current_price
					).toFixed(1)}%
				</p>
				<a
					class="col-span-1 flex items-center justify-center text-center text-blue-600 hover:underline"
					href={`/trades/${trade.id}`}>More</a
				>
			</div>
		{/each}
	</div>
</div>
