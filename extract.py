import requests
import os
from dotenv import load_dotenv

load_dotenv()

params = {
    "language": "en-AU",
    "region": "AU"
}

headers = { 
    "accept": "application/json",
    "Authorization": f"Bearer {os.environ.get('API_TOKEN')}"
}

now_playing_resp = requests.get(
    url="https://api.themoviedb.org/3/movie/now_playing", 
    headers=headers, 
    params=params
    )

upcoming_resp = requests.get(
    url="https://api.themoviedb.org/3/movie/upcoming", 
    headers=headers, 
    params=params
    )

if now_playing_resp.status_code == 200:
    now_playing_json = now_playing_resp.json()
else:
    raise Exception(
        f"""
        Failed to extract now playing movie data from The Movies Database API. 
        Status Code {now_playing_resp.status_code}. 
        Response: {now_playing_resp.text}
        """
    )

if upcoming_resp.status_code == 200:
    upcoming_json = upcoming_resp.json()
else:
    raise Exception(
        f"""
        Failed to extract upcoming movie data from The Movies Database API. 
        Status Code {upcoming_resp.status_code}. 
        Response: {upcoming_resp.text}
        """
    )

now_playing_total_pages = now_playing_json.get("total_pages")
upcoming_total_pages = upcoming_json.get("total_pages")

now_playing_data = now_playing_json.get("results")
upcoming_data = upcoming_json.get("results")

if now_playing_total_pages > 1:
    for page_num in range(2, now_playing_total_pages + 1):
        params.update({"page":page_num})
        response = requests.get(url="https://api.themoviedb.org/3/movie/now_playing", headers=headers, params=params)
        if response.status_code == 200:
            response_data = response.json()
            now_playing_data.extend(response_data.get("results"))
        else:
            raise Exception(
                f"""
                Failed to extract now playing movie data from The Movies Database API. 
                Status Code {now_playing_resp.status_code}. 
                Response: {now_playing_resp.text}
                """
            )
else:
    pass

if upcoming_total_pages > 1:
    for page_num in range(2, upcoming_total_pages + 1):
        params.update({"page":page_num})
        response = requests.get(url="https://api.themoviedb.org/3/movie/upcoming", headers=headers, params=params)
        if response.status_code == 200:
            response_data = response.json()
            upcoming_data.extend(response_data.get("results"))
        else:
            raise Exception(
                f"""
                Failed to extract upcoming movie data from The Movies Database API. 
                Status Code {upcoming_resp.status_code}. 
                Response: {upcoming_resp.text}
                """
            )
else:
    pass
