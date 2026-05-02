# %%
import pandas as pd
import os
import random
import uuid
from datetime import datetime

def generate_daily_data(n_shops=3):
    # Create a folder named “data” if it doesn't exist
    if not os.path.exists('data'):
        os.makedirs('data')
    
    categories = ['бытовая химия', 'текстиль', 'посуда', 'кухонная утварь']
    
    for shop_num in range(1, n_shops + 1):
        # Emulate two cash registers for each store
        for cash_num in range(1, 3):
            data = []
            # Generate 5–15 random strings for each upload
            for _ in range(random.randint(5, 15)):
                price = random.randint(100, 5000)
                data.append({
                    'doc_id': str(uuid.uuid4())[:12], # Receipt ID
                    'item': f"Товар_{random.randint(1, 100)}",
                    'category': random.choice(categories),
                    'amount': random.randint(1, 10),
                    'price': price,
                    'discount': random.randint(0, int(price * 0.2)) # Up to 20% off
                })
            
            df = pd.DataFrame(data)
            file_name = f"data/{shop_num}_{cash_num}.csv"
            df.to_csv(file_name, index=False)
            print(f"File generated: {file_name}")

if __name__ == "__main__":
    # Hours: Open every day except Sunday (6)
    if datetime.today().weekday() != 6:
        generate_daily_data()
    else:
        print("Today is Sunday; generation is not required.")


