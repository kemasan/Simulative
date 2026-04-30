import os
import pandas as pd
import configparser
from pgdb import PGDatabase

def load_data_to_db():
    # 1. Read config
    config = configparser.ConfigParser()
    
    # Automatically detect the path to the folder containing the script
    base_path = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(base_path, 'config.ini')
    
    config.read(config_path)
    
    # Ensure that the section is actually loaded
    if 'Database' not in config:
        print(f"ERROR: The [Database] section was not found!")
        print(f"Path to the file: {config_path}")
        print(f"Sections found: {config.sections()}")
        return

    creds = config['Database']
    
    # 2. Connecting to the database
    db = PGDatabase(
        host=creds['HOST'],
        database=creds['DATABASE'],
        user=creds['USER'],
        password=creds['PASSWORD']
    )
    
    # 3. Setting the path to the data folder
    data_path = os.path.join(base_path, 'data')
    
    if not os.path.exists(data_path):
        print(f"The “data” folder was not found at the path: {data_path}")
        return

    all_files = os.listdir(data_path)
    
    for file in all_files:
        # Шgnore unnecessary files and select only those that match the “shop_cash.csv” pattern.
        if file.endswith('.csv') and '_' in file:
            # Building the full path to the CSV file
            file_full_path = os.path.join(data_path, file)
            print(f"File processing: {file}")
            
            try:
                df = pd.read_csv(file_full_path)
                
                for _, row in df.iterrows():
                    # Use a secure insertion %s
                    query = """
                        INSERT INTO sales (doc_id, item, category, amount, price, discount)
                        VALUES (%s, %s, %s, %s, %s, %s)
                    """
                    values = (
                        row['doc_id'], row['item'], row['category'],
                        row['amount'], row['price'], row['discount']
                    )
                    db.post(query, values)
                
            except Exception as e:
                print(f" Processing error {file}: {e}")

if __name__ == "__main__":
    load_data_to_db()

