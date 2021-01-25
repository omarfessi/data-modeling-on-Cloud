# data-modeling-on-Cloud
## Introduction 
### Infrastructure as Code to configure the Redshift Cluster
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
- After launching the Redshift cluster via the `IaC-Redshift.ipynb`, execute the `create_tables.py` to drop and create all needed tables in Redshift.
- The `create_tables.py` imports queries from `sql_queries.py` which contains all sql statements.
### Entity Relationship Diagram
![ERD-Sparkify](https://user-images.githubusercontent.com/47854692/105757705-9bbee980-5f4e-11eb-9033-c8795328f6a6.png)
