from opensearchpy import OpenSearch
import os

client = OpenSearch(hosts=[os.getenv("OPENSEARCH_HOST")])