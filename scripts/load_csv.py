import pandas as pd
import sqlite3


import sqlite3

def db_connection():
    try:
        connection = sqlite3.connect('instance/ships.db')
        return connection
    except Exception as e:
        print("Error while db connection: ",e)
        if connection:
            connection.close()
    return None


def load_csv_to_database(csv_file,db_connection):
    try:
        # Assuming csv file is headerless and in rigt order
        column_names = ['IMO_number', 'timestamp', 'longitude', 'latitude']
        df = pd.read_csv(csv_file,names=column_names)
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        df.to_sql('ship_positions', con=db_connection, if_exists='append', index=False)
    except Exception as e:
        print(f"Error while data ingestion: {e}")
        raise e



if __name__ == '__main__':  
    # path_to_csv = input("Enter your csv file path: ")
    load_csv_to_database(csv_file="scripts/positions (3).csv",db_connection=db_connection())