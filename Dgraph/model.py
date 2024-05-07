import pydgraph
import json
import csv

def define_schema(client):

    schema = """
    type Passenger {
        transit
        reason
        checked_bags
        carry_on
        stay
        gender
        ticket
        customer_id
        age
    }

    transit: string @index(exact) .
    reason: string .
    checked_bags: int .
    carry_on: int .
    stay: bool .
    gender: string .
    ticket: [uid] @reverse .
    customer_id: string .
    age: int .

    type Flight {
        connection
        wait
        duration
        airline
        dest
        to
        flight_id
        day
        month
        year
    }

    connection: bool .
    wait: string .
    duration: string .
    airline: string @index(exact) .
    dest: [uid] @reverse .
    to: string .
    flight_id: string .
    day: int .
    month: int .
    year: int .

    type Airport {
        airport_code
        airport_name
        country
        city
    }

    airport_code: string @index(exact) .
    airport_name: string @index(trigram) .
    country: string .
    city: string .

    """

    return client.alter(pydgraph.Operation(schema=schema))

def load_data(client):
    txn = client.txn()
    try:
        data = []
        csv_filename = 'Data/flightsData.csv'

        with open(csv_filename) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            next(csv_reader)

            for row in csv_reader:
                (
                    transit, reason, checked_bags, carry_on, stay, gender, ticket, customer_id, age, connection, wait, duration, airline, dest, to, flight_id, day, month, year, airport_code, airport_name, country, city
                ) = row

                passenger_data = {
                    'dgraph.type': 'Passenger',
                    'transit': transit.strip(),
                    'reason': reason.strip(),
                    'checked_bags': int(checked_bags.strip()),
                    'carry_on': int(carry_on.strip()),
                    'gender': gender.strip(),
                    'ticket': [
                        {
                            'connection': connection.strip(),
                            'wait': wait.strip(),
                            'duration': duration.strip(),
                            'airline': airline.strip(),
                            'dest': [
                                {
                                    'airport_code': airport_code.strip(),
                                    'airport_name': airport_name.strip(),
                                    'country': country.strip(),
                                    'city': city.strip()
                                }
                            ],
                            'to': to.strip(),
                            'flight_id': flight_id.strip(),
                            'day': int(day.strip()),
                            'month': int(month.strip()),
                            'year': int(year.strip()),
                        }
                    ],
                    'customer_id': customer_id.strip(),
                    'age': int(age.strip()),

                }
                data.append(passenger_data)

            response = txn.mutate(commit_now=True, set_obj=data)
            print(f"Response: {response}")
            

    finally:
        txn.discard()

###define querys later
##hi

def select_all(client):
    query = """
        {
             passengers(func: has(transit)) {
                transit
                reason
                age
                ticket {
                    flight_id
                    connection
                    wait
                    airline
                    to
                    day
                    month
                    year
                    dest {
                    airport_code
                    airport_name
                    country
                    city
                    }
                }
            }
        }
    """

    res = client.txn(read_only=True).query(query)
    allNodes = json.loads(res.json)

    print(f"-----------All data----------")
    print(f"{allNodes}")

    return 



def drop_all(client):
    return client.alter(pydgraph.Operation(drop_all=True))