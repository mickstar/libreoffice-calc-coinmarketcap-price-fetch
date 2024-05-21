import uno
import http.client, ssl
import json

# 
# You need to set the api key here
# You can obtain an API key from coinmarketcap API page, there's a free plan that should be enough
# e.g
# CMC_API_KEY = "1234567-1234-1234-1234-1234567890"
CMC_API_KEY = None

def fetch_quote_from_coinmarketcap(cryptocurrency, currency="USD"):
    '''
        For whatever reason, we can't use the requests library in python
        so we have to make a fetch using the standard library http lib.
    '''

    url = f"https://pro-api.coinmarketcap.com/v2/cryptocurrency/quotes/latest?convert={currency}&symbol={cryptocurrency}"

    # Parse the URL
    from urllib.parse import urlparse
    parsed_url = urlparse(url)

    # Create an SSL context that does not verify the certificate
    # we do this because the python runtime in libreoffice doesn't have access to
    # OS certificate chain.
    context = ssl.create_default_context()
    context.check_hostname = False
    context.verify_mode = ssl.CERT_NONE


    # Create a connection based on the URL scheme
    if parsed_url.scheme == "https":
        conn = http.client.HTTPSConnection(parsed_url.netloc, context=context)
    else:
        conn = http.client.HTTPConnection(parsed_url.netloc)
    
    # Make the request
    headers = {
        "X-CMC_PRO_API_KEY": CMC_API_KEY,
    }
    conn.request("GET", parsed_url.path + "?" + parsed_url.query, headers=headers)

    # Get the response
    response = conn.getresponse()
    data = response.read()
    
    # Close the connection
    conn.close()

    # Return the response data as a string
    return data.decode('utf-8')

def get_price_from_cmc(cryptocurrency, currency):
    if CMC_API_KEY is None:
        return "ERROR API KEY NOT SET"

    r = fetch_quote_from_coinmarketcap(cryptocurrency, currency)
    
    try:
        data = json.loads(r)
    except:
        return "error bad response"

    if "data" not in data or cryptocurrency not in data["data"]:
        return "error data not in response"

    price = -1
    try:
        price = data["data"][cryptocurrency][0]["quote"][currency]["price"]
    except:
        return "error price not available"

    # Return the value
    return price
