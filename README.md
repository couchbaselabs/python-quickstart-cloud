# Quickstart in Couchbase Cloud with Python

### Prerequisites

- [Python v3.9](https://www.python.org/downloads/) installed

### How to Run

- Create [Couchbase Cloud](https://docs.couchbase.com/cloud/get-started/create-account.html) Account.
- [Connect your Cloud](https://docs.couchbase.com/cloud/get-started/deploy-first-cluster.html#connect-a-cloud) to Couchbase Cloud to create the Virtual Private Cloud (VPC) to manage the clusters in your cloud. Currently, AWS & Azure are supported. This operation will take a few minutes to finish.
- [Generate an API Key](https://docs.couchbase.com/cloud/public-api-guide/using-cloud-public-api.html) (Access Key and Secret) for the Couchbase Cloud Account. This is used by the script to create the cluster in the following steps.
- Install the dependencies for the script

  `pip install -r requirements.txt`

- Setup the environment variables to bootstrap the cloud settings. This can be done by copying the `.env.example` file and filling it out the variables.

Variables and their description

    CBC_ACCESS_KEY: API Access Key for the Couchbase Cloud Account
    CBC_SECRET_KEY: API Secret Key for the Couchbase Cloud Account
    CBC_URL: The end point for the Couchbase Cloud API. It should be https://cloudapi.cloud.couchbase.com unless it changes
    CBC_PROJECT: Name of the project to be created in Couchbase Cloud
    CBC_CLUSTER: Name of the cluster to be created in Couchbase Cloud
    USERNAME: Username of the Database User to be created in Couchbase Cloud
    PASSWORD: Password of the Database User to be created in Couchbase Cloud
    BUCKET: Set to `couchbasecloudbucket` the default bucket in Couchbase Cloud. If this is changed, the bucket needs to be created on Couchbase Cloud before running the script.
    COLLECTION: Set to `_default` until Couchbase 7 is released on Cloud
    SCOPE: Set to `_default` until Couchbase 7 is released on Cloud

- Run the script `cloud_bootstrap.py`. The script perfroms the following functionality

  - Check if the cloud (AWS/Azure) is connected to the Couchbase Cloud account.
  - Create the project in Couchbase Cloud account.
  - Create the cluster in the project in Couchbase Cloud account. This process will take a bit of time (upto 30 minutes) as the resources are being created in your cloud.
  - Enable access to the cluster from everywhere.
  - Create the Database Users to access the Cluster.
  - Optionally, you can also delete the cluster by uncommenting the relevant part of the code and inserting the cluster id manually.

- The script will output the URL to access the Cluster in the end. This can be used to connect to the Cluster running in Couchbase Cloud from your machine. Additionally, the cloud, project and cluster ids are also printed on the console after their creation.
  Example:`Database access URL: cc260b0d-0aba-4038-a846-442d9279117c.dp.cloud.couchbase.com`

### How to Proceed

- You can run the flask application `app.py` after adding the `DB_HOST` to the `.env` file with the URL obtained in the bootstrap process.

- For more detailed instructions on the application, please check [`README_APP.md`](README_APP.md)

### Known Issues

- The first cloud connected to the account is used.
- The instances created are hardcoded to AWS m5.xlarge. All of them will run the data, query and index services.
- If multiple clusters are associated with the same project, only the first cluster will be used by the script.
- The cluster is accessible from any IP.

### Notes

- The Couchbase Cloud is free to try but the resources being used from your cloud provider are charged by your cloud provider.
