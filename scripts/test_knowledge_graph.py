import sys
import os
# This is a bit of a hack to make the script find the hermes_pro module
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from hermes_pro.core.knowledge_graph import build_graph_for_repo

REPO_URL = "https://github.com/psf/requests.git"
LOCAL_REPO_PATH = "./temp_repo"

knowledge_graph = build_graph_for_repo(REPO_URL, LOCAL_REPO_PATH, "src/requests")

print("\n--- Knowledge Graph Stats ---")
print(f"Total Nodes: {knowledge_graph.number_of_nodes()}")
print(f"Total Edges: {knowledge_graph.number_of_edges()}")
print("----------------------------")
