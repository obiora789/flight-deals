from data_manager import DataManager
from flight_data import FlightData
from flight_search import FlightSearch
from notification_manager import NotificationManager

CITY_OF_DEPARTURE = "Lagos"
flight_prices = FlightSearch()
get_iata = FlightData()
DEPARTURE_AERODROME = get_iata.get_codes(CITY_OF_DEPARTURE)[0]
data_mgr = DataManager()
notify_user = NotificationManager()
flight_date_7 = flight_prices.round_7
flight_date_28 = flight_prices.round_28


def write_code():
    """This method sends necessary data to notifications, Google Sheets and the data.json file to be updated."""
    iata_code = both_codes[0]
    icao_code = both_codes[1]
    best_deal = flight_prices.search_flight(departure=DEPARTURE_AERODROME, destination=iata_code)
    best_deal = round(float(best_deal), 2)
    write_data = {
        location["city"].title(): {"iataCode": iata_code, "icaoCode": icao_code,
                                   "lowestPrice": f"{best_deal}", "id": location["id"], },
    }
    try:
        old_price = location["lowestPrice"]
        try:
            old_price = float(old_price.split("₦")[1])
        except ValueError:
            old_price = float(old_price.split("₦")[2])
    except KeyError:
        location["lowestPrice"] = best_deal
    else:
        if best_deal < float(old_price):
            print("better deal")
            notify_user.send_notification(deal_price=best_deal, dept_city=CITY_OF_DEPARTURE,
                                          iata_dep=DEPARTURE_AERODROME, iata_dest=iata_code,
                                          date_7=flight_date_7, date_28=flight_date_28, dest_city=location["city"])
    if "iataCode" in keys_list and "icaoCode" in keys_list:
        data_mgr.write_google_sheet([{"lowestPrice": f"{'{:.2f}'.format(best_deal)}", "id": location["id"]}])
    else:
        data_mgr.write_google_sheet([{"iataCode": iata_code, "icaoCode": icao_code,
                                      "lowestPrice": f"{'{:.2f}'.format(best_deal)}", "id": location["id"]}])
    data_mgr.write_to_file(write_data)


for location in data_mgr.sheety_data:
    keys_list = list(location.keys())
    get_local_data = data_mgr.search_local(location["city"])
    if data_mgr.data_found:
        both_codes = get_local_data
        write_code()
    else:
        both_codes = get_iata.get_codes(location["city"])
        write_code()
