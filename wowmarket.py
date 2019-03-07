from wowapi import WowApi #https://python-wowapi.readthedocs.io/en/latest/modules/wowapi.html#wowapi.api.WowApi.get_auctions
import pandas as pd
import requests
import numpy

api = WowApi('PUBLIC_KEY', 'PRIVATE_KEY')
api.get_token('us', namespace='dynamic-us', locale='en_US')
foo = api.get_auctions('us', 'zuljin', locale='en_US')
data = requests.get(foo['files'][0]['url'], 'json')

auctions = data.json()['auctions']

df = pd.DataFrame(auctions)

df['owner'].mode()

thaeleeaAuctions = list(filter(lambda auction: auction['owner'] == 'Unhoarie', auctions))

sum(map(lambda auction: auction['buyout'], thaeleeaAuctions))/10000
