<script lang="ts">
	import * as d3 from 'd3';
	import { onMount, onDestroy } from 'svelte';

	export let dates: string[] = [];
	export let prices: number[] = [];
	export let tradeDate: string | null = null; // new prop

	let chartEl: HTMLDivElement;
	let resizeObserver: ResizeObserver;

	function drawChart() {
		if (!dates.length || !prices.length || !chartEl) return;

		// clear previous chart
		d3.select(chartEl).selectAll('*').remove();

		const data = dates.map((d, i) => ({
			x: new Date(d),
			y: prices[i]
		}));

		const margin = { top: 20, right: 30, bottom: 40, left: 60 };
		const width = chartEl.offsetWidth - margin.left - margin.right;
		const height = chartEl.offsetHeight - margin.top - margin.bottom;

		const svg = d3
			.select(chartEl)
			.append('svg')
			.attr('width', width + margin.left + margin.right)
			.attr('height', height + margin.top + margin.bottom)
			.append('g')
			.attr('transform', `translate(${margin.left},${margin.top})`);

		// scales
		const x = d3
			.scaleTime()
			.domain(d3.extent(data, (d) => d.x) as [Date, Date])
			.range([0, width]);

		const y = d3
			.scaleLinear()
			.domain([d3.min(data, (d) => d.y)! * 0.95, d3.max(data, (d) => d.y)! * 1.05])
			.nice()
			.range([height, 0]);

		// axes
		svg
			.append('g')
			.attr('transform', `translate(0,${height})`)
			.call(d3.axisBottom(x).tickFormat(d3.timeFormat('%b %d') as any));

		svg.append('g').call(d3.axisLeft(y));

		// line path
		svg
			.append('path')
			.datum(data)
			.attr('fill', 'none')
			.attr('stroke', 'steelblue')
			.attr('stroke-width', 1.5)
			.attr(
				'd',
				d3
					.line<{ x: Date; y: number }>()
					.x((d) => x(d.x))
					.y((d) => y(d.y))
			);

		// add vertical trade line if provided
		if (tradeDate) {
			const tradeX = new Date(tradeDate);
			if (!isNaN(tradeX.getTime())) {
				const lineX = x(tradeX);
				svg
					.append('line')
					.attr('x1', lineX)
					.attr('x2', lineX)
					.attr('y1', 0)
					.attr('y2', height)
					.attr('stroke', 'red')
					.attr('stroke-width', 2)
					.attr('stroke-dasharray', '4 2');
			}
		}

		// bisector for hover
		const bisect = d3.bisector<{ x: Date; y: number }, Date>((d) => d.x).left;

		// focus circle
		const focus = svg
			.append('g')
			.append('circle')
			.style('fill', 'none')
			.attr('stroke', 'black')
			.attr('r', 5)
			.style('opacity', 0);

		// focus text
		const focusText = svg
			.append('g')
			.append('text')
			.style('opacity', 0)
			.attr('text-anchor', 'end')
			.attr('alignment-baseline', 'middle');

		// overlay rect for hover
		svg
			.append('rect')
			.style('fill', 'none')
			.style('pointer-events', 'all')
			.attr('width', width)
			.attr('height', height)
			.on('mouseover', () => {
				focus.style('opacity', 1);
				focusText.style('opacity', 1);
			})
			.on('mouseout', () => {
				focus.style('opacity', 0);
				focusText.style('opacity', 0);
			})
			.on('mousemove', function (event) {
				const x0 = x.invert(d3.pointer(event, this)[0]);
				const i = bisect(data, x0, 1);
				const d0 = data[i - 1];
				const d1 = data[i] || d0;
				const d = x0.getTime() - d0.x.getTime() > d1.x.getTime() - x0.getTime() ? d1 : d0;

				focus.attr('cx', x(d.x)).attr('cy', y(d.y));

				const padding = 10;
				focusText
					.text(`${d3.timeFormat('%b %d, %Y')(d.x)} — $${d.y.toFixed(2)}`)
					.attr('x', width - padding)
					.attr('y', padding);
			});
	}

	onMount(() => {
		drawChart();
		resizeObserver = new ResizeObserver(() => {
			drawChart();
		});
		resizeObserver.observe(chartEl);
	});

	onDestroy(() => {
		if (resizeObserver) resizeObserver.disconnect();
	});
</script>

<div bind:this={chartEl} class="h-64 w-full rounded-lg bg-white shadow sm:h-80 md:h-96"></div>
