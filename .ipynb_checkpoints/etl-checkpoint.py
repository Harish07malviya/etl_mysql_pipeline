import pandas as pd
import csv

def extract():
    # Load CSVs into DataFrames
    customers_df = pd.read_csv('customers.csv', header=True)
    customers_df = customers_df.drop_duplicates()
    
    return customers_df, products_df, orders_df, order_items_df

def transform(customers, products, orders, order_items):
    # Join, calculate, clean
    return final_order_details_df

def load(customers, products, orders, order_items, order_details):
    # Save to SQLite database
