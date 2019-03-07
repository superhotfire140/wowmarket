from wowapi import WowApi
import pandas

api = WowApi('PUBLIC_KEY', 'PRIVATE_KEY')
api.get_token('us', namespace='dynamic-us', locale='en_US')
foo = api.get_auctions('us', 'zuljin', locale='en_US')
foo.json().keys()

foo.json()['auctions']

auctions = foo.json()['auctions']
thaeleeaAuctions = list(filter(lambda auction: auction['owner'] == 'Thaeleea', auctions))


sum(map(lambda auction: auction['buyout'], thaeleeaAuctions))/10000
