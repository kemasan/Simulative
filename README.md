# Automated ETL Pipeline: Robust Sales Data Integration

🎯 **The Business Question:** "How can we ensure reliable, daily synchronization of sales data from distributed sources into a centralized database without manual intervention or data duplication?"

In retail operations, sales data often arrives from various POS terminals as fragmented CSV files. Manually processing these files is inefficient and prone to human error. This project automates the "Load" part of an ETL pipeline, ensuring that business intelligence reports always rely on a "Single Source of Truth" that is updated automatically every night.

## 📊 Methodology

I built a resilient Python-based integration layer that connects local data sources to a PostgreSQL environment:
* **Automated Discovery:** The script scans the data directory for new CSV entries using the `os` and `pandas` libraries.
* **Relational Mapping:** Raw transaction data is mapped to a structured SQL schema (`doc_id`, `item`, `category`, `amount`, `price`, `discount`).
* **Scheduled Execution:** Using **Crontab**, the system is configured to execute at specific intervals, ensuring zero-touch operations.

## 🧠 Strategic Assumptions

* **Data Integrity:** I assume that a unique business transaction is defined by the combination of a Document ID and an Item name.
* **Schema Consistency:** The framework assumes that incoming CSV files maintain a consistent header format to ensure successful mapping.
* **Environment Stability:** I assume the host machine is active during the scheduled Cron window to trigger the Python interpreter.

## ⚖️ Risk Trade-offs & Analysis

* **Hard vs. Soft Constraints:** I implemented a **Hard Unique Constraint** in PostgreSQL (`sales_unique_doc_item`). 
    * *Trade-off:* While this prevents any revenue double-counting, it causes the script to reject updates to existing records. 
    * *Decision:* For this financial context, preventing duplicates is more critical than allowing mid-day price corrections.
* **Local vs. Cloud Storage:** The system processes files from a local directory. 
    * *Trade-off:* This is cost-effective and fast for small-to-medium datasets but would require migration to S3/Blob storage for a globally distributed enterprise.

## 🔄 Sensitivity Analysis

* **Conclusion Change:** If the business logic changes to allow multiple identical items in one receipt, the `UNIQUE` constraint must be expanded to include a `serial_number` column to avoid "False Positive" duplication errors.
* **Actionable Insight:** The current `UniqueViolation` logging provides an immediate audit trail, allowing managers to identify which source files are being sent redundantly.

## 🛠️ Tech Stack

* **Language:** Python
* **Database:** PostgreSQL
* **Libraries:** Pandas, Psycopg2, Configparser
* **Automation:** Crontab (Linux/macOS)

---

## ⚙️ Instructions for Setting Up on a New Machine

### 1. Database Preparation
Install PostgreSQL and create a database named `shop`. Execute the following query to create the table and set up uniqueness:
```sql
CREATE TABLE sales (
    doc_id VARCHAR(50),
    item VARCHAR(255),
    category VARCHAR(100),
    amount DECIMAL(10, 2),
    price DECIMAL(10, 2),
    discount DECIMAL(10, 2)
);

ALTER TABLE sales ADD CONSTRAINT sales_unique_doc_item UNIQUE (doc_id, item);
```

### 2. Environment Configuration 
Create a `config.ini` file in the project root directory (use `config.ini.example` as a template):
```ini
[Database]
HOST = localhost
DATABASE = shop
USER = your_user_name
PASSWORD = your_password
```

### 3. Installing Dependencies
Run the following command in your terminal:

```bash
pip install pandas psycopg2-binary
```

### 4. Automation (Linux/macOS)
To set up a daily job (e.g., at 11:20), run `crontab -e` and add the following line:
```bash
20 11 * * * /path/to/your/venv/bin/python /path/to/your_project/run_code.py
```
