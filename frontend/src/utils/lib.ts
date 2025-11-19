export function formatDate(dateStr: string) {
	const date = new Date(dateStr);
	return date.toLocaleDateString('en-US', {
		year: 'numeric',
		month: 'short',
		day: 'numeric'
	});
}
export function convertToReadableAmount(number: number) {
	if (number >= 1_000) {
		// If the number is in billions
		return (number / 1_000).toFixed(1) + ' B';
	} else if (number >= 1) {
		// If the number is in millions
		return number.toFixed(1) + ' M';
	} else {
		// If the number is less than a million
		return number.toFixed(1) + ' M'; // Can adjust as needed
	}
}

export function getPctChange(start: number, end: number) {
	if (start == 0) {
		return 0;
	}
	return ((end - start) / end) * 100;
}
