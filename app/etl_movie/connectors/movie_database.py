import requests

class MovieDatabaseApiClient:

    def __init__(self, api_token: str):
        if api_token is None:
            raise Exception("An API Token must be provided.")
        self.api_token = api_token

        self.base_url = "https://api.themoviedb.org/3/"

    def get_now_playing(self) -> list[dict]: 
        
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
        
        if response.status_code == 200 and response.json().get("results") is not None:
            response_json = response.json().get("results")
            response_pages = response.json().get("total_pages")
        else:
            raise Exception(
                f"""
                Failed to extract now playing movie data from The Movies Database API. 
                Status Code {response.status_code}. 
                Response: {response.text}
                """)
        
        if response_pages > 1:
            for page_num in range(2, response_pages + 1):
                params.update({"page":page_num})
                response = requests.get(url="https://api.themoviedb.org/3/movie/now_playing", headers=headers, params=params)
                if response.status_code == 200:
                    response_json.extend(response.json().get("results"))
                else:
                    raise Exception(
                        f"""
                        Failed to extract page {page_num} from now playing movie data from The Movies Database API. 
                        Status Code {response.status_code}. 
                        Response: {response.text}
                        """
                    )
        else:
            pass
        
        return response_json