import requests

BASE_URL = "https://restcountries.com/v3.1"

def get_country_info(country_name):
    url = f"{BASE_URL}/name/{country_name}"
    response = requests.get(url)
    
    if response.status_code == 200:
        country_data = response.json()
        return country_data
    else:
        print(f"Failed to retrieve data {response.status_code}")

def get_all_countries():
    url = f"{BASE_URL}/all"
    response = requests.get(url)

    if response.status_code == 200:
        countries_all = response.json()
        return countries_all
    else:
        print(f"Failed to retrieve data {response.status_code}")

def get_countries_by_region(region):
    url = f"{BASE_URL}/region/{region}"
    response = requests.get(url)

    if response.status_code == 200:
        countries_by_region = response.json()
        return countries_by_region
    else:
        print(f"Failed to retrieve data {response.status_code}")