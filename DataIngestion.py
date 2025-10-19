# import csv
# import mysql.connector

# # Config
# csv_file_path = 'customers.csv'
# db_name = 'etl_project_week2'
# db_user = 'root'
# db_password = 'root'
# db_host = 'localhost'
# table_name = 'customers'

# try:
#     # 1. Connect to the database
#     conn = mysql.connector.connect(
#         host=db_host,
#         user=db_user,
#         password=db_password,
#         database=db_name
#     )
#     cursor = conn.cursor()
    
#     # 2. Read the CSV file and handle the header
#     with open(csv_file_path, 'r', encoding='utf-8') as file:
#         csv_data = csv.reader(file)
        
#         # Get the header (column names)
#         header = next(csv_data)
#         num_columns = len(header) 
        
#         # --- NEW STEP: CREATE TABLE IF NOT EXISTS ---
        
#         # Determine the table schema based on your CSV columns (adjust data types as needed)
#         # Assuming all columns are TEXT/VARCHAR for simplicity. Adjust if you have numbers/dates.
#         column_definitions = [f"`{col}` VARCHAR(255)" for col in header]
#         create_table_sql = f"""
#         CREATE TABLE IF NOT EXISTS {table_name} (
#             {', '.join(column_definitions)}
#         );
#         """
        
#         # 1. Clean the SQL query string first
#         cleaned_sql = create_table_sql.strip().replace('\n', ' ')

#         # 2. Print the cleaned string using the f-string
#         print(f"Executing: {cleaned_sql}")
#         cursor.execute(create_table_sql)
#         conn.commit()
#         print(f"Table '{table_name}' ensured to exist.")
        
#         # --- END NEW STEP ---
        
#         # Create the SQL template for insertion
#         columns_sql = ', '.join(f"`{col}`" for col in header) # Use backticks for safer column names
#         placeholders = ', '.join(['%s'] * num_columns)
#         sql_insert = f"INSERT INTO {table_name} ({columns_sql}) VALUES ({placeholders})"
        
#         # 3. Iterate over the CSV rows and execute INSERT
#         row_count = 0
#         for row in csv_data:
#             cursor.execute(sql_insert, tuple(row))
#             row_count += 1
            
#         # 4. Commit changes
#         conn.commit()
        
#         print(f"Successfully imported {row_count} rows into table '{table_name}'.")
    
# except mysql.connector.Error as err:
#     print(f"MySQL Error: {err}")
# except FileNotFoundError:
#     print(f"Error: The CSV file path '{csv_file_path}' was not found.")
# finally:
#     if 'conn' in locals() and conn.is_connected():
#         cursor.close()
#         conn.close()
#         print("MySQL connection is closed")


# Multiple CSV file store in MySQL 
import csv
import mysql.connector

# --- Configuration ---
DB_NAME = 'etl_project_week2'
DB_USER = 'root'
DB_PASSWORD = 'root'
DB_HOST = 'localhost'

# Files and their target table names
FILES_TO_IMPORT = [
    {'csv_path': 'customers.csv', 'table_name': 'customers'},
    {'csv_path': 'order_items.csv', 'table_name': 'order_items'},
    {'csv_path': 'orders.csv', 'table_name': 'orders'},
    {'csv_path': 'products.csv', 'table_name': 'products'},
]

# --- Import Function ---
def import_csv_to_mysql(conn, csv_file_path, table_name):
    """Reads a CSV file and imports its data into a specified MySQL table."""
    try:
        cursor = conn.cursor()

        with open(csv_file_path, 'r', encoding='utf-8') as file:
            csv_data = csv.reader(file)
            try:
                header = next(csv_data)
            except StopIteration:
                print(f"[{table_name}] Skipping: File is empty.")
                return

            num_columns = len(header)
            column_definitions = [f"`{col}` VARCHAR(255)" for col in header]
            create_table_sql = f"""
            CREATE TABLE IF NOT EXISTS {table_name} (
                {', '.join(column_definitions)}
            );
            """
            cleaned_sql = create_table_sql.strip().replace('\n', ' ')
            print(f"[{table_name}] Executing CREATE TABLE: {cleaned_sql}")
            cursor.execute(create_table_sql)
            conn.commit()
            print(f"[{table_name}] Table ensured to exist.")

            columns_sql = ', '.join(f"`{col}`" for col in header)
            placeholders = ', '.join(['%s'] * num_columns)
            sql_insert = f"INSERT INTO {table_name} ({columns_sql}) VALUES ({placeholders})"
            data_to_insert = [tuple(row) for row in csv_data if len(row) == num_columns]

            if data_to_insert:
                cursor.executemany(sql_insert, data_to_insert)
                conn.commit()
                print(f"[{table_name}] Successfully imported {cursor.rowcount} rows.")
            else:
                print(f"[{table_name}] No data rows found to import.")

    except FileNotFoundError:
        print(f"[{table_name}] Error: The CSV file path '{csv_file_path}' was not found.")
    except mysql.connector.Error as err:
        print(f"[{table_name}] MySQL Error: {err}")

# --- Main Execution ---
def main():
    conn = None
    try:
        conn = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )
        print("--- Database connection successful. Starting imports. ---")

        for file_info in FILES_TO_IMPORT:
            print("-" * 50)
            import_csv_to_mysql(conn, file_info['csv_path'], file_info['table_name'])

        print("-" * 50)
        print("✅ All CSV files processed successfully.")

    except mysql.connector.Error as err:
        print(f"Fatal Connection Error: {err}")
    finally:
        if conn and conn.is_connected():
            conn.close()
            print("MySQL connection is closed")

if __name__ == "__main__":
    main()
