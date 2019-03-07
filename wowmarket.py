from wowapi import WowApi
import pandas
import requests

api = WowApi('2e5f247983b941ec8cea07f8e6e8802f', 'muq1xUmblMpnjMIZuRts60kmPFKCUObY')
api.get_token('us', namespace='dynamic-us', locale='en_US')
foo = api.get_auctions('us', 'zuljin', locale='en_US')
data = requests.get(foo['files'][0]['url'], 'json')

auctions = data.json()['auctions']

thaeleeaAuctions = list(filter(lambda auction: auction['owner'] == 'Thaeleea', auctions))

sum(map(lambda auction: auction['buyout'], thaeleeaAuctions))/10000
