import pandas as pd
import random
from faker import Faker

fake = Faker()
Faker.seed(42)
random.seed(42)

# Generate customers
customers = []
for i in range(1, 11):
    customers.append({
        "customer_id": i,
        "name": fake.name(),
        "email": fake.email(),
        "region": fake.state()
    })

# Generate products
categories = ["Electronics", "Books", "Clothing", "Home", "Toys"]
products = []
for i in range(1, 11):
    products.append({
        "product_id": i,
        "name": fake.word().capitalize(),
        "category": random.choice(categories),
        "price": round(random.uniform(10.0, 500.0), 2)
    })

# Generate orders
orders = []
for i in range(1, 21):
    orders.append({
        "order_id": i,
        "customer_id": random.randint(1, 10),
        "order_date": fake.date_between(start_date='-1y', end_date='today')
    })

# Generate order_items
order_items = []
item_id_counter = 1
for order in orders:
    num_items = random.randint(1, 3)
    product_ids = random.sample(range(1, 11), num_items)
    for pid in product_ids:
        order_items.append({
            "item_id": item_id_counter,
            "order_id": order["order_id"],
            "product_id": pid,
            "quantity": random.randint(1, 5)
        })
        item_id_counter += 1

# Convert to DataFrames
customers_df = pd.DataFrame(customers)
products_df = pd.DataFrame(products)
orders_df = pd.DataFrame(orders)
order_items_df = pd.DataFrame(order_items)

# Save to CSVs
customers_df.to_csv("ProjectWeek2/customers.csv", index=False)
products_df.to_csv("ProjectWeek2/products.csv", index=False)
orders_df.to_csv("ProjectWeek2/orders.csv", index=False)
order_items_df.to_csv("ProjectWeek2/order_items.csv", index=False)

print("✅ Sample CSV files generated successfully!")
