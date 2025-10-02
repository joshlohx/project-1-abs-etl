import requests
import os
from dotenv import load_dotenv

load_dotenv()

url = "https://api.themoviedb.org/3/movie/now_playing"

params = {
    "language": "en-AU",
    "region": "AU"
}

headers = { 
    "accept": "application/json",
    "Authorization": f"Bearer {os.environ.get('API_TOKEN')}"
}

response = requests.get(
    url=url, 
    headers=headers, 
    params=params
    )

if response.status_code == 200:
    response_data = response.json()
else:
    raise Exception(
        f"Failed to extract data from The Movies Database API. Status Code {response.status_code}. Response: {response.text}"
    )

response_num_pages = response_data.get("total_pages")

airing_movie_data = response_data.get("results")

if response_num_pages > 1:
    for page_num in range(2, response_num_pages + 1):
        params.update({"page":page_num})
        response = requests.get(url=url, headers=headers, params=params)
        if response.status_code == 200:
            response_data = response.json()
            airing_movie_data.extend(response_data.get("results"))
        else:
            raise Exception(
                f"Failed to extract data from The Movies Database API. Status Code {response.status_code}. Response: {response.text}"
            )
else:
    pass
