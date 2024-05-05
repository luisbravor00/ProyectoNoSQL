import argparse
import logging
import os
import requests


# Set logger
log = logging.getLogger()
log.setLevel('INFO')
handler = logging.FileHandler('books.log')
handler.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(name)s: %(message)s"))
log.addHandler(handler)

# Read env vars related to API connection
BOOKS_API_URL = os.getenv("BOOKS_API_URL", "http://localhost:8000")

def main():
    log.info(f"Welcome to books catalog. App requests to: {BOOKS_API_URL}")

    parser = argparse.ArgumentParser()



if __name__ == "__main__":
    main()