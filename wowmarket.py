from wowapi import WowApi #https://python-wowapi.readthedocs.io/en/latest/modules/wowapi.html#wowapi.api.WowApi.get_auctions
import pandas as pd
import requests
import config
import datetime

input_item = input("Item #: ")

api = WowApi(config.PUBLIC_KEY, config.PRIVATE_KEY)
api.get_token('us', namespace='dynamic-us', locale='en_US')
foo = api.get_auctions('us', 'zuljin', locale='en_US')
data = requests.get(foo['files'][0]['url'], 'json')

auctions = data.json()['auctions']

# market Data
market = list(filter(lambda auction: auction['item'] == int(input_item), auctions))
market_df = pd.DataFrame(market)
market_df['buyout'] = market_df['buyout']/10000
market_df['Price/Unit'] = market_df['buyout']/market_df['quantity']
market_200_df = market_df[market_df['quantity'] == 200].copy()

# Remove Outliers
market_200_avg = market_200_df['Price/Unit'].mean()
market_200_std = market_200_df['Price/Unit'].std()

market_200_df = market_200_df[market_200_df['Price/Unit'] < market_200_avg + 1.5*market_200_std]

# Get new avg and std
market_200_avg = market_200_df['Price/Unit'].mean()
market_200_std = market_200_df['Price/Unit'].std()

market_df = market_df[market_df['Price/Unit'] < market_200_avg + 2*market_200_std]

market_df['Price/Unit Avg'] = market_200_avg
market_df['Price/Unit Std'] = market_200_std
market_df['Std 1'] = market_200_avg - market_200_std
market_df['Std 2'] = market_200_avg - market_200_std*2
market_df['%'] = market_df['Price/Unit'] / market_200_avg

#Write to Market Price file
price_upper = market_200_avg + market_200_std*2
price_lower = market_200_avg - market_200_std*2

time_stamp = datetime.datetime.now()
time_stamp = time_stamp.strftime("%Y-%m-%d %H:%M")

# Write to Excel
market_df.to_excel('market_auctions.xlsx', sheet_name='market')