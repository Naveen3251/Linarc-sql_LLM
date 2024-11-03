from flask import Flask, request, jsonify
from dotenv import load_dotenv
import os
import sqlite3
import google.generativeai as genai
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})  

load_dotenv()

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
################################  PROMPT ##################################
prompt="""
You are an expert in converting English questions to SQL queries!

The e-commerce dataset has the following tables with their relationships:

1. *customers*: Contains information about each customer, including:
   - customer_id: Primary key for customer records.
   - customer_unique_id, customer_zip_code_prefix, customer_city, customer_state.

2. *orders*: Holds order details linked to customers, with columns:
   - order_id: Primary key for each order.
   - customer_id: Foreign key linking to customers.
   - order_status, order_purchase_timestamp, order_approved_at, order_delivered_carrier_date, order_delivered_customer_date, order_estimated_delivery_date.

3. *order_items*: Records each item in an order, with columns:
   - order_id: Foreign key linking to orders.
   - order_item_id, product_id, seller_id, shipping_limit_date, price, freight_value.

4. *order_payments*: Stores payment details for orders, including:
   - order_id: Foreign key linking to orders.
   - payment_sequential, payment_type, payment_installments, payment_value.

5. *order_reviews*: Contains reviews for each order, with columns:
   - review_id, order_id (Foreign key to orders), review_score, review_comment_title, review_comment_message, review_creation_date, review_answer_timestamp.

6. *geolocation*: Provides location information, including:
   - geolocation_zip_code_prefix, geolocation_lat, geolocation_lng, geolocation_city, geolocation_state.

7. *products*: Holds information about products, including:
   - product_id, product_category_name, product_name_lenght, product_description_lenght, product_photos_qty, product_weight_g, product_length_cm, product_height_cm, product_width_cm.

8. *product_category_name_translation*: Maps product_category_name to English, with columns:
   - product_category_name, product_category_name_english.

9. *sellers*: Contains information on sellers, with columns:
   - seller_id, seller_zip_code_prefix, seller_city, seller_state.

10. *leads_qualified* and *leads_closed*: These tables hold information about qualified leads and closed leads, used for tracking sales performance, with columns including:
    - mql_id, seller_id, first_contact_date, landing_page_id, origin, won_date, business_segment, lead_type, etc.

When generating SQL queries:
 Ensure that:
- Column names exist in the respective tables strict order .
- Use table aliases consistently to avoid ambiguity.
- Validate that JOIN statements are correctly implemented.
- For ambiguous columns, specify the source table explicitly.
- Ensure the query matches the specific columns and relationships in this schema.
- Avoid referencing non-existent columns like "quantity" unless explicitly defined.
- For common queries:
  - Total number of orders: SELECT COUNT(*) FROM orders;
  - Fetch top 10 products based on total quantity sold: SELECT product_id, SUM(order_item_id) AS total_items_sold FROM order_items GROUP BY product_id ORDER BY total_items_sold DESC LIMIT 10;
  - Fetch customer details with order and payment info: SELECT * FROM customers c JOIN orders o ON c.customer_id = o.customer_id JOIN order_payments op ON o.order_id = op.order_id WHERE c.customer_id = <id>;

The SQL code should not have ``` at the beginning or end, and the word "SQL" should not be in the output.
"""
#######################
def get_gemini_response(question, prompt):
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content([prompt, question])
    return response.text.strip()

def read_sql_query(sql, db):
    conn = None  
    try:
        conn = sqlite3.connect(db)
        cur = conn.cursor()
        cur.execute(sql)
        rows = cur.fetchall()
        conn.commit()
        columns = [desc[0] for desc in cur.description] 
        return {"columns": columns, "rows": rows}
    except sqlite3.Error as e:
        return {"error": str(e)}
    finally:
        if conn:  
            conn.close()


@app.route('/generate-query', methods=['POST'])
def generate_query():
    try:
        data = request.json
        question = data.get('question')
        db_path = os.getenv("DB_PATH")

        if not question or not prompt or not db_path:
            return jsonify({"error": "Missing parameters"}), 400

   
        sql_query = get_gemini_response(question, prompt)
   
        results = read_sql_query(sql_query, db_path)
    
        return jsonify({"sql_query": sql_query, "results": results})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)




