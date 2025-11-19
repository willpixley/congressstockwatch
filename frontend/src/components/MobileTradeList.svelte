<script lang="ts">
	import { formatDate, getPctChange } from '../utils/lib';
	let { trades } = $props();
</script>

<div class="flex w-full flex-col space-y-4 px-4 sm:px-8">
	{#each trades as trade}
		<div class="flex flex-col rounded-lg bg-gray-200 p-4 shadow-md">
			<div class="mb-2 flex items-center justify-between">
				<a
					href={`/stocks/${trade.stock__ticker}`}
					class="text-lg font-bold text-blue-600 hover:underline">{trade.stock__ticker}</a
				>
				<a
					href={`/members/${trade.member__bio_guide_id}`}
					class="text-sm text-blue-600 hover:underline"
					>{trade.member__first_name} {trade.member__last_name} | {trade.member__party}</a
				>
			</div>

			<div class="grid grid-cols-2 gap-2 text-sm">
				<p><span class="font-semibold">Type:</span> {trade.type == 'b' ? 'Buy' : 'Sell'}</p>
				<p><span class="font-semibold">Amount:</span> ~${trade.amount.toLocaleString()}</p>
				<p><span class="font-semibold">Date:</span> {formatDate(trade.date)}</p>
				<p><span class="font-semibold">Traded By:</span> {trade.traded_by}</p>
				<p class="col-span-2">
					<span class="font-semibold">Performance:</span>
					<span
						class={`rounded-lg px-2 py-1 text-white ${
							(getPctChange(trade.price_at_trade, trade.current_price) > 0 && trade.type == 'b') ||
							(getPctChange(trade.price_at_trade, trade.current_price) < 0 && trade.type == 's')
								? 'bg-green-500'
								: 'bg-red-500'
						}`}
					>
						{getPctChange(trade.price_at_trade, trade.current_price) > 0 ? '+' : ''}{getPctChange(
							trade.price_at_trade,
							trade.current_price
						).toFixed(1)}%
					</span>
				</p>
				<a
					href={`/trades/${trade.id}`}
					class="col-span-2 mt-2 text-center text-blue-600 hover:underline">More Details</a
				>
			</div>
		</div>
	{/each}
</div>
