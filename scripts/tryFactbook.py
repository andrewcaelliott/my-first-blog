import re
import requests
import json
from bs4 import BeautifulSoup
from blog.models import NumberFact
from blog.config import MEASURE_CHOICES, MULTIPLE_CHOICES,MULTIPLE_INVERSE
from blog.utils import parseBigNumber

continents = [
	"africa",
	"antarctica",
	"australia-oceania",
	"central-america-n-caribbean",
	"central-asia",
	"east-n-southeast-asia",
	"europe",
	"middle-east",
	"north-america",
	"oceans",
	"south-america",
	"south-asia",
	"world"
]

countries = [
		{"code": "af", "iso": "AF", "continent": "south-asia", "name": "Afghanistan"},
		{"code": "al", "iso": "AL", "continent": "europe", "name": "Albania"},
		{"code": "ag", "iso": "DZ", "continent": "africa", "name": "Algeria"},
		{"code": "an", "iso": "AD", "continent": "europe", "name": "Andorra"},
		{"code": "ao", "iso": "AO", "continent": "africa", "name": "Angola"},
		{"code": "ac", "iso": "AG", "continent": "central-america-n-caribbean", "name": "Antigua and Barbuda"},
		{"code": "ar", "iso": "AR", "continent": "south-america", "name": "Argentina"},
		{"code": "am", "iso": "AM", "continent": "middle-east", "name": "Armenia"},
		{"code": "as", "iso": "AU", "continent": "australia-oceania", "name": "Australia"},
		{"code": "au", "iso": "AT", "continent": "europe", "name": "Austria"},
		{"code": "aj", "iso": "AZ", "continent": "middle-east", "name": "Azerbaijan"},

		{"code": "bf", "iso": "BS", "continent": "central-america-n-caribbean", "name": "The Bahamas"},
		{"code": "ba", "iso": "BH", "continent": "middle-east", "name": "Bahrain"},
		{"code": "bg", "iso": "BD", "continent": "south-asia", "name": "Bangladesh"},
		{"code": "bb", "iso": "BB", "continent": "central-america-n-caribbean", "name": "Barbados"},
		{"code": "bo", "iso": "BY", "continent": "europe", "name": "Belarus"},
		{"code": "be", "iso": "BE", "continent": "europe", "name": "Belgium"},
		{"code": "bh", "iso": "BZ", "continent": "central-america-n-caribbean", "name": "Belize"},
		{"code": "bn", "iso": "BJ", "continent": "africa", "name": "Benin"},
		{"code": "bt", "iso": "BT", "continent": "south-asia", "name": "Bhutan"},
		{"code": "bl", "iso": "BO", "continent": "south-america", "name": "Bolivia"},
		{"code": "bk", "iso": "BA", "continent": "europe", "name": "Bosnia and Herzegovina"},
		{"code": "bc", "iso": "BW", "continent": "africa", "name": "Botswana"},
		{"code": "br", "iso": "BR", "continent": "south-america", "name": "Brazil"},
		{"code": "bx", "iso": "BN", "continent": "east-n-southeast-asia", "name": "Brunei"},
		{"code": "bu", "iso": "BG", "continent": "europe", "name": "Bulgaria"},
		{"code": "uv", "iso": "BF", "continent": "africa", "name": "Burkina Faso"},
		{"code": "bm", "iso": "MM", "continent": "east-n-southeast-asia", "name": "Burma"},
		{"code": "by", "iso": "BI", "continent": "africa", "name": "Burundi"},

		{"code": "cb", "iso": "KH", "continent": "east-n-southeast-asia", "name": "Cambodia"},
		{"code": "cm", "iso": "CM", "continent": "africa", "name": "Cameroon"},
		{"code": "ca", "iso": "CA", "continent": "north-america", "name": "Canada"},
		{"code": "cv", "iso": "CV", "continent": "africa", "name": "Cabo Verde"},
		{"code": "ct", "iso": "CF", "continent": "africa", "name": "Central African Republic"},
		{"code": "cd", "iso": "TD", "continent": "africa", "name": "Chad"},
		{"code": "ci", "iso": "CL", "continent": "south-america", "name": "Chile"},
		{"code": "ch", "iso": "CN", "continent": "east-n-southeast-asia", "name": "China"},
		{"code": "co", "iso": "CO", "continent": "south-america", "name": "Colombia"},
		{"code": "cn", "iso": "KM", "continent": "africa", "name": "Comoros"},
		{"code": "cg", "iso": "CD", "continent": "africa", "name": "Democratic Republic of the Congo"},
		{"code": "cf", "iso": "CG", "continent": "africa", "name": "The Congo"},
		{"code": "cs", "iso": "CR", "continent": "central-america-n-caribbean", "name": "Costa Rica"},
		{"code": "iv", "iso": "CI", "continent": "africa", "name": "Cote d'Ivoire"},
		{"code": "hr", "iso": "HR", "continent": "europe", "name": "Croatia"},
		{"code": "cu", "iso": "CU", "continent": "central-america-n-caribbean", "name": "Cuba"},
		{"code": "cy", "iso": "CY", "continent": "europe", "name": "Cyprus"},
		{"code": "ez", "iso": "CZ", "continent": "europe", "name": "Czechia"},

		{"code": "da", "iso": "DK", "continent": "europe", "name": "Denmark"},
		{"code": "dj", "iso": "DJ", "continent": "africa", "name": "Djibouti"},
		{"code": "do", "iso": "DM", "continent": "central-america-n-caribbean", "name": "Dominica"},
		{"code": "dr", "iso": "DO", "continent": "central-america-n-caribbean", "name": "The Dominican Republic"},

		{"code": "ec", "iso": "EC", "continent": "south-america", "name": "Ecuador"},
		{"code": "eg", "iso": "EG", "continent": "africa", "name": "Egypt"},
		{"code": "es", "iso": "SV", "continent": "central-america-n-caribbean", "name": "El Salvador"},
		{"code": "ek", "iso": "GQ", "continent": "africa", "name": "Equatorial Guinea"},
		{"code": "er", "iso": "ER", "continent": "africa", "name": "Eritrea"},
		{"code": "en", "iso": "EE", "continent": "europe", "name": "Estonia"},
		{"code": "wz", "iso": "SZ", "continent": "africa", "name": "Eswatini"},
		{"code": "et", "iso": "ET", "continent": "africa", "name": "Ethiopia"},

		{"code": "fj", "iso": "FJ", "continent": "australia-oceania", "name": "Fiji"},
		{"code": "fi", "iso": "FI", "continent": "europe", "name": "Finland"},
		{"code": "fr", "iso": "FR", "continent": "europe", "name": "France"},

		{"code": "gb", "iso": "GA", "continent": "africa", "name": "Gabon"},
		{"code": "ga", "iso": "GM", "continent": "africa", "name": "The Gambia"},
		{"code": "gg", "iso": "GE", "continent": "middle-east", "name": "Georgia"},
		{"code": "gm", "iso": "DE", "continent": "europe", "name": "Germany"},
		{"code": "gh", "iso": "GH", "continent": "africa", "name": "Ghana"},
		{"code": "gr", "iso": "GR", "continent": "europe", "name": "Greece"},
		{"code": "gj", "iso": "GD", "continent": "central-america-n-caribbean", "name": "Grenada"},
		{"code": "gt", "iso": "GT", "continent": "central-america-n-caribbean", "name": "Guatemala"},
		{"code": "gv", "iso": "GN", "continent": "africa", "name": "Guinea"},
		{"code": "pu", "iso": "GW", "continent": "africa", "name": "Guinea-Bissau"},
		{"code": "gy", "iso": "GY", "continent": "south-america", "name": "Guyana"},

		{"code": "ha", "iso": "HT", "continent": "central-america-n-caribbean", "name": "Haiti"},
		{"code": "ho", "iso": "HN", "continent": "central-america-n-caribbean", "name": "Honduras"},
		{"code": "hu", "iso": "HU", "continent": "europe", "name": "Hungary"},

		{"code": "ic", "iso": "IS", "continent": "europe", "name": "Iceland"},
		{"code": "in", "iso": "IN", "continent": "south-asia", "name": "India"},
		{"code": "id", "iso": "ID", "continent": "east-n-southeast-asia", "name": "Indonesia"},
		{"code": "ir", "iso": "IR", "continent": "middle-east", "name": "Iran"},
		{"code": "iz", "iso": "IQ", "continent": "middle-east", "name": "Iraq"},
		{"code": "ei", "iso": "IE", "continent": "europe", "name": "Ireland"},
		{"code": "is", "iso": "IL", "continent": "middle-east", "name": "Israel"},
		{"code": "it", "iso": "IT", "continent": "europe", "name": "Italy"},

		{"code": "jm", "iso": "JM", "continent": "central-america-n-caribbean", "name": "Jamaica"},
		{"code": "ja", "iso": "JP", "continent": "east-n-southeast-asia", "name": "Japan"},
		{"code": "jo", "iso": "JO", "continent": "middle-east", "name": "Jordan"},
		{"code": "kz", "iso": "KZ", "continent": "central-asia", "name": "Kazakhstan"},
		{"code": "ke", "iso": "KE", "continent": "africa", "name": "Kenya"},
		{"code": "kr", "iso": "KI", "continent": "australia-oceania", "name": "Kiribati"},
		{"code": "kn", "iso": "KP", "continent": "east-n-southeast-asia", "name": "North Korea"},
		{"code": "ks", "iso": "KR", "continent": "east-n-southeast-asia", "name": "South Korea"},
		{"code": "kv", "iso": "XK", "continent": "europe", "name": "Kosovo"},
		{"code": "ku", "iso": "KW", "continent": "middle-east", "name": "Kuwait"},
		{"code": "kg", "iso": "KG", "continent": "central-asia", "name": "Kyrgyzstan"},

		{"code": "la", "iso": "LA", "continent": "east-n-southeast-asia", "name": "Laos"},
		{"code": "lg", "iso": "LV", "continent": "europe", "name": "Latvia"},
		{"code": "le", "iso": "LB", "continent": "middle-east", "name": "Lebanon"},
		{"code": "lt", "iso": "LS", "continent": "africa", "name": "Lesotho"},
		{"code": "li", "iso": "LR", "continent": "africa", "name": "Liberia"},
		{"code": "ly", "iso": "LY", "continent": "africa", "name": "Libya"},
		{"code": "ls", "iso": "LI", "continent": "europe", "name": "Liechtenstein"},
		{"code": "lh", "iso": "LT", "continent": "europe", "name": "Lithuania"},
		{"code": "lu", "iso": "LU", "continent": "europe", "name": "Luxembourg"},

		{"code": "ma", "iso": "MG", "continent": "africa", "name": "Madagascar"},
		{"code": "mi", "iso": "MW", "continent": "africa", "name": "Malawi"},
		{"code": "my", "iso": "MY", "continent": "east-n-southeast-asia", "name": "Malaysia"},
		{"code": "mv", "iso": "MV", "continent": "south-asia", "name": "Maldives"},
		{"code": "ml", "iso": "ML", "continent": "africa", "name": "Mali"},
		{"code": "mt", "iso": "MT", "continent": "europe", "name": "Malta"},
		{"code": "rm", "iso": "MH", "continent": "australia-oceania", "name": "Marshall Islands"},
		{"code": "mr", "iso": "MR", "continent": "africa", "name": "Mauritania"},
		{"code": "mp", "iso": "MU", "continent": "africa", "name": "Mauritius"},
		{"code": "mx", "iso": "MX", "continent": "north-america", "name": "Mexico"},
		{"code": "fm", "iso": "FM", "continent": "australia-oceania", "name": "Micronesia"},
		{"code": "md", "iso": "MD", "continent": "europe", "name": "Moldova"},
		{"code": "mn", "iso": "MC", "continent": "europe", "name": "Monaco"},
		{"code": "mg", "iso": "MN", "continent": "east-n-southeast-asia", "name": "Mongolia"},
		{"code": "mj", "iso": "ME", "continent": "europe", "name": "Montenegro"},
		{"code": "mo", "iso": "MA", "continent": "africa", "name": "Morocco"},
		{"code": "mz", "iso": "MZ", "continent": "africa", "name": "Mozambique"},
		{"code": "bm", "iso": "MM", "continent": "east-n-southeast-asia", "name": "Myanmar"},

		{"code": "wa", "iso": "NA", "continent": "africa", "name": "Namibia"},
		{"code": "nr", "iso": "NR", "continent": "australia-oceania", "name": "Nauru"},
		{"code": "np", "iso": "NP", "continent": "south-asia", "name": "Nepal"},
		{"code": "nl", "iso": "NL", "continent": "europe", "name": "Netherlands"},
		{"code": "nz", "iso": "NZ", "continent": "australia-oceania", "name": "New Zealand"},
		{"code": "nu", "iso": "NI", "continent": "central-america-n-caribbean", "name": "Nicaragua"},
		{"code": "ng", "iso": "NE", "continent": "africa", "name": "Niger"},
		{"code": "ni", "iso": "NG", "continent": "africa", "name": "Nigeria"},
		{"code": "no", "iso": "NO", "continent": "europe", "name": "Norway"},
		{"code": "mk", "iso": "MK", "continent": "europe", "name": "North Macedonia"},

		{"code": "mu", "iso": "OM", "continent": "middle-east", "name": "Oman"},

		{"code": "pk", "iso": "PK", "continent": "south-asia", "name": "Pakistan"},
		{"code": "ps", "iso": "PW", "continent": "australia-oceania", "name": "Palau"},
		{"code": "pm", "iso": "PA", "continent": "central-america-n-caribbean", "name": "Panama"},
		{"code": "pp", "iso": "PG", "continent": "east-n-southeast-asia", "name": "Papua New Guinea"},
		{"code": "pa", "iso": "PY", "continent": "south-america", "name": "Paraguay"},
		{"code": "pe", "iso": "PE", "continent": "south-america", "name": "Peru"},
		{"code": "rp", "iso": "PH", "continent": "east-n-southeast-asia", "name": "Philippines"},
		{"code": "pl", "iso": "PL", "continent": "europe", "name": "Poland"},
		{"code": "po", "iso": "PT", "continent": "europe", "name": "Portugal"},

		{"code": "qa", "iso": "QA", "continent": "middle-east", "name": "Qatar"},

		{"code": "ro", "iso": "RO", "continent": "europe", "name": "Romania"},
		{"code": "rs", "iso": "RU", "continent": "central-asia", "name": "Russia"},
		{"code": "rw", "iso": "RW", "continent": "africa", "name": "Rwanda"},

		{"code": "sc", "iso": "KN", "continent": "central-america-n-caribbean", "name": "Saint Kitts and Nevis"},
		{"code": "st", "iso": "LC", "continent": "central-america-n-caribbean", "name": "Saint Lucia"},
		{"code": "vc", "iso": "VC", "continent": "central-america-n-caribbean", "name": "Saint Vincent and the Grenadines"},
		{"code": "ws", "iso": "WS", "continent": "australia-oceania", "name": "Samoa"},
		{"code": "sm", "iso": "SM", "continent": "europe", "name": "San Marino"},
		{"code": "tp", "iso": "ST", "continent": "africa", "name": "Sao Tome and Principe"},
		{"code": "sa", "iso": "SA", "continent": "middle-east", "name": "Saudi Arabia"},
		{"code": "sg", "iso": "SN", "continent": "africa", "name": "Senegal"},
		{"code": "ri", "iso": "RS", "continent": "europe", "name": "Serbia"},
		{"code": "se", "iso": "SC", "continent": "africa", "name": "Seychelles"},
		{"code": "sl", "iso": "SL", "continent": "africa", "name": "Sierra Leone"},
		{"code": "sn", "iso": "SG", "continent": "east-n-southeast-asia", "name": "Singapore"},
		{"code": "lo", "iso": "SK", "continent": "europe", "name": "Slovakia"},
		{"code": "si", "iso": "SI", "continent": "europe", "name": "Slovenia"},
		{"code": "bp", "iso": "SB", "continent": "australia-oceania", "name": "Solomon Islands"},
		{"code": "so", "iso": "SO", "continent": "africa", "name": "Somalia"},
		{"code": "sf", "iso": "ZA", "continent": "africa", "name": "South Africa"},
		{"code": "od", "iso": "SS", "continent": "africa", "name": "South Sudan"},
		{"code": "sp", "iso": "ES", "continent": "europe", "name": "Spain"},
		{"code": "ce", "iso": "LK", "continent": "south-asia", "name": "Sri Lanka"},
		{"code": "su", "iso": "SD", "continent": "africa", "name": "Sudan"},
		{"code": "ns", "iso": "SR", "continent": "south-america", "name": "Suriname"},
		{"code": "sw", "iso": "SE", "continent": "europe", "name": "Sweden"},
		{"code": "sz", "iso": "CH", "continent": "europe", "name": "Switzerland"},
		{"code": "sy", "iso": "SY", "continent": "middle-east", "name": "Syria"},

		{"code": "ti", "iso": "TJ", "continent": "central-asia", "name": "Tajikistan"},
		{"code": "tz", "iso": "TZ", "continent": "africa", "name": "Tanzania"},
		{"code": "th", "iso": "TH", "continent": "east-n-southeast-asia", "name": "Thailand"},
		{"code": "tt", "iso": "TL", "continent": "east-n-southeast-asia", "name": "Timor-Leste"},
		{"code": "to", "iso": "TG", "continent": "africa", "name": "Togo"},
		{"code": "tn", "iso": "TO", "continent": "australia-oceania", "name": "Tonga"},
		{"code": "td", "iso": "TT", "continent": "central-america-n-caribbean", "name": "Trinidad and Tobago"},
		{"code": "ts", "iso": "TN", "continent": "africa", "name": "Tunisia"},
		{"code": "tu", "iso": "TR", "continent": "middle-east", "name": "Turkey"},
		{"code": "tx", "iso": "TM", "continent": "central-asia", "name": "Turkmenistan"},
		{"code": "tv", "iso": "TV", "continent": "australia-oceania", "name": "Tuvalu"},

		{"code": "ug", "iso": "UG", "continent": "africa", "name": "Uganda"},
		{"code": "up", "iso": "UA", "continent": "europe", "name": "Ukraine"},
		{"code": "ae", "iso": "AE", "continent": "middle-east", "name": "United Arab Emirates"},
		{"code": "uk", "iso": "GB", "continent": "europe", "name": "United Kingdom"},
		{"code": "us", "iso": "US", "continent": "north-america", "name": "United States"},
		{"code": "uy", "iso": "UY", "continent": "south-america", "name": "Uruguay"},
		{"code": "uz", "iso": "UZ", "continent": "central-asia", "name": "Uzbekistan"},

		{"code": "nh", "iso": "VU", "continent": "australia-oceania", "name": "Vanuatu"},
		{"code": "vt", "iso": "VA", "continent": "europe", "name": "Holy See (Vatican City)"},
		{"code": "ve", "iso": "VE", "continent": "south-america", "name": "Venezuela"},
		{"code": "vm", "iso": "VN", "continent": "east-n-southeast-asia", "name": "Vietnam"},
		{"code": "ym", "iso": "YE", "continent": "middle-east", "name": "Yemen"},
		{"code": "za", "iso": "ZM", "continent": "africa", "name": "Zambia"},
		{"code": "zi", "iso": "ZW", "continent": "africa", "name": "Zimbabwe"}
]

