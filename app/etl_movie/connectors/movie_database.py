import requests

class MovieDatabaseApiClient:

    def __init__(self, api_token: str):
        if api_token is None:
            raise Exception("An API Token must be provided.")
        self.api_token = api_token

        self.base_url = "https://api.themoviedb.org/3/"

    def get_now_playing(self) -> dict: 
        
        url = f"{self.base_url}movie/now_playing"

        params = {
            "language": "en-AU",
            "region": "AU"}

        headers = {
            "accept":"application/json",
            "Authorization": f"Bearer {self.api_token}"}

        response = requests.get(
            url=url, 
            headers=headers, 
            params=params)
        
        if response.status_code == 200 and response.json() is not None:
            return response.json()
        else:
            raise Exception(
                f"""
                Failed to extract now playing movie data from The Movies Database API. 
                Status Code {response.status_code}. 
                Response: {response.text}
                """)