import requests
from couchbase_cloud import CouchbaseCloud


def check_response_for_errors(
    res, check_message, status_codes
) -> tuple[requests.Response, bool]:
    """Checks if the response from the requests are succesful or not based on the status_codes provided
    If there is an error, the error reason is reported"""
    success = True
    if res.status_code in status_codes:
        print(f"{check_message} Successful")
    else:
        print(f"{check_message} Failed")
        print(
            f"Status code: {res.status_code}\nError Type:{res.json()['errorType']} \nError Message:{res.json()['message']}"
        )
        success = False
    return res, success


def get_cloud_status(cloud: CouchbaseCloud) -> tuple[str, str]:
    "Checks if the Cloud (AWS/Azure) is connected. It returns the first cloud connected by the user"
    res = cloud.request("/v2/clouds", "GET")
    res, success = check_response_for_errors(res, "Check Cloud Connection", [200])
    cloud_id, cloud_provider = None, None
    if success:
        try:
            res_json = res.json()["data"][0]
            cloud_id = res_json["id"]
            cloud_provider = res_json["provider"]
        except KeyError:
            pass
    return cloud_id, cloud_provider


def create_project(cloud: CouchbaseCloud, project_name: str) -> str:
    """Creates a new project in Couchbase Cloud and returns the project id if successful"""
    res = cloud.request("/v2/projects", "POST", data={"name": project_name})
    res, success = check_response_for_errors(res, "Create Project", [201])
    project_id = None
    if success:
        try:
            res_json = res.json()
            project_id = res_json["id"]
        except KeyError:
            pass
    return project_id


def create_cluster(
    cloud: CouchbaseCloud, cluster_name: str, cloud_id: str, project_id: str
) -> bool:
    """Initiate the creation of a new cluster in Couchbase Cloud.
    Currently the instance used is AWS (m5.xlarge) with storage of 128GB running data, query and index services"""
    res = cloud.request(
        "/v2/clusters",
        "POST",
        data={
            "name": cluster_name,
            "cloudId": cloud_id,
            "projectId": project_id,
            "version": "latest",
            "servers": [
                {
                    "services": ["data", "index", "query"],
                    "size": 3,
                    "aws": {"ebsSizeGib": 128, "instanceSize": "m5.xlarge"},
                }
            ],
        },
    )
    res, success = check_response_for_errors(res, "Create Cluster", [202])
    return success


def get_clusters(cloud: CouchbaseCloud) -> str:
    """Request to get the cluster id for the first cluster in Couchbase Cloud"""
    res = cloud.request("/v2/clusters", "GET")
    res, success = check_response_for_errors(res, "Get Clusters", [200])
    cluster_id = None
    if success:
        res_json = res.json()["data"][0]
        cluster_id = res_json["id"]
    return cluster_id


def check_cluster_ready(
    cloud: CouchbaseCloud, cluster_id: str
) -> tuple[requests.Response, bool]:
    """Request to check if the Cluster is ready to be used in Couchbase Cloud"""
    res = cloud.request(f"/v2/clusters/{cluster_id}", "GET")
    res, success = check_response_for_errors(res, "Get Cluster Status", [200])
    return res, success


def enable_access_to_cluster(cloud: CouchbaseCloud, cluster_id: str) -> bool:
    """Request to enable access to the cluster from the entire world (CIDR 0.0.0.0/1)"""
    # TODO: Change it to a more reasonable IP range or make it temporary

    res = cloud.request(
        f"/v2/clusters/{cluster_id}/allowlist",
        "POST",
        data={
            "cidrBlock": "0.0.0.0/0",
            "ruleType": "permanent",
            "comment": "cluster accesss to all",
        },
    )

    res, success = check_response_for_errors(res, "Enable Cluster Access", [202])

    return success


def create_database_user(
    cloud: CouchbaseCloud, cluster_id: str, username: str, password: str
) -> bool:
    """Request to create the Database User with read write access to all the Buckets in Couchbase Cloud"""
    res = cloud.request(
        f"/v2/clusters/{cluster_id}/users",
        "POST",
        data={
            "username": username,
            "password": password,
            "allBucketsAccess": "data_writer",
        },
    )
    res, success = check_response_for_errors(res, "Create Database User", [201])

    return success


def delete_cluster(cloud: CouchbaseCloud, cluster_id: str) -> bool:
    """Request to delete the cluster from Couchbase Cloud"""
    res = cloud.request(f"/v2/clusters/{cluster_id}", "DELETE")
    res, success = check_response_for_errors(res, "Delete Cluster", [202])

    return success
