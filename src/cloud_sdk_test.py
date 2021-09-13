from couchbase.cluster import Cluster, ClusterOptions
from couchbase.cluster import PasswordAuthenticator
from couchbase.cluster import QueryOptions
from couchbase.management.queries import CreatePrimaryQueryIndexOptions

from dotenv import load_dotenv
import os

######## Update this to your cluster
load_dotenv()
endpoint = os.getenv("DB_HOST")
username = os.getenv("USERNAME")
password = os.getenv("PASSWORD")
bucketName = "couchbasecloudbucket"

#### User Input ends here.


# Initialize the Connection
cluster = Cluster(
    "couchbases://" + endpoint + "?ssl=no_verify",
    ClusterOptions(PasswordAuthenticator(username, password)),
)
cb = cluster.bucket(bucketName)
cb_coll = cb.default_collection()

# Create a N1QL Primary Index (but ignore if it exists)
cluster.query_indexes().create_primary_index(bucketName, ignore_if_exists=True)

# Store a Document
cb_coll.upsert(
    "u:king_arthur",
    {
        "name": "Arthur",
        "email": "kingarthur@couchbase.com",
        "interests": ["Holy Grail", "African Swallows"],
    },
)

# Load the Document and print it
print(cb_coll.get("u:king_arthur").content_as[str])

# Perform a N1QL Query
row_iter = cluster.query(
    "SELECT name FROM %s WHERE $1 IN interests" % (bucketName),
    QueryOptions(positional_parameters=["African Swallows"]),
)

# Print each found Row
for row in row_iter:
    print(row)
