<script lang="ts">
	import '../app.css';
	let { children } = $props();
	let menuOpen = $state(false);
</script>

<div class="border-b-2 border-slate-900 bg-slate-800 text-slate-300 shadow-lg">
	<nav class="flex h-20 w-full items-center justify-between px-5">
		<a href="/" class="text-lg font-semibold">Home</a>

		<!-- Hamburger Button (Mobile Only) -->
		<button
			class="flex flex-col gap-1 md:hidden"
			onclick={() => (menuOpen = !menuOpen)}
			aria-label="Toggle menu"
		>
			<span class="h-0.5 w-6 bg-slate-300"></span>
			<span class="h-0.5 w-6 bg-slate-300"></span>
			<span class="h-0.5 w-6 bg-slate-300"></span>
		</button>

		<!-- Desktop Nav -->
		<div class="hidden gap-5 md:flex">
			<a href="/trades">Trades</a>
			<a href="/stocks">Stocks</a>
			<a href="/market">Market</a>
			<a href="/members">Members</a>
			<a href="/about">About</a>
		</div>
	</nav>

	<!-- Mobile Menu -->
	{#if menuOpen}
		<div
			class="flex flex-col gap-3 border-t border-slate-700 bg-slate-800 px-5 pb-4 text-slate-300 md:hidden"
		>
			<a
				href="/trades"
				onclick={() => {
					menuOpen = false;
				}}>Trades</a
			>
			<a
				href="/stocks"
				onclick={() => {
					menuOpen = false;
				}}>Stocks</a
			>
			<a
				href="/market"
				onclick={() => {
					menuOpen = false;
				}}>Market</a
			>
			<a
				href="/members"
				onclick={() => {
					menuOpen = false;
				}}>Members</a
			>
			<a
				href="/about"
				onclick={() => {
					menuOpen = false;
				}}>About</a
			>
		</div>
	{/if}
</div>
<main>
	{@render children()}
</main>

<style>
	main {
		min-height: 100%;
	}
</style>
