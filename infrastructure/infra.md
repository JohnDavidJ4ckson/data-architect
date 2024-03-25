The infrastructure required for the example consists of: comoute resources to show the dashboard, network components to access the database, a database service to provide ETL operations and queries as requested by the frontend, a storage system to secure the data for database operations.

In AWS one needs to create a Virtual Private Cloud (VPC) for networking purposes. The VPC consists of a public and a privete subnet. The database should be protected in a private subnet and the front-end dashboard should be accesible throug a public subnet with its own internet gateway.

Then the Identity Access Management (IAM) system should be used to create the policies and roles that will be used to modify the database, or to retrieve data from the database into the dashboard.

An instance of a database dedicated to the ETL such as Athena (if the data schema is expected to be open) has to be created and it has to be connected to the specific S3 bucket were data will be stored.

The backend services that communicate with external data sources and that send database requests to a front-end dashboard could be implemented in serverless services (Lamba functions)

Cloud Watch could be provisiones in order to monitor the use of infrastructure resources.

A dummy version of the infrastructure described is implemented both in Terraforms HCL, and as a Yaml file as in CloudFormation.
