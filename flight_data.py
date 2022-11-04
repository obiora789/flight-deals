import requests
import dotenv
import os

dotenv_file = dotenv.find_dotenv()
dotenv.load_dotenv(dotenv_file)


class FlightData:
    # This class is responsible for structuring the flight data.
    def __init__(self):
        self.tequila_endpoint = os.getenv("TEQUILA_ENDPOINT")
        self.headers = {"apikey": os.environ.get("HEADERS")}
        self.goflightlabs_endpoint = os.environ.get("GOFLIGHTLABS_ENDPOINT")

    def get_codes(self, city):
        icao_code = ""
        data = {
            "term": city,
        }
        iata_response = requests.get(url=self.tequila_endpoint, params=data, headers=self.headers)
        iata_response.raise_for_status()
        iata_code = iata_response.json()["locations"][0]["code"]
        parameters = {
            "access_key": "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJhdWQiOiI0IiwianRpIjoiNDMzYmVmZTAzM2E2MDNlMTMxZWY5Y"
                          "mY3MzFiZGI3ZjZhM2FjZDY5OGY2ODMwOGQyM2Y5MWE0ZmQwNzY2OTBjYzNkZDRhZWNmYzA4ZTNkNDgiLCJpYXQiOjE"
                          "2NjcyNzIwNDQsIm5iZiI6MTY2NzI3MjA0NCwiZXhwIjoxNjk4ODA4MDQ0LCJzdWIiOiIxNjYwNCIsInNjb3BlcyI6W"
                          "119.H_3W8acJzw97hDYaH04n10KBh4_rJRIteyttNf5dwpd0RJmK8pHZ54boJs5aAnB7Eg1jJtPIuBhxyzx-9W1bqQ",
            "search": iata_code
        }
        icao_response = requests.get(url=self.goflightlabs_endpoint, params=parameters)
        icao_response.raise_for_status()
        for item in icao_response.json():
            try:
                item["iata_code"]
            except KeyError:
                pass
            else:
                if item["iata_code"] == iata_code:
                    icao_code = item["icao_code"]
        return iata_code, icao_code
