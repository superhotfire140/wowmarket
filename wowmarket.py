from wowapi import WowApi #https://python-wowapi.readthedocs.io/en/latest/modules/wowapi.html#wowapi.api.WowApi.get_auctions
import pandas as pd
import requests
import config


api = WowApi(config.PUBLIC_KEY, config.PRIVATE_KEY)
api.get_token('us', namespace='dynamic-us', locale='en_US')
foo = api.get_auctions('us', 'zuljin', locale='en_US')
data = requests.get(foo['files'][0]['url'], 'json')

auctions = data.json()['auctions']

akunda = list(filter(lambda auction: auction['item'] == 152507, auctions))

df = pd.DataFrame(akunda)

df.to_excel('auctionhouse.xlsx', sheet_name='MarketInfo')
