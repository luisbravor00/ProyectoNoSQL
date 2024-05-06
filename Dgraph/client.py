import os
import pydgraph
import model

DGRAPH_URI = os.getenv('DGRAPH_URI', 'localhost:9080')

def print_menu():
    mm_options = {
        1: "Load Data",
        2: "Erase Data",
        3: "Exit"
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
    model.set_schema(client)

    while(True):
        print_menu()
        option = int(input('Enter your choice: '))
        if option == 1:
            model.load_data_data(client)
        if option == 2:
            person = input("Name: ")
            model.drop_all(client)
            close_client_stub(client_stub)
            exit(0)
        if option == 3:
            exit(0)


if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print('Error: {}'.format(e))