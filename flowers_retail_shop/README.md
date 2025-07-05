Title: Flower and Retail shop API

Description: 

This is a simple API for a Flower and retail shop. You can manage business owners, customers, supplier, products and orders. It lets you create, view, update and delete records using easy to understand endpoints. The API uses a PostgresSQL database for storing the data. 

Had a bit of issues of connecting to the Flask run. It was connected to the twitter clone folder. So here’s the run down I did in order for it to work. I had to connect to the Flask container, then I had get into virtual environment. 
Once I was connected to virtual environment. I had to get into the file I need to get to. Pretty much where the my-blog/flower is at.
I had to run this command in the virtual environment in order to remove the twitter clone folder: (venv) root@079cbb756888:/app/Flower_Portfolio/flowers_retail_shop# export FLASK_APP=wsgi.py
After I ran that I run : (venv) root@079cbb756888:/Flower_Portfolio/flowers_retail_shop# flask run --host=0.0.0.0 --port=5000 for it to connect it. 
For there I was able to run API’s
 
My base environment in Insomnia

{
	"base_url": "http://127.0.0.1:5000"
}

Here are the API reference table also including the example URL and parameters base on what I did
 
Endpoint	          Method	Example URL	                   Parameters

/customers	              GET	        http://localhost:5000/customers	   None
/customers	              POST	        http://localhost:5000/customers	   JSON: first_name, last_name, user_id
/customers/<customer_id>  PUT	        http://localhost:5000/customers/1  JSON: fields to update
/customers/<customer_id>  DELETE	    http://localhost:5000/customers/1  None
/products	              GET	        http://localhost:5000/products	   None
/products	              POST	        http://localhost:5000/products	   JSON: name, price, owner_id
/suppliers	              GET	        http://localhost:5000/suppliers	   None
/suppliers	              POST	        http://localhost:5000/suppliers	   JSON: name, contact_name, email, owner_id
/orders	                  GET	        http://localhost:5000/orders	   None
/orders   	              POST	        http://localhost:5000/orders	   JSON: customer_id, order_date, status
/orders/<order_id>	      PUT	        http://localhost:5000/orders/1	   JSON: fields to update
/orders/<order_id>	      DELETE	    http://localhost:5000/orders/1	   None

Retrospective answering of the following questions:

1.How did the project’s design evolve over time? 

The design started with an ER diagram that mapped out the relationships between users, business owners, suppliers, customers, products, and orders. As I was building the API, I added constraints, indexes, and cleaned up the route to make everything work smoothly. I also simplified parts that were complicated first. To be honest, I feel or it looks like the ER diagram evolved into something more like stuff been added or so because of the corrections or changes that are made.
 
2.Did you choose to use an ORM or raw SQL? Why?

I used raw SQL for this project because it gave me more control over the queries and matched the learning goals of the assignment. It help me better understand how the database and API connect. 

3.What future improvements are in store, if any?

In the future, I could add more indexes for performance, improve error handling in the API, and create more advance data visualizations. I might also switch to using an ORM like SQLAlchemy to make the code to maintain. But there are always improvements. Like I always tell my kids “It’s not practice makes perfect. It’s practice makes Improvements” 
