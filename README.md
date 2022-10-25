# Milwaukee OpenData Call Center Records

Processes the combined [historical call center records](https://data.milwaukee.gov/dataset/callcenterdatahistorical)
and [current call center records](https://data.milwaukee.gov/dataset/callcenterdatacurrent) from the Milwaukee OpenData portal. Current records were downloaded on October 5, 2022.

Attempts to parse the ZIP Code from each record. When the ZIP code is missing, uses the [ZIP Code Lookup API](https://www.usps.com/business/web-tools-apis/address-information-api.htm#_Toc110511817) provided by the United States Postal Service to retrieve the ZIP code using the street address information.

If the ZIP code can be determined, writes the complete record to a tab-delimited output file. Otherwise, skips the line.

## Usage instructions
Register for a free account at [USPS Web Tools](https://registration.shippingapis.com/). You will receive a confirmation email containing your username and password. 

Run `main.py USERNAME` where *USERNAME* is the account name provided in the registration confirmation email. The password is not necessary.

## Dependencies
- requests 2.28.1

## Input data
Input data (MKE-Call-Center-10-5-22.tsv) is tab-delimited, with the following columns:

- address
- creation.date
- closed.date
- title
- closure.reason

A smaller file of curated sample lines (test-data.tsv) can be used to test the algorithm.

### Sample input data

<pre>
2162 N 46TH ST, MILWAUKEE, WI, 53208-1227	2022-08-23T00:00:00Z		Scattered debris	Scattered Litter and Debris on Private Property
2806 N 28TH ST, MILWAUKEE, WI, 53210-2004	2022-08-23T00:00:00Z		Large scattered debris	Large Items Discarded on Private Property
2805 N 27TH ST, MILWAUKEE, WI, 53210-2002	2022-08-23T00:00:00Z		Scattered debris	Scattered Litter and Debris on Private Property
7988 N 94TH ST, MILWAUKEE, WI, 00000-0000	2022-08-07T00:00:00Z	2022-08-08T00:00:00Z	City TD blocking road.	City Tree Down
1552 N 52ND ST	2022-08-08T00:00:00Z		Tree brush	Brush Pickup Request, Less than 2 Cubic Yards, April-November
3250 N 22ND ST	2022-08-08T00:00:00Z		Items are placed along side of garbage cart	Sanitation Inspector Notification and Bulky Item Pickup Request
2028 N BOOTH ST, MILWAUKEE, WI, 532123404	2020-04-28T00:00:00Z	2020-05-01T00:00:00Z	Dead squirrel	Dead Animal
3248 N CAMBRIDGE AV, MILWAUKEE, WI, 532113026	2020-04-28T00:00:00Z		West side of street.	Street Light Out
338 E EUCLID AV, MILWAUKEE, WI, 532072650	2020-04-27T00:00:00Z			Pothole
2926 W LISBON AV, MILWAUKEE, WI, 53208	2020-04-30T00:00:00Z	2020-05-05T00:00:00Z	Abandoned Boat left in the alley in the rear of location, next to the alley.	Large Items Discarded on Private Property
	2020-05-18T00:00:00Z	2020-05-18T00:00:00Z		DNS - No Contact Info X2268 Internal Transfer
	2020-05-18T00:00:00Z	2020-05-18T00:00:00Z		DNS X2268 Internal Transfer
	2020-05-18T00:00:00Z	2020-05-18T00:00:00Z		Police Internal Transfer
	2020-05-18T00:00:00Z	2020-05-18T00:00:00Z		Mayor's Office X2200 Internal Transfer
</pre>


## Output data
Output data (out.tsv) is tab-delimited, with the following columns. The file does not include a header line.

- line.number
- zip.code
- address
- creation.date
- closed.date
- title
- closure.reason

### Sample output data

<pre>
1	53208	2162 N 46TH ST, MILWAUKEE, WI, 53208-1227	2022-08-23T00:00:00Z		Scattered debris	Scattered Litter and Debris on Private Property
2	53210	2806 N 28TH ST, MILWAUKEE, WI, 53210-2004	2022-08-23T00:00:00Z		Large scattered debris	Large Items Discarded on Private Property
3	53210	2805 N 27TH ST, MILWAUKEE, WI, 53210-2002	2022-08-23T00:00:00Z		Scattered debris	Scattered Litter and Debris on Private Property
4	53224	7988 N 94TH ST, MILWAUKEE, WI, 00000-0000	2022-08-07T00:00:00Z	2022-08-08T00:00:00Z	City TD blocking road.	City Tree Down
5	53208	1552 N 52ND ST	2022-08-08T00:00:00Z		Tree brush	Brush Pickup Request, Less than 2 Cubic Yards, April-November
6	53206	3250 N 22ND ST	2022-08-08T00:00:00Z		Items are placed along side of garbage cart	Sanitation Inspector Notification and Bulky Item Pickup Request
7	53212	2028 N BOOTH ST, MILWAUKEE, WI, 532123404	2020-04-28T00:00:00Z	2020-05-01T00:00:00Z	Dead squirrel	Dead Animal
8	53211	3248 N CAMBRIDGE AV, MILWAUKEE, WI, 532113026	2020-04-28T00:00:00Z		West side of street.	Street Light Out
9	53207	338 E EUCLID AV, MILWAUKEE, WI, 532072650	2020-04-27T00:00:00Z			Pothole
10	53208	2926 W LISBON AV, MILWAUKEE, WI, 53208	2020-04-30T00:00:00Z	2020-05-05T00:00:00Z	Abandoned Boat left in the alley in the rear of location, next to the alley.	Large Items Discarded on Private Property
</pre>