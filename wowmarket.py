from wowapi import WowApi #https://python-wowapi.readthedocs.io/en/latest/modules/wowapi.html#wowapi.api.WowApi.get_auctions
import pandas as pd
import requests
import config


api = WowApi(config.PUBLIC_KEY, config.PRIVATE_KEY)
api.get_token('us', namespace='dynamic-us', locale='en_US')
foo = api.get_auctions('us', 'zuljin', locale='en_US')
data = requests.get(foo['files'][0]['url'], 'json')

auctions = data.json()['auctions']

# # Akunda Data
# akunda = list(filter(lambda auction: auction['item'] == 152507, auctions))
# akunda_df = pd.DataFrame(akunda)
# akunda_df['buyout'] = akunda_df['buyout']/10000
# akunda_df['Price/Unit'] = akunda_df['buyout']/akunda_df['quantity']

# Riverbud Data
riverbud = list(filter(lambda auction: auction['item'] == 152505, auctions))
riverbud_df = pd.DataFrame(riverbud)
riverbud_df['buyout'] = riverbud_df['buyout']/10000
riverbud_df['Price/Unit'] = riverbud_df['buyout']/riverbud_df['quantity']
riverbud_200_df = riverbud_df[riverbud_df['quantity'] == 200]

# Remove Outliers
riverbud_200_avg = riverbud_200_df['Price/Unit'].mean()
riverbud_200_std = riverbud_200_df['Price/Unit'].std()

riverbud_200_df = riverbud_200_df[riverbud_200_df['Price/Unit'] < riverbud_200_avg + 2*riverbud_200_std]
riverbud_df = riverbud_df[riverbud_df['Price/Unit'] < riverbud_200_avg + 2*riverbud_200_std]

# Get new avg and std
riverbud_200_avg = riverbud_200_df['Price/Unit'].mean()
riverbud_200_std = riverbud_200_df['Price/Unit'].std()

riverbud_df['Price/Unit Avg'] = riverbud_200_avg
riverbud_df['Price/Unit Std'] = riverbud_200_std
riverbud_df['Std 1'] = riverbud_200_avg - riverbud_200_std
riverbud_df['Std 2'] = riverbud_200_avg - riverbud_200_std*2
riverbud_df['%'] = riverbud_df['Price/Unit'] / riverbud_200_avg

# Write to Excel
riverbud_df.to_excel('riverbud_auctions.xlsx', sheet_name='Riverbud')
