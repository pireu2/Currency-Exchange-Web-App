import requests
from datetime import date

# api used https://exchangerate.host/

isocodes = {
    "AED": "ae",
    "AFN": "af",
    "ALL": "al",
    "AMD": "am",
    "ANG": "nl",
    "AOA": "ao",
    "ARS": "ar",
    "AUD": "au",
    "AWG": "aw",
    "AZN": "az",
    "BAM": "ba",
    "BBD": "bb",
    "BDT": "bd",
    "BGN": "bg",
    "BHD": "bh",
    "BIF": "bi",
    "BMD": "bm",
    "BND": "bn",
    "BOB": "bo",
    "BRL": "br",
    "BSD": "bs",
    "BTC": "-",
    "BTN": "bt",
    "BWP": "bw",
    "BYN": "by",
    "BZD": "bz",
    "CAD": "ca",
    "CDF": "cd",
    "CHF": "ch",
    "CLF": "cl",
    "CLP": "cl",
    "CNH": "cn",
    "CNY": "cn",
    "COP": "co",
    "CRC": "cr",
    "CUC": "cu",
    "CUP": "cu",
    "CVE": "cv",
    "CZK": "cz",
    "DJF": "dj",
    "DKK": "dk",
    "DOP": "do",
    "DZD": "dz",
    "EGP": "eg",
    "ERN": "er",
    "ETB": "et",
    "EUR": "eu",
    "FJD": "fj",
    "FKP": "fk",
    "GBP": "gb",
    "GEL": "ge",
    "GGP": "gg",
    "GHS": "gh",
    "GIP": "gi",
    "GMD": "gm",
    "GNF": "gn",
    "GTQ": "gt",
    "GYD": "gy",
    "HKD": "hk",
    "HNL": "hn",
    "HRK": "hr",
    "HTG": "ht",
    "HUF": "hu",
    "IDR": "id",
    "ILS": "il",
    "IMP": "im",
    "INR": "in",
    "IQD": "iq",
    "IRR": "ir",
    "ISK": "is",
    "JEP": "je",
    "JMD": "jm",
    "JOD": "jo",
    "JPY": "jp",
    "KES": "ke",
    "KGS": "kg",
    "KHR": "kh",
    "KMF": "km",
    "KPW": "kp",
    "KRW": "kr",
    "KWD": "kw",
    "KYD": "ky",
    "KZT": "kz",
    "LAK": "la",
    "LBP": "lb",
    "LKR": "lk",
    "LRD": "lr",
    "LSL": "ls",
    "LYD": "ly",
    "MAD": "ma",
    "MDL": "md",
    "MGA": "mg",
    "MKD": "mk",
    "MMK": "mm",
    "MNT": "mn",
    "MOP": "mo",
    "MRO": "mr",
    "MRU": "mr",
    "MUR": "mu",
    "MVR": "mv",
    "MWK": "mw",
    "MXN": "mx",
    "MYR": "my",
    "MZN": "mz",
    "NAD": "na",
    "NGN": "ng",
    "NIO": "ni",
    "NOK": "no",
    "NPR": "np",
    "NZD": "nz",
    "OMR": "om",
    "PAB": "pa",
    "PEN": "pe",
    "PGK": "pg",
    "PHP": "ph",
    "PKR": "pk",
    "PLN": "pl",
    "PYG": "py",
    "QAR": "qa",
    "RON": "ro",
    "RSD": "rs",
    "RUB": "ru",
    "RWF": "rw",
    "SAR": "sa",
    "SBD": "sb",
    "SCR": "sc",
    "SDG": "sd",
    "SEK": "se",
    "SGD": "sg",
    "SHP": "sh",
    "SLL": "sl",
    "SOS": "so",
    "SRD": "sr",
    "SSP": "ss",
    "STD": "st",
    "STN": "st",
    "SVC": "sv",
    "SYP": "sy",
    "SZL": "sz",
    "THB": "th",
    "TJS": "tj",
    "TMT": "tm",
    "TND": "tn",
    "TOP": "to",
    "TRY": "tr",
    "TTD": "tt",
    "TWD": "tw",
    "TZS": "tz",
    "UAH": "ua",
    "UGX": "ug",
    "USD": "us",
    "UYU": "uy",
    "UZS": "uz",
    "VEF": "ve",
    "VES": "ve",
    "VND": "vn",
    "VUV": "vu",
    "WST": "ws",
    "XAF": "cm",
    "XAG": "-",
    "XAU": "-",
    "XCD": "ag",
    "XDR": "-",
    "XOF": "ci",
    "XPD": "-",
    "XPF": "pf",
    "XPT": "-",
    "YER": "ye",
    "ZAR": "za",
    "ZMW": "zm",
    "ZWL": "zw",
}


# converts the base amount specified of the base currency to the to currency
def convert(base, to, amount):
    url = "https://api.exchangerate.host/convert"
    try:
        base = base.upper()
        to = to.upper()
        amount = float(amount)
    except (AttributeError, ValueError):
        return None
    url = url + f"?from={base}&to={to}&amount={amount}"
    response = requests.get(url)
    data = response.json()
    if data["success"] == True:
        return data["result"]
    else:
        return None


# returns a list of dictionaries of all the possible currencies
def symbols():
    url = "https://api.exchangerate.host/symbols"
    response = requests.get(url)
    data = response.json()
    if data["success"] == True:
        list = []
        for value in data["symbols"].values():
            list.append({"symbol": value["code"], "description": value["description"]})
        return list
    else:
        return None


# returns a list of dictionaries of all the exchange rates for the base currency
def lookup(base):
    url = f"https://api.exchangerate.host/latest"
    try:
        base = base.upper()
    except AttributeError:
        return None
    url = url + f"?base={base}"
    response = requests.get(url)
    data = response.json()
    if data["success"] == True and data["base"] == base:
        list = []
        for key, value in data["rates"].items():
            list.append({"symbol": key, "rate": value})
        return list
    else:
        return None


# returns a list of dictionarties containting all the exchange rates for the base currency at a particular time
def history(base, date_string):
    url = "https://api.exchangerate.host/"
    try:
        base = base.upper()
        date.fromisoformat(date_string)
    except (AttributeError, ValueError):
        return None
    url = url + date_string + f"?base={base}"
    response = requests.get(url)
    data = response.json()
    if data["success"] == True and data["base"] == base:
        list = []
        for key, value in data["rates"].items():
            list.append({"symbol": key, "rate": value})
        return list
    else:
        return None


def flags():
    url = "https://flagcdn.com/"
    symbols = []
    for symbol in isocodes.keys():
        if symbol in isocodes.keys():
            if isocodes[symbol] != "-":
                flag = url + isocodes[symbol] + ".svg"
            elif symbol == "BTC":
                flag = "https://img.icons8.com/?size=512&id=63192&format=svg"  # bitcoin logo image
            elif symbol == "XAG":
                flag = "https://img.icons8.com/?size=512&id=60371&format=svg"  # silver ingot image
            elif symbol == "XAU":
                flag = "https://img.icons8.com/?size=512&id=20043&format=svg"  # gold bars image
            elif symbol == "XDR":
                flag = "https://static.currencyrate.today/f/flags/xdr.svg"  # xdr logo image
            elif symbol == "XPT":
                flag = "https://img.icons8.com/?size=512&id=uejo9NN9fl7z&format=svg"  # platinum image
            elif symbol == "XPD":
                flag = "https://img.icons8.com/?size=512&id=aCKekxNDs6IE&format=svg"  # palladium image
        else:
            flag = None

        symbols.append({
            'symbol' : symbol,
            'flag': flag
        })
    return symbols


