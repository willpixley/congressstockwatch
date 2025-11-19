export type CongressMember = {
	bioGuideId: string;
	firstName: string;
	lastName: string;
	chamber: string;
	party: string;
	state: string;
	term: number;
};
export type Sector = {
	sectorCode: string;
	sectorName: string;
	description: string;
};
export type Stock = {
	ticker: string;
	sector: Sector;
	name: string;
};
export type Trade = {
	id: number;
	type: string;
	stock: Stock;
	date: Date;
	amount: number;
	member: CongressMember;
	tradedBy: string;
};

export type CompanyInfo = {
	country: string;
	currency: string;
	estimateCurrency: string;
	exchange: string;
	finnhubIndustry: string;
	ipo: string; // ISO 8601 date string (YYYY-MM-DD)
	logo: string; // URL string
	marketCapitalization: number;
	name: string;
	phone: string;
	shareOutstanding: number;
	ticker: string;
	weburl: string; // URL string
};

export type CompanyNews = {
	category: string;
	datetime: number;
	headline: string;
	id: number;
	image: string;
	related: string;
	source: string;
	summary: string;
	url: string;
};

export const testTrades: Trade[] = [
	{
		id: 1,
		type: 'Buy',
		stock: {
			ticker: 'AAPL',
			name: 'Apple Inc.',
			sector: { sectorCode: 'TECH', sectorName: 'Technology', description: 'Tech sector' }
		},
		date: new Date('2024-02-01'),
		amount: 50000,
		member: {
			bioGuideId: 'A123',
			firstName: 'John',
			lastName: 'Doe',
			chamber: 'House',
			party: 'Independent',
			state: 'CA',
			term: 3
		},
		tradedBy: 'Self'
	},
	{
		id: 2,
		type: 'Sell',
		stock: {
			ticker: 'TSLA',
			name: 'Tesla Inc.',
			sector: { sectorCode: 'AUTO', sectorName: 'Automotive', description: 'Automobile sector' }
		},
		date: new Date('2024-01-15'),
		amount: 75000,
		member: {
			bioGuideId: 'B456',
			firstName: 'Jane',
			lastName: 'Smith',
			chamber: 'Senate',
			party: 'Democrat',
			state: 'NY',
			term: 2
		},
		tradedBy: 'Spouse'
	},
	{
		id: 3,
		type: 'Buy',
		stock: {
			ticker: 'GOOGL',
			name: 'Alphabet Inc.',
			sector: { sectorCode: 'TECH', sectorName: 'Technology', description: 'Tech sector' }
		},
		date: new Date('2023-12-20'),
		amount: 100000,
		member: {
			bioGuideId: 'C789',
			firstName: 'Robert',
			lastName: 'Johnson',
			chamber: 'House',
			party: 'Republican',
			state: 'TX',
			term: 4
		},
		tradedBy: 'Child'
	},
	{
		id: 4,
		type: 'Buy',
		stock: {
			ticker: 'AMZN',
			name: 'Amazon Inc.',
			sector: {
				sectorCode: 'TECH',
				sectorName: 'Technology',
				description: 'E-commerce and cloud computing'
			}
		},
		date: new Date('2024-02-05'),
		amount: 60000,
		member: {
			bioGuideId: 'D101',
			firstName: 'Emily',
			lastName: 'Brown',
			chamber: 'Senate',
			party: 'Democrat',
			state: 'WA',
			term: 1
		},
		tradedBy: 'Self'
	},
	{
		id: 5,
		type: 'Sell',
		stock: {
			ticker: 'NFLX',
			name: 'Netflix Inc.',
			sector: {
				sectorCode: 'MEDIA',
				sectorName: 'Media',
				description: 'Streaming and entertainment'
			}
		},
		date: new Date('2024-02-10'),
		amount: 90000,
		member: {
			bioGuideId: 'E202',
			firstName: 'Michael',
			lastName: 'Green',
			chamber: 'House',
			party: 'Republican',
			state: 'FL',
			term: 2
		},
		tradedBy: 'Spouse'
	},
	{
		id: 6,
		type: 'Buy',
		stock: {
			ticker: 'MSFT',
			name: 'Microsoft Corp.',
			sector: { sectorCode: 'TECH', sectorName: 'Technology', description: 'Software and hardware' }
		},
		date: new Date('2024-01-20'),
		amount: 120000,
		member: {
			bioGuideId: 'F303',
			firstName: 'Laura',
			lastName: 'White',
			chamber: 'Senate',
			party: 'Independent',
			state: 'CO',
			term: 3
		},
		tradedBy: 'Self'
	},
	{
		id: 7,
		type: 'Sell',
		stock: {
			ticker: 'JPM',
			name: 'JPMorgan Chase & Co.',
			sector: { sectorCode: 'FIN', sectorName: 'Finance', description: 'Banking and investment' }
		},
		date: new Date('2023-11-15'),
		amount: 50000,
		member: {
			bioGuideId: 'G404',
			firstName: 'David',
			lastName: 'Clark',
			chamber: 'House',
			party: 'Democrat',
			state: 'IL',
			term: 4
		},
		tradedBy: 'Child'
	},
	{
		id: 8,
		type: 'Buy',
		stock: {
			ticker: 'XOM',
			name: 'ExxonMobil',
			sector: { sectorCode: 'ENG', sectorName: 'Energy', description: 'Oil and gas' }
		},
		date: new Date('2024-02-08'),
		amount: 70000,
		member: {
			bioGuideId: 'H505',
			firstName: 'Sophia',
			lastName: 'Davis',
			chamber: 'Senate',
			party: 'Republican',
			state: 'TX',
			term: 5
		},
		tradedBy: 'Spouse'
	},
	{
		id: 9,
		type: 'Sell',
		stock: {
			ticker: 'V',
			name: 'Visa Inc.',
			sector: { sectorCode: 'FIN', sectorName: 'Finance', description: 'Payment processing' }
		},
		date: new Date('2024-01-30'),
		amount: 80000,
		member: {
			bioGuideId: 'I606',
			firstName: 'Daniel',
			lastName: 'Martinez',
			chamber: 'House',
			party: 'Independent',
			state: 'NV',
			term: 2
		},
		tradedBy: 'Self'
	},
	{
		id: 10,
		type: 'Buy',
		stock: {
			ticker: 'BA',
			name: 'Boeing Co.',
			sector: { sectorCode: 'AERO', sectorName: 'Aerospace', description: 'Aircraft manufacturing' }
		},
		date: new Date('2023-12-10'),
		amount: 110000,
		member: {
			bioGuideId: 'J707',
			firstName: 'Olivia',
			lastName: 'Wilson',
			chamber: 'Senate',
			party: 'Democrat',
			state: 'WA',
			term: 1
		},
		tradedBy: 'Child'
	}
];
