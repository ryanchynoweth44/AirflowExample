## Data Pipelines Using Airflow

I previously wrote a [blog and demo](https://ryansdataspot.com/2019/03/14/data-analytics-data-engineering-and-containers/) discussing how and why data engineers should deploy pipeliens using containers. One slight disadvantage to deploying data pipeline containers is managing, monitoring, and scheduling these can be a little bit of a pain. One of the most popular tools out their for solving this is [Apache Airflow](https://airflow.apache.org/). Apache Airflow is a platform to programmitcally develop, schedule, and monitor workflows. Workflows are defined as code, making them easy to maintain, test, deploy, and collaborate across a team. 






Workflows are written in Python but tasks can be in many different forms. 

Airflow workflows are directed acyclic graphs (DAGs) comprised of tasks to be executed on a cadence. 


The airflow scheduler executes your tasks on an array of workers while following the specified dependencies. Rich command line utilities make performing complex surgeries on DAGs a snap. The rich user interface makes it easy to visualize pipelines running in production, monitor progress, and troubleshoot issues when needed.

