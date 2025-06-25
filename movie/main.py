# This library gives us access to Operating System utilites, ie. loading the env variables.
import os

# This is where we will put our program code.
import omdb_exporter
from dotenv import load_dotenv

# This function reads the .env file and gives us environment variables
load_dotenv()

def main():
    # Loads API KEY from .env file
    API_KEY = os.getenv("OMDB_API_KEY")
    print("Hello from Movie Exporter!")


if __name__ == "__main__":
    main()
