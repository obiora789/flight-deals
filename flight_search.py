import requests
from datetime import datetime
from dateutil.relativedelta import relativedelta
import dotenv
import os

dotenv_file = dotenv.find_dotenv()
dotenv.load_dotenv(dotenv_file)


class FlightSearch:
    # This class handles flight searches for the destination cities provided
    def __init__(self):
        self.flight_search_endpoint = os.environ.get("FLIGHTSEARCH_ENDPOINT")
        self.return_ticket = {"apikey": os.environ.get("RETURN_TICKET")}
        self.today = datetime.today().date()
        self.tomorrow = (self.today + relativedelta(day=+2)).strftime("%d/%m/%Y")  # tomorrow
        self.six_months = (self.today + relativedelta(months=+6)).strftime("%d/%m/%Y")  # in six months
        self.round_7 = (self.today + relativedelta(day=+8)).strftime("%d/%m/%Y")  # in 7 days time
        self.round_28 = (self.today + relativedelta(day=+29)).strftime("%d/%m/%Y")  # in 28 days time
        self.currency = "NGN"

    def search_flight(self, departure, destination):
        """This method performs flight searches from the flight API and sends the result to main.py"""
        parameters = {
            "fly_from": departure,
            "fly_to": destination,
            "date_from": self.tomorrow,
            "date_to": self.six_months,
            "return_from": self.round_7,
            "return_to": self.round_28,
            "curr": self.currency,
        }
        response = requests.get(url=self.flight_search_endpoint, params=parameters, headers=self.return_ticket)
        response.raise_for_status()
        return response.json()["data"][0]["price"]