def extract_dated_metric(raw_text, regex):
	gd = re.match(regex, raw_text).groupdict()
	return {
		"number": parseBigNumber(gd["NUMBER"]),
		"year": int(gd["YEAR"])
	}

def get_population(country):
	pop_text = country["People and Society"]["Population"]["text"]
	rx = r"(?P<NUMBER>[0-9,]+)\s\((?P<YEAR>[0-9]+).*\).*"
	return extract_dated_metric(pop_text, rx)

def get_gdp(country):
	text = country["Economy"]["GDP (official exchange rate)"]["text"]
	rx = r"(?P<NUMBER>\$[0-9.,]+\s?[a-z]*)\s\((?P<YEAR>[0-9]+).*\).*"
	return extract_dated_metric(text, rx)

def get_govexp(country):
	text = country["Economy"]["Budget"]["expenditures"]["text"]
	rx = r"(?P<NUMBER>\$[0-9.,]+\s?[a-z]*)\s\((?P<YEAR>[0-9]+).*\).*"
	return extract_dated_metric(text, rx)

def get_govrev(country):
	text = country["Economy"]["Budget"]["revenues"]["text"]
	rx = r"(?P<NUMBER>\$[0-9.,]+\s?[a-z]*)\s\((?P<YEAR>[0-9]+).*\).*"
	return extract_dated_metric(text, rx)

