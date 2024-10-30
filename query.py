from dotenv import load_dotenv
import streamlit as st
import os
import sqlite3
import google.generativeai as genai

# Load environment variables
load_dotenv()

# Configure GenAI Key
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Function to load Google Gemini Model and provide queries as response
def get_gemini_response(question, prompt):
    model = genai.GenerativeModel('gemini-pro')  # Check if model initialization is correct
    response = model.generate_content([prompt, question])
    return response.text.strip()  # Remove extra whitespace

# Function to retrieve query results from the database
def read_sql_query(sql, db):
    try:
        conn = sqlite3.connect(db)
        cur = conn.cursor()
        cur.execute(sql)
        rows = cur.fetchall()
        conn.commit()
        return rows
    except sqlite3.Error as e:
        return f"An error occurred: {e}"
    finally:
        conn.close()

# Define the prompt text
prompt="""

You are an expert in converting English questions to SQL queries!

The e-commerce dataset has the following tables with their relationships:

1. **customers**: Contains information about each customer, including:
   - `customer_id`: Primary key for customer records.
   - `customer_unique_id`, `customer_zip_code_prefix`, `customer_city`, `customer_state`.

2. **orders**: Holds order details linked to customers, with columns:
   - `order_id`: Primary key for each order.
   - `customer_id`: Foreign key linking to `customers`.
   - `order_status`, `order_purchase_timestamp`, `order_approved_at`, `order_delivered_carrier_date`, `order_delivered_customer_date`, `order_estimated_delivery_date`.

3. **order_items**: Records each item in an order, with columns:
   - `order_id`: Foreign key linking to `orders`.
   - `order_item_id`, `product_id`, `seller_id`, `shipping_limit_date`, `price`, `freight_value`.

4. **order_payments**: Stores payment details for orders, including:
   - `order_id`: Foreign key linking to `orders`.
   - `payment_sequential`, `payment_type`, `payment_installments`, `payment_value`.

5. **order_reviews**: Contains reviews for each order, with columns:
   - `review_id`, `order_id` (Foreign key to `orders`), `review_score`, `review_comment_title`, `review_comment_message`, `review_creation_date`, `review_answer_timestamp`.

6. **geolocation**: Provides location information, including:
   - `geolocation_zip_code_prefix`, `geolocation_lat`, `geolocation_lng`, `geolocation_city`, `geolocation_state`.

7. **products**: Holds information about products, including:
   - `product_id`, `product_category_name`, `product_name_lenght`, `product_description_lenght`, `product_photos_qty`, `product_weight_g`, `product_length_cm`, `product_height_cm`, `product_width_cm`.

8. **product_category_name_translation**: Maps `product_category_name` to English, with columns:
   - `product_category_name`, `product_category_name_english`.

9. **sellers**: Contains information on sellers, with columns:
   - `seller_id`, `seller_zip_code_prefix`, `seller_city`, `seller_state`.

10. **leads_qualified** and **leads_closed**: These tables hold information about qualified leads and closed leads, used for tracking sales performance, with columns including:
    - `mql_id`, `seller_id`, `first_contact_date`, `landing_page_id`, `origin`, `won_date`, `business_segment`, `lead_type`, etc.

When generating SQL queries:
- Ensure the query matches the specific columns and relationships in this schema.
- Avoid referencing non-existent columns like "quantity" unless explicitly defined.
- For common queries:
  - Total number of orders: `SELECT COUNT(*) FROM orders;`
  - Fetch top 10 products based on total quantity sold: `SELECT product_id, SUM(order_item_id) AS total_items_sold FROM order_items GROUP BY product_id ORDER BY total_items_sold DESC LIMIT 10;`
  - Fetch customer details with order and payment info: `SELECT * FROM customers c JOIN orders o ON c.customer_id = o.customer_id JOIN order_payments op ON o.order_id = op.order_id WHERE c.customer_id = <id>;`

The SQL code should not have ``` at the beginning or end, and the word "SQL" should not be in the output.

"""

# Path to the SQLite database
db_path = r"C:\LinarcTask\olist.sqlite"

# Streamlit App
st.title("SQL Query Generator for E-commerce Dataset")

# Input for natural language question
question = st.text_input("Ask your question:", key="input")
submit = st.button("Run Query")

if submit and question:
    response = get_gemini_response(question, prompt)
    st.write("Generated SQL Query:")
    st.code(response)  # Display generated SQL query in code formatting for clarity
    
    query_response = read_sql_query(response, db_path)  # Execute the query against the database
    st.subheader("Results:")
    
    if isinstance(query_response, str):  # Check if there's an error
        st.error(query_response)
    else:
        if query_response:  # Check if there are any results
            #for row in query_response:
            st.dataframe(query_response)
        else:
            st.write("No results found.")








