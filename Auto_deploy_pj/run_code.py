import os
import pandas as pd
import configparser
from pgdb import PGDatabase
import logging 

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.FileHandler("etl_log.log"),
        logging.StreamHandler()
    ]
)

def load_data_to_db():
    logging.info("Start of the data upload process")
    # 1. Read config
    config = configparser.ConfigParser()
    
    # Automatically detect the path to the folder containing the script
    base_path = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(base_path, 'config.ini')
    
    config.read(config_path)
    
    # Ensure that the section is actually loaded
    if 'Database' not in config:
        logging.error(f"The [Database] section was not found!")
        logging.error(f"Path to the file: {config_path}")
        logging.error(f"Sections found: {config.sections()}")
        return

    creds = config['Database']
    
    # 2. Connecting to the database
    try: 
        db = PGDatabase(
            host=creds['HOST'],
            database=creds['DATABASE'],
            user=creds['USER'],
            password=creds['PASSWORD']
        )
        logging.info("The database connection was successful.")
    except Exception as e:
        logging.critical(f"Unable to connect to the database: {e}")
        return
    
    # 3. Setting the path to the data folder
    data_path = os.path.join(base_path, 'data')
    
    if not os.path.exists(data_path):
        logging.error(f"The “data” folder was not found at the path: {data_path}")
        return

    all_files = os.listdir(data_path)
    # To ignore unnecessary files and select only those that match the “shop_cash.csv” pattern.
    csv_files = [f for f in all_files if f.endswith('.csv') and '_' in f]
    
    logging.info(f"Files found to be processed: {len(csv_files)}")
    for file in csv_files:
        # Building the full path to the CSV file
        file_full_path = os.path.join(data_path, file)
        logging.info(f"File processing: {file}")
        
        try:
            df = pd.read_csv(file_full_path)
            rows_inserted = 0
            
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
                rows_inserted += 1
            
            logging.info(f"The file {file} has been successfully uploaded. Rows: {rows_inserted}")
                
        except Exception as e:
            logging.error(f"Processing error {file}: {e}")

    logging.info("The ETL process is complete")
    

if __name__ == "__main__":
    load_data_to_db()

