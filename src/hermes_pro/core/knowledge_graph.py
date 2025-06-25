import os
import networkx as nx
from git import Repo
from .code_parser import CodeParser 

def build_graph_for_repo(repo_url: str, local_path: str, target_folder: str = None) -> nx.DiGraph:
    """
    Orchestrates the process of building the knowledge graph for a repository.
    """
    print(f"Cloning or updating repository from {repo_url} into {local_path}...")

    # Step 1: Get the code from GitHub
    if not os.path.exists(local_path):
        Repo.clone_from(repo_url, local_path)
    else:
        print("Repo already exists. Using cached version.")
    print("Cloning complete.")

    # Step 2: Initialize components
    knowledge_graph = nx.DiGraph()
    parser = CodeParser(knowledge_graph) # Pass the empty graph to the parser
    parse_path = os.path.join(local_path, target_folder) if target_folder else local_path

    # Step 3: Walk through files and delegate parsing
    print(f"Starting to parse repository at: {parse_path}")
    for root, _, files in os.walk(parse_path):
        for file in files:
            if file.endswith('.py'):
                file_path = os.path.join(root, file)
                print(f"  -> Processing file: {file_path}")

                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    # Tell the parser to do its job on this file
                    parser.parse_file_and_add_to_graph(file_path, content)

    print(f"--> Repository parsing complete. Found {knowledge_graph.number_of_nodes()} nodes.")
    return knowledge_graph