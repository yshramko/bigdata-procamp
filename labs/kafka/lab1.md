## Apache Kafka Lab 1

### Overview
This lab has two parts:
1. Producer side. Here the task is to extend the Apache Nifi lab and publish same messages to Apache Kafka.
2. Consumer side. Implement logic on consumer using programming language of your choice.

### Task Description
On NiFi lessons, the NiFi workflow has been presented, which reads BitCoins transactions data.
A single transaction, converted to a string, looks like the following (where "value" is a default value for data field in Kafka):

```
{
   "data":{
      "id":1297851689496576,
      "id_str":"1297851689496576",
      "order_type":1,
      "datetime":"1605693298",
      "microtimestamp":"1605693298239000",
      "amount":0.014,
      "amount_str":"0.01400000",
      "price":18058.68,
      "price_str":"18058.68"
   },
   "channel":"live_orders_btcusd",
   "event":"order_deleted"
}
```
The goal is to write the BitCoins Transactions data to Kafka, then read this data on consumer side and compute top 10 transactions by `price` field.

## Parts that should be implemented and technical constraints
1. Bash script that creates a topic in Kafka which will be used for bitcoin transactions
    - self descriptive name
    - data is stored in a redundant form i.e. not a single copy
2. Producer side.
    - implemented using Apache Nifi out-of-the-box processors
    - acknowledgement from all brokers is configured
3. Consumer side.
    - implement using your language of choice
    - at least once delivery semantics is implemented
    - on each poll there should be from 100 to 200 records consumed or if there are less then 100
    - compute top 10 bitcoin transactions based on `price` field (ascending) and print them to std out
        - maintain a collection of top 10 transactions from the beginning
        - after each consumer poll update this collection
        - after the update, print collection to the std out.
4. Readme instruction is included on how to build and run your code
