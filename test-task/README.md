# Dataset

Given the dataset with clothing products (summer_products.csv). For each product, there are the following fields of interests:
origin_country - country of origin for the products

price - price of the products

rating_count - how many times the product has been rated by user/consumer

rating_five_count - how many times the product has been rated by user/consumer with five stars

# Task
Using Programming Language of your choice (Java/Python/Scala), calculate the following metrics for each Country of Origins:

- Average price of product
- Share of five star products

# SQL Representation:
<code>select avg(price), (sum(rating_five_count) / sum(rating_count)) * 100 as five_percentage, origin_country
from summer_products
group by origin_country
order by origin_country</code>

# Timeline
Please send back a link to your public repository with your source code within the next 3 business days.  
