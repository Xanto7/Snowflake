import snowflake.connector
from snowflake.connector.pandas_tools import write_pandas
import pandas as pd
import json

def apply_order_items(row):
    order_items = pd.json_normalize(json.loads(row['total_shipping']))
    order_items['order_id'] = row['order_id']
    return order_items


# Connect to Snowflake
conn = snowflake.connector.connect(
    user="admin",
    password="Admin123",
    account="iogmvev-mw12740",
    warehouse="COPMUTE_WH",
    database="SnowflakeDB",
    schema="PUBLIC"
    )

conn.cursor().execute("USE WAREHOUSE COMPUTE_WH")

# Set options to see all columns and values in terminal
pd.set_option('display.max_columns', None)
pd.set_option('display.max_colwidth', None)

# Read orders.csv file
order_df = pd.read_csv(r'Files\Input\orders.csv', delimiter=';', quoting=3, encoding='latin-1')

# Create orders table
orders_df = order_df[['order_id', 'created_at', 'shop_id', 'merchant_id']]

# Create order_items table
# Normalize json data in total_shipping column, each value as list of order items
# For each order_id can be many order items
order_items_df = pd.concat(order_df.apply(apply_order_items, axis=1).to_list(), ignore_index=True)[['order_id', 'print_provider_id', 'print_provider_sku', 'quantity']]

# Print to console
print("Orders:\n", orders_df)
print("Order items:\n", order_items_df)

# Create tables in Snowflake
write_pandas(conn, orders_df, "orders", auto_create_table=True)
write_pandas(conn, order_items_df, "order_items", auto_create_table=True)