## To setup
1. Clone the repo
 ```
 git clone <url>
 ```
### Frontend setup
1.Navigate to frontend folder
```
cd frontend/sql-llm
```
2.Installation
```
npm install
```
3.To start
```
npm start
```
### Backend setup
1.Navigate to backend folder
```
cd backend
```
2.Create Virtual environment
```
python -m venv venv
```
3.Activate for windows
```
venv\Scripts\activate
```
4.Install the requirements
```
pip install -r requirements.txt
```
5.Create .env and paste your gemini apikey
```
GOOGLE_API_KEY=<your api key>
DB_PATH=<>
```
6.Run the app
```
python app.py
```
## DB SCHEMA
![inbox_2473556_23a7d4d8cd99e36e32e57303eb804fff_db-schema](https://github.com/user-attachments/assets/9caf4914-671e-4c15-8be9-a0572b77330c)

## Data source
Download the data and extract it and take the oslist.sqlite put in project backend directory
https://www.kaggle.com/datasets/terencicp/e-commerce-dataset-by-olist-as-an-sqlite-database

## SQL Query Generator Testing

To evaluate the performance of the SQL query generator for the e-commerce dataset, you can use the following example natural language questions. These questions cover a range of scenarios, from basic queries to advanced analysis, allowing for comprehensive testing of the generator's capabilities.

### Basic Query Examples
1. How many orders have been placed in total?  
2. Show me the top 10 products with the highest sales.  
3. List all customers from the state of 'SP'.  
4. What is the average payment value for each payment type?  
5. Find the total number of unique customers.  

### Orders and Customers
1. List the orders along with their customer details where the order status is 'delivered'.  
2. Show the top 5 cities with the most orders.  
3. Find the count of orders by order status.  
4. List customers who have ordered more than 5 times.  

### Payments and Reviews
1. Show the average review score for each product category.  
2. Which orders have more than one payment installment?  
3. Get the total revenue from each payment type.  
4. List all orders that have a review score of 5.  

### Product Information
1. Find the most popular product categories.  
2. List all products with a weight greater than 1000 grams.  
3. Show products with more than 3 photos.  
4. Get the average product dimensions for each category.  

### Advanced Analysis  
1. List all orders where the estimated delivery date was earlier than the actual delivery date.  
2. Find the number of closed leads by each business segment.
3. Find the average delivery time for each product category.  
These queries should serve as a comprehensive set of test cases to validate the accuracy and effectiveness of the SQL query generator.

### Demo
##### video
https://drive.google.com/drive/folders/1ppK_kCJTlBbGvZMdsgV3U4KL1jVJTOi2?usp=drive_link

![Screenshot 2024-11-03 124152](https://github.com/user-attachments/assets/5bfc17d1-2e90-4a30-b866-7437ec17506a)
![Screenshot 2024-11-03 124323](https://github.com/user-attachments/assets/a8b67255-cb2a-4cf8-ab68-38d871358bce)

Techstacks
<div align="center">
  <img src="https://upload.wikimedia.org/wikipedia/commons/a/a7/React-icon.svg" alt="React" width="50" />
  <img src="https://nodejs.org/static/logos/nodejsLight.svg" alt="Node.js" width="50" />
  <img src="https://legacy.python.org/community/logos/python-logo.png" alt="Python" width="50" />
  <img src="https://www.gstatic.com/lamda/images/gemini_sparkle_v002_d4735304ff6292a690345.svg" alt="Gemini" width="50" /> <!-- Replace with actual logo URL -->
</div>