def get_debt(country, gdp):
	entries = country["Economy"]["Public debt"]
	text = entries[list(entries.keys())[0]]["text"]
	rx = r"(?P<NUMBER>[0-9.,]+)% of GDP\s\((?P<YEAR>[0-9]+).*\).*"
	perc = extract_dated_metric(text, rx)
	debt = gdp
	debt["number"] = (str(round(float(gdp["number"][0]) * float(perc["number"][0]) / 100, 5)), gdp["number"][1], gdp["number"][2], gdp["number"][3])
	return debt

def get_import_line(cc, metric, title, force_unit, force_measure):
	country_access = get_country_access(cc)
	country_detail = get_country_detail(cc)
	if metric == 'population':
		country_item = get_population(country_detail)
	if metric == 'gdp':
		country_item = get_gdp(country_detail)
	if metric == 'govexp':
		country_item = get_govexp(country_detail)
	if metric == 'govrev':
		country_item = get_govrev(country_detail)
	name = country_access["name"]
	iso = country_access["iso"]
	year = country_item["year"]
	magnitude, mult, unit, measure = country_item["number"]
	multiple = [pair[1] for pair in MULTIPLE_CHOICES if pair[0] == mult][0]
	scale = [s for (s, m) in MULTIPLE_INVERSE.items() if m == mult][0]
	nf = NumberFact(magnitude=magnitude, multiple=multiple, scale=scale, unit=unit, measure=measure, title=title.format(name=name))
	nf.normalise(round_to=3)	
	#measure = 'count'
	return f',{name},{year},{iso},{nf.magnitude},{nf.get_multiple_display()},{nf.scale},{force_unit},{force_measure},{country_access["url"]}'

