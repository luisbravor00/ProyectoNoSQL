import os
import pydgraph
import model

DGRAPH_URI = os.getenv('DGRAPH_URI', 'localhost:9080')

def print_menu():
    mm_options = {
        1: "Load Data",
        2: "Erase Data",
        3: "Select All",
        4: "Passengers above age",
        5: "Passenger using rentals car",
        6: "Search Passengers with different type of transit",
        7: "Airport Recommendation",
        8: "Search flights using an airline",
        9: "Exit"
    }
    for key in mm_options.keys():
        print(key, '--', mm_options[key])

def create_client_stub():
    return pydgraph.DgraphClientStub(DGRAPH_URI)


def create_client(client_stub):
    return pydgraph.DgraphClient(client_stub)


def close_client_stub(client_stub):
    client_stub.close()

def main():
    # Init Client Stub and Dgraph Client
    client_stub = create_client_stub()
    client = create_client(client_stub)

    # Create schema
    model.define_schema(client)

    while(True):
        print_menu()
        option = int(input('Enter your choice: '))
        if option == 1:
            model.load_data(client)
        if option == 2:
            model.drop_all(client)
        if option == 3:
            model.select_all(client)
        if option == 4:
            model.passengers_above_age(client)
        if option == 5:
            model.passengers_using_rental_cars(client)
        if option == 6:
            tType = input("Type of transit: ")
            model.search_passengers_with_transit(client, tType)
        if option == 7:
            model.airportRecommendation(client)
        if option == 8:
            aName = input("Airline: ")
            model.search_flights_with_airline(client, aName)
        if option == 9:
            close_client_stub(client_stub)
            exit(0)


if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print('Error: {}'.format(e))