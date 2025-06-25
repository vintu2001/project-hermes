import networkx as nx

class CodeQueryTool:
    """
    A tool to perform structured queries on a code knowledge graph.
    This class takes a pre-built graph and provides methods to ask questions about it.
    """
    def __init__(self, graph: nx.DiGraph):
        if not isinstance(graph, nx.DiGraph):
            raise TypeError("A networkx DiGraph object is required.")
        self.graph = graph

    def get_all_files(self) -> list:
        """Returns a list of all file nodes in the graph."""
        files = [node for node, data in self.graph.nodes(data=True) if data.get('type') == 'file']
        return files

    def get_all_classes(self) -> list:
        """Returns a list of all class nodes in the graph."""
        classes = [node for node, data in self.graph.nodes(data=True) if data.get('type') == 'class']
        return classes

    def get_all_functions_in_file(self, file_path: str) -> list:
        """Returns all functions and methods defined directly in a given file."""
        if not self.graph.has_node(file_path):
            return f"Error: File '{file_path}' not found in the graph."
        
        # We find neighbors of the file node that are functions/methods
        neighbors = self.graph.successors(file_path)
        functions = [
            node for node in neighbors 
            if self.graph.nodes[node].get('type') in ['function', 'method']
        ]
        return functions
    
    def get_methods_in_class(self, class_name: str) -> list:
        """Returns all methods defined in a given class."""
        if not self.graph.has_node(class_name):
            return f"Error: Class '{class_name}' not found in the graph."
        
        # We find neighbors of the class node that are methods
        neighbors = self.graph.successors(class_name)
        methods = [
            node for node in neighbors
            if self.graph.nodes[node].get('type') == 'method'
        ]
        return methods

    def find_code_by_name(self, name: str) -> dict:
        """Finds a function, method, or class by its exact name."""
        if self.graph.has_node(name):
            return {
                "name": name,
                "attributes": self.graph.nodes[name]
            }
        return {"error": f"Node '{name}' not found."}