def get_dependent_import_line(cc, metric, title, force_unit, force_measure):
	country_access = get_country_access(cc)
	country_detail = get_country_detail(cc)
	name = country_access["name"]
	iso = country_access["iso"]
	if metric == 'debt':
		gdp_item = get_gdp(country_detail)
		country_item = get_debt(country_detail, gdp_item)
		year = country_item["year"]
	magnitude, mult, unit, measure = country_item["number"]
	multiple = [pair[1] for pair in MULTIPLE_CHOICES if pair[0] == mult][0]
	scale = [s for (s, m) in MULTIPLE_INVERSE.items() if m == mult][0]
	nf = NumberFact(magnitude=magnitude, multiple=multiple, scale=scale, unit=unit, measure=measure, title=title.format(name=name))
	nf.normalise(round_to=3)	
	#measure = 'count'
	return f',{name},{year},{iso},{nf.magnitude},{nf.get_multiple_display()},{nf.scale},{force_unit},{force_measure},{country_access["url"]}'



def get_country(cc):
	for continent in continents:
		try:
			country = get_country_for_continent(continent, cc)
			return country
		except Exception as ex:
			pass


def get_country_for_continent(continent, cc):
	url = f'https://github.com/factbook/factbook.json/raw/master/{continent}/{cc}.json'
	response = requests.get(url=url)
	response.raise_for_status()
	country = json.loads(response.text)
	country["Continent"] = continent
	return country

