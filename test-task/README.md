# Dataset

Given the dataset with clotning products (./dataset/summer_products.csv). For each products, there are the following fields of interests:
origin_country - country of origing for the products

price - price of the products

rating_count - how many times the product has been rated by user/consumer

rating_five_count - how many times the product has been rated by user/consumer with five stars

# Task
Using Programming Language of your choice (Java/Python), calculate the following metrics for each Country of Origins:
- Average price of product
- What percent of all ratings was five stars

## SQL Representation:
<code>select (sum(rating_five_count) / sum(rating_count)) * 100 as five_percentage, avg(price), origin_country 
from summer_products 
group by origin_country 
order by origin_country</code>
