# data-modeling-on-Cloud
## Introduction 
This work aims to design a Data Warehouse hosted on the Cloud, more specifically using AWS Redshift which is a fully managed, petabyte-scale data warehouse service in the cloud. 
The project enables to acquire new insights manipulating the easy-to-use data residing in the Data Warehouse.

The project demonstrates an ETL pipeline process created to populate the database with raw data which is stored in two S3 Buckets of JSON logs on user activity in the steaming app, as well as a JSON metadata on the songs in their app, which is not an easy way to query the necessary data for particular analysis.

Hence, the solution is to create a star schema of fact and dimension tables optimized for queries on song play analysis. 
Before that, we need to issue SQL COPY command to load data into a staging tables on Redshift , this intermediate part of the ETL process is important especially when we dispose of multiple data sources of different types. For instance we are dealing with the same data type which are JSON files but located into two different S3 buckets 

The solution suggests to create links between the music data set and the users data log in order to understand the users musical preferences and maybe for further analysis, we could infer and asses the music tendency based on the periods of the day or year, or even the relationship between a certain music genre and the user location.

Based on the parallel processing nature of Amazon Redshift nodes, we could make a certain choice regarding the distribution style of the data when creating star schema. Here are links to further information about data distribution style [link](https://www.matillion.com/resources/blog/aws-redshift-performance-choose-the-right-distribution-style)
## Infrastructure as Code to configure the Redshift Cluster
There are several ways to manage clusters. If you prefer a more interactive way of managing clusters, you can use the Amazon Redshift console or the AWS Command Line Interface (AWS CLI). If you are an application developer, you can use the Amazon Redshift Query API or the AWS Software Development Kit (SDK) libraries to manage clusters programmatically. In my case I used the AWS SDK Python Library.
##### Create IAM user:
- Open up your AWS Management Console.
- Under AWS services/Security, Identity & compliance choose IAM.
- On the Dashboard in the left, under Access management choose Users
- Click on Add user, fill in the user name and Select AWS access type as programmatic access.
- Click on "Attach existing policies directly", check "AdministratorAccess" and Click on Next:tags
- Choose not to add tags and hit Next:Review
- Finally click on Create use and download your credentials and put it into a safe place 
- Copy&Paste KEY and SECRET into redshift-configuration.cfg ( which I left it blank for you and please do not publicly expose your credentials)

##### Open IaC-Redshift.ipynb:
This notebook enables to set the infrastructure on AWS:
- Reads the `Redshift-configuration.cfg` which contains your IAM credentials and cluster configuration.
- Creates IAM, Redshift clients
- Creates an IAM role to allow Redshift clusters to call AWS services on your behalf.
- Launches the Redshift Cluster with the following config:
```
{
CLUSTER_IDENTIFIER  = data-modeling-cloud
CLUSTER_TYPE        = multi-node
NUM_NODES           = 4
NODE_TYPE           = dc2.large
}
```
- !!! Do not to clean up the AWS resources in the buttom of the notebook 

## Data modeling
### The project Datasets
The raw data is partitioned into 2 different datasets, one is a subset of real data from the Million Song Dataset, and the other one consists of log files in JSON format which stores activity logs based on the song in the first dataset. You'll be working with two datasets that reside in S3. Here are the S3 links for each:
Song data: s3://udacity-dend/song_data
Log data : s3://udacity-dend/log_data

The files are partitioned by the first three letters of each song's track ID. For example, here are filepaths to two files in this song's dataset:
song_data/A/B/C/TRABCEI128F424C983.json
song_data/A/A/B/TRAABJL12903CDCF1A.json

And below is an example of what a single song file, TRAABJL12903CDCF1A.json, looks like.

{"num_songs": 1, "artist_id": "ARJIE2Y1187B994AB7", "artist_latitude": null, "artist_longitude": null, "artist_location": "", "artist_name": "Line Renaud", "song_id": "SOUPIRU12A6D4FA1E1", "title": "Der Kleine Dompfaff", "duration": 152.92036, "year": 0}

The second dataset consists of log files in JSON format based on the songs in the dataset above. These simulate app activity logs from an imaginary music streaming app based on configuration settings.

The log files in the dataset you'll be working with are partitioned by year and month. For example, here are filepaths to two files in this dataset.
log_data/2018/11/2018-11-12-events.json
log_data/2018/11/2018-11-13-events.json

### Execution Steps
- After launching the Redshift cluster via the `IaC-Redshift.ipynb`, execute the `create_tables.py` to drop and create all needed tables in Redshift.
- The `create_tables.py` imports queries from `sql_queries.py` which contains all sql statements.
### Entity Relationship Diagram
![ERD-Sparkify](https://user-images.githubusercontent.com/47854692/105757705-9bbee980-5f4e-11eb-9033-c8795328f6a6.png)

NOTES:
I used some design table optimization which consist in inserting data with distribution keys and sort key. 
I duplicated the users and songplay table over the cluster nodes as as they are considered as "small table" and thus avoid the shuffling and huge workload between nudes when querying. Feel free to change the distribution style ( ALL, EVEN, KEY), you can also let Redshift take control on distribution over machines ( AUTO distribution).

#####  !!! Do not forget to clean up the AWS resources otherwise you will be charged for a service you did not actually use, to do so you go redshift page and select the cluster you are running and click on action/delete.