def build_country_list():
	url = "https://github.com/factbook/factbook.json/tree/master"
	response = requests.get(url=url)
	html_content = response.text

	soup = BeautifulSoup(html_content, "html.parser")

	codes = soup.findAll('code')
	country_codes = [cc for cc in [codetag.text for codetag in codes] if len(cc)==2]
	for cc in country_codes[11:]:
		country = get_country(cc)
		print(f'{{"code":"{cc}", "continent": "{country["Continent"]}", "name": "{country["Government"]["Country name"]["conventional short form"]["text"]}"}},')
	print("ok")

def list_countries():
	for country in countries:
		print(country["name"])


def get_country_access(cc):
	country_access = next(country for country in countries if country["code"] == cc)
	if country_access:
		country_access["url"] = f'https://github.com/factbook/factbook.json/raw/master/{country_access["continent"]}/{cc}.json'
		return country_access


def get_country_detail(cc):
	country_access = next(get_country_access(cc) for country in countries if country["code"] == cc)
	if country_access:
		return get_country_for_continent(country_access["continent"], cc)


def run():
	for country in countries[:10]:
		#print(get_import_line(country["code"], "population", "Population of {name}", "people"))
		#print(get_import_line(country["code"], "gdp", "GDP of {name}", "USD", "amount.gdp"))
		#print(get_import_line(country["code"], "govexp", "Government Expenditure of {name}", "USD", "amount.~finance"))
		#print(get_import_line(country["code"], "govrev", "Government Revenues of {name}", "USD", "amount.~finance"))
		print(get_dependent_import_line(country["code"], "debt", "Public Debt of {name}", "USD", "amount.~use"))
