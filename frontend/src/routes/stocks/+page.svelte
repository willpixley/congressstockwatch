<script lang="ts">
	import axios from 'axios';
	interface StockResponse {
		ticker: string;
		name: string;
		sector: number;
	}
	const BASE_URL = import.meta.env.VITE_BACKEND_API_URL ?? 'https://api.congressstockwatch.com';

	let results = $state<StockResponse[]>([]);
	let loading = $state(false);
	let query = $state('');

	async function searchStocks() {
		query = query.trim();
		if (query != '') {
			loading = true;
			const response = await axios.get(`${BASE_URL}/stock`, {
				params: { search: query }
			});
			results = response.data.data;
			loading = false;
		}
	}

	function handleKeyDown(event: any) {
		if (event.key === 'Enter') searchStocks();
	}
</script>

<main class="flex min-h-screen flex-col items-center bg-gray-100 p-4 sm:p-6">
	<h1 class="mb-6 text-center text-3xl font-bold text-gray-800">Search Page</h1>

	<!-- Search Form -->
	<div class="flex w-full max-w-lg flex-col gap-3 sm:flex-row">
		<input
			type="text"
			placeholder="Search by company name"
			onkeydown={handleKeyDown}
			bind:value={query}
			class="w-full rounded-md border border-gray-300 p-3 text-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
		/>

		<button
			class="w-full rounded-md bg-blue-500 p-3 text-white hover:bg-blue-600 focus:outline-none focus:ring-2 focus:ring-blue-500 sm:w-auto"
			onclick={searchStocks}
		>
			Search
		</button>
	</div>

	<!-- Loading Indicator -->
	{#if loading}
		<p class="mt-4 text-gray-500">Loading...</p>
	{/if}

	<!-- Results -->
	{#if results.length > 0}
		<div class="mt-6 grid w-full max-w-3xl gap-4 px-2 sm:grid-cols-1 md:grid-cols-2 lg:grid-cols-3">
			{#each results as result}
				<a href={`/stocks/${result.ticker}`} class="flex w-full">
					<div
						class="flex w-full flex-col justify-center gap-1 rounded-lg bg-white p-4 shadow transition-shadow hover:shadow-md"
					>
						<p class="text-lg font-bold">{result.ticker}</p>
						<p class="text-gray-700">{result.name}</p>
					</div>
				</a>
			{/each}
		</div>
	{/if}
</main>

<style>
	main {
		min-height: 100%;
	}
</style>
