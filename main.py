import requests as r
from datetime import datetime


class SearchTickets:
    def __init__(self, fly_from, fly_to):
        self.fly_from = fly_from
        self.fly_to = fly_to
        self.dateFrom = ""
        self.dateTo = ""
        self.head = {"apikey": "bBcEN7gg1PDGVw5S8ryHzFBfSkWvPhCs"}

    def search(self, date_from, date_to):
        self.dateFrom = date_from
        self.dateTo = date_to
        url = f"https://api.tequila.kiwi.com/v2/search?fly_from={self.fly_from}&fly_to={self.fly_to}&dateFrom=" \
              f"{self.dateFrom}&dateTo={self.dateTo}"
        response = r.get(url, headers=self.head)
        durations = [el["duration"]["total"] for el in response.json()["data"]]

        flyes = [fly for fly in response.json()["data"] if fly["duration"]["total"] <= min(durations)*1.5 ]
        prices = [el["price"] for el in flyes]
        cheapest_fly_on_that_day = flyes[prices.index(min(prices))]

        result_str = f"\nFrom {self.fly_from} to {self.fly_to}" \
                     f"\nData departure: {cheapest_fly_on_that_day['utc_departure'].replace('T', ' ').replace('Z', '').replace(':00.000', '')}" \
                     f"\nData arrival: {cheapest_fly_on_that_day['utc_arrival'].replace('T', ' ').replace('Z', '').replace(':00.000', '')}" \
                     f"\nCompany: {', '.join(cheapest_fly_on_that_day['airlines'])}" \
                     f"\nPrice: {cheapest_fly_on_that_day['price']} £" \
                     f"\n—————————————————————————————————————————\n"

        with open("data.txt", "a") as fl:
            fl.write(result_str)
            fl.close()


def multi_destination(searching_from_date, searching_to_date):
    req = r.get('https://api.sheety.co/c61d0b53b3cd45902d9612a931178d10/fly/лист1')
    list_of_destinations = req.json()['лист1']

    with open("data.txt", "a") as fl:
        today = datetime.now()
        fl.write(f"\n\n##########################################"
                 f"\n!-------{str(today)}-------!"
                 f"\n##########################################\n")
        fl.close()

    for destination in list_of_destinations:
        new_fly = SearchTickets(destination['from'], destination['to'])
        new_fly.search(searching_from_date, searching_to_date)


multi_destination("03/10/2022", "20/12/2022")