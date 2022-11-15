import requests
from google.cloud import datastore

# Import python date module
import datetime

def query_address(param):
    # Define returning variables
    ethereum = {
        'total_gas_spent': '0',
        'total_gas_spent_usd': '0',
        'avg_gas_per_tx': '0',
        'avg_gas_per_tx_usd': '0',
        'wallet': param
    }

    # optimism = {
    #     'total_gas_spent': '0',
    #     'total_gas_spent_usd': '0',
    #     'avg_gas_per_tx': '0',
    #     'avg_gas_per_tx_usd': '0',
    #     'history': ''
    # }
    #
    # arbitrum = {
    #     'total_gas_spent': '0',
    #     'total_gas_spent_usd': '0',
    #     'avg_gas_per_tx': '0',
    #     'avg_gas_per_tx_usd': '0',
    #     'history': ''
    # }

    # General parts of the query
    url = "https://pregod.rss3.dev/v1/notes/{}".format(param)
    headers = {"accept": "application/json"}

    # Build ethereum request
    eth_params = {
        'include_poap': 'false',
        'count_only': 'false',
        'query_status': 'false',
        'network': 'ethereum'
    }
    eth_response = requests.get(url, params=eth_params, headers=headers).json()
    eth_results = eth_response["result"]

    eth_total_gas = 0
    for tx in eth_results: # Each item in the list of results is a transaction
            eth_total_gas += float(tx['fee'])

    eth_avg_gas = eth_total_gas/len(eth_results)


    # # Build optimism request
    # op_params = {
    #     'include_poap': 'false',
    #     'count_only': 'false',
    #     'query_status': 'false',
    #     'network': 'optimism'
    # }
    # op_response = requests.get(url, params=op_params, headers=headers).json()
    # op_results = op_response["result"]
    #
    # op_total_gas = 0
    # for tx in op_results: # Each item in the list of results is a transaction
    #         op_total_gas += float(tx['fee'])
    #
    # op_avg_gas = op_total_gas/len(op_results)
    #
    #
    # # Build arbitrum request
    # arb_params = {
    #     'include_poap': 'false',
    #     'count_only': 'false',
    #     'query_status': 'false',
    #     'network': 'arbitrum'
    # }
    # arb_response = requests.get(url, params=arb_params, headers=headers).json()
    # arb_results = arb_response["result"]
    #
    # arb_total_gas = 0
    # for tx in arb_results: # Each item in the list of results is a transaction
    #         arb_total_gas += float(tx['fee'])
    #
    # arb_avg_gas = arb_total_gas/len(arb_results)
    #

    # Get current Ethereum price
    url = 'https://api.coingecko.com/api/v3/coins/ethereum'
    payload = {
        'localization':'false',
        'stickers':'false',
        'market_data':'true',
        'community_data':'false',
        'developer_data':'false',
        'sparkline':'false'
    }

    response = requests.get(url, params=payload)
    json_response = response.json()
    eth_price = json_response['market_data']['current_price']['usd']
    print(eth_price)


    # Reconciliation
    ethereum['total_gas_spent'] = "{:.15f}".format(eth_total_gas)
    ethereum['total_gas_spent_usd'] = "{:.2f}".format(eth_total_gas * eth_price)
    ethereum['avg_gas_per_tx'] = "{:.15f}".format(eth_avg_gas)
    ethereum['avg_gas_per_tx_usd'] = "{:.2f}".format(eth_avg_gas * eth_price)

    # optimism['total_gas_spent'] = op_total_gas
    # optimism['total_gas_spent_usd'] = op_total_gas * eth_price
    # optimism['avg_gas_per_tx'] = op_avg_gas
    # optimism['avg_gas_per_tx_usd'] = op_avg_gas * eth_price
    #
    # arbitrum['total_gas_spent'] = arb_total_gas
    # arbitrum['total_gas_spent_usd'] = arb_total_gas * eth_price
    # arbitrum['avg_gas_per_tx'] = arb_avg_gas
    # arbitrum['avg_gas_per_tx_usd'] = arb_avg_gas * eth_price

    response = {
        'ethereum': ethereum
    }

    return response

def count_pageview():
    # Instantiate client
    client = datastore.Client()

    # The kind for the new entity
    kind = "Pageview"

    # Compose the entity key which includes the date
    key = client.key(kind, str(datetime.date.today()))

    # Try to get task
    stat = client.get(key)

    # If stats is a valid entity, go ahead to update
    if stat:
        stat.update({
            "views": stat['views'] + 1
        })
        client.put(stat)

    else: # Create a new entity
        stat = datastore.Entity(key)
        stat.update({
            "views": 1,
            "date": datetime.datetime.now().strftime("%G-%m-%d")
        })
        client.put(stat)
