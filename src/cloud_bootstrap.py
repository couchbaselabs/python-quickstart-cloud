import os
import time

from dotenv import load_dotenv

from couchbase_cloud import CouchbaseCloud
from cloud_helpers import *


def main():
    # Load environment variable
    load_dotenv()
    access_key = os.getenv("CBC_ACCESS_KEY")
    access_secret = os.getenv("CBC_SECRET_KEY")
    url = os.getenv("CBC_URL")

    # Edit this part to manually work on specific cloud or project or cluster
    # cloud_id = ""
    # project_id = ""
    # cluster_id = ""

    cloud = CouchbaseCloud(access_key, access_secret, url)

    # Ensure that the cloud is established
    cloud_id, cloud_provider = get_cloud_status(cloud)
    if not (cloud_id or cloud_provider):
        print(
            "Ensure that the Cloud is connected. \nCheck the details here:https://docs.couchbase.com/cloud/get-started/deploy-first-cluster.html#connect-a-cloud"
        )
        exit()

    print(f"Cloud ID: {cloud_id}")
    print(f"Cloud Provider: {cloud_provider}")

    # Create Project to host cluster
    project_name = os.getenv("CBC_PROJECT")
    project_id = create_project(cloud, project_name)
    if not project_id:
        print("Project Not Created")
        exit()
    print(f"Project Created with ID: {project_id}")

    # Create cluster
    cluster_name = os.getenv("CBC_CLUSTER")
    create_cluster(cloud, cluster_name, cloud_id, project_id)

    # Get cluster ID
    cluster_id = get_clusters(cloud)
    if not cluster_id:
        print("Cluster Creation Unsuccessful. Please try again")
        exit()
    print(f"Cluster Created with ID: {cluster_id}")

    # Check if the cluster is ready for 30 minutes
    timeout = 30
    while timeout > 0:
        res, success = check_cluster_ready(cloud, cluster_id)
        if success:
            res_json = res.json()
            status = res_json["status"]
            if status == "ready":
                print("Cluster is ready")
                break
            else:
                print("Checking again in a minute...")
                time.sleep(60)
                timeout -= 1
        else:
            print("Cluster not accessible. Please check the Cloud Environment")
            exit()

    # Enable access to the cluster
    cluster_access = enable_access_to_cluster(cloud, cluster_id)
    if not cluster_access:
        print("Enabling access to cluster failed.")
        exit()

    # Create Database User for SDK
    username = os.getenv("USERNAME")
    password = os.getenv("PASSWORD")
    user_creation = create_database_user(cloud, cluster_id, username, password)
    if not user_creation:
        print("User not created. Please try again")
        exit()

    print(f"Database access URL: {cluster_id}.dp.cloud.couchbase.com")

    # # Delete Cluster
    # delete_status = delete_cluster(cloud, cluster_id)
    # if delete_status:
    #     print("Cluster deletion initiated")
    # else:
    #     print("Cluster deletion not successful. Please try again")
    #     exit()


if __name__ == "__main__":
    main()
