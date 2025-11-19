<script lang="ts">
	import type { CompanyInfo, CompanyNews } from '../../../types/types';
	import StockProfile from '../../../components/StockProfile.svelte';
	import StockChart from '../../../components/StockChart.svelte';

	export let data;
	const { company, news, stockHistory } = data;

	function convertToReadableAmount(number: number) {
		if (number >= 1_000_000) {
			return (number / 1_000_000).toFixed(1) + ' T';
		} else if (number >= 1_000) {
			return (number / 1_000).toFixed(1) + ' B';
		} else if (number >= 1) {
			return number.toFixed(1) + ' M';
		} else {
			return number.toFixed(1) + ' M';
		}
	}
</script>

<div class="flex w-full flex-col items-center justify-center bg-gray-100">
	<!-- Profile + Chart -->
	<div class="flex w-full flex-col gap-4 p-4 md:flex-row md:justify-evenly">
		<div class="w-full md:w-[35%]">
			<StockProfile {company} />
		</div>
		<div class="w-full rounded-2xl bg-white p-6 shadow-lg md:w-[60%]">
			<h1 class="mb-3 text-center font-bold">6 month performance</h1>
			<StockChart dates={stockHistory.dates} prices={stockHistory.prices} />
		</div>
	</div>

	<!-- News -->
	<h1 class="py-5 text-center text-2xl font-extrabold md:text-3xl">Recent News</h1>
	<div class="grid w-full gap-5 p-4 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 2xl:grid-cols-5">
		{#each news as article}
			<div class="rounded-2xl bg-white p-4 shadow-lg">
				<a href={article.url} target="_blank" class="block">
					<h2 class="text-lg font-bold text-blue-600">{article.headline}</h2>
				</a>
				<p class="text-sm text-gray-500">
					{new Date(article.datetime * 1000).toLocaleDateString()}
				</p>
				<p class="mt-2 line-clamp-4 text-gray-700">{article.summary}</p>
				{#if article.image}
					<div class="mt-4">
						<img src={article.image} alt="News" class="h-auto w-full rounded-md object-cover" />
					</div>
				{/if}
				<p class="mt-2 text-sm text-gray-600">Source: {article.source}</p>
			</div>
		{/each}
	</div>
</div>
