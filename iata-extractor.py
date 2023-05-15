# import csv
#
# import requests
# API_KEY='2cb18dde-ae85-42e8-a5c5-e18fafba643e'
# params={'api_key':API_KEY}
# API_URL="https://airlabs.co/api/v9/cities"
# response=requests.get(url=API_URL,params=params)
# response.raise_for_status()
# data=response.json()['response']
# city_list=[]
# for city in data:
#     city_list.append([city['name'],city['city_code']])
# # print(city_list)
# with open('3-letter-city.csv', mode='a') as city_codes:
#     for city in city_list:
#         writer = csv.writer(city_codes)
#         writer.writerow(city)