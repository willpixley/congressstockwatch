<script lang="ts">
	import { convertToReadableAmount, formatDate } from '../utils/lib';
	let { company } = $props();
</script>

<div class="h-full w-full rounded-2xl bg-white p-6 shadow-lg">
	<div class="flex justify-center">
		<img src={company.logo} alt={company.name} class="h-20 w-20 rounded-md object-contain" />
	</div>
	<h2 class="mt-4 text-center text-2xl font-bold">{company.name}</h2>
	<p class="text-center text-gray-500">{company.ticker} - {company.exchange}</p>
	<div class="mt-4 space-y-2">
		<p><strong>Industry:</strong> {company.finnhubIndustry}</p>
		<p>
			<strong>Market Cap:</strong>
			{company.marketCapitalization && convertToReadableAmount(company.marketCapitalization)}
		</p>
		<p><strong>IPO Date:</strong> {formatDate(company.ipo)}</p>
		<p><strong>Country:</strong> {company.country}</p>
		<p><strong>Currency:</strong> {company.currency}</p>
		<p>
			<strong>Shares Outstanding:</strong>
			{company.shareOutstanding && convertToReadableAmount(company.shareOutstanding)}
		</p>
	</div>
	<div class="mt-4 text-center">
		<a href={company.weburl} target="_blank" class="text-blue-500 hover:underline">Visit Website</a>
	</div>
</div>
