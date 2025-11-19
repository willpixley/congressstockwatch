<script lang="ts">
	import { formatDate } from '../../utils/lib';
	export let data: any;
	const { trends } = data;
</script>

<div class="flex min-h-full w-full flex-col items-center gap-8 bg-gray-300">
	<h1 class="mb-1 mt-6 text-2xl font-bold">Recent Trends</h1>
	<div
		class="grid w-[80%] grid-cols-2 gap-3 rounded-md bg-gray-100 p-3 shadow-md sm:grid-cols-2 md:grid-cols-2 lg:grid-cols-5"
	>
		<div class="col-span-1 flex flex-col items-center justify-center">
			<p class=" text-center font-bold">Past Month</p>
			<p class="text-center">{formatDate(trends.since)}</p>
		</div>
		<div class="col-span-1 flex flex-col items-center justify-center">
			<p class=" text-center font-bold">Volume Bought</p>
			<p class="text-center">~${trends.volume_bought.toLocaleString()}</p>
		</div>
		<div class="col-span-1 flex flex-col items-center justify-center">
			<p class="text-center font-bold">Volume Sold</p>
			<p class="text-center">~${trends.volume_sold.toLocaleString()}</p>
		</div>
		<div class="col-span-1 flex flex-col items-center justify-center">
			<p class="text-center font-bold">Most Bought Sector</p>
			<p class="text-center">{trends.max_sector_bought.sector_name}</p>
		</div>
		<div class="col-span-1 flex flex-col items-center justify-center">
			<p class="text-center font-bold">Most Sold Sector</p>
			<p class="text-center">{trends.max_sector_sold.sector_name}</p>
		</div>
	</div>
</div>
