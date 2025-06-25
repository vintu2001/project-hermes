import ast
import networkx as nx

class CodeParser:
    """
    A dedicated class to parse Python code.
    It takes an existing graph and adds information about a single file to it.
    """
    def __init__(self, graph: nx.DiGraph):
        # This parser will work on a graph that is passed to it from the outside.
        self.graph = graph

    def parse_file_and_add_to_graph(self, file_path: str, file_content: str):
        """
        Parses the content of a single Python file and updates the graph.
        """
        try:
            # Parse the file content into an Abstract Syntax Tree
            tree = ast.parse(file_content)
            
            # Add the file itself as a top-level node
            self.graph.add_node(file_path, type='file')

            # Iterate through all top-level statements in the file
            for node in tree.body:
                # If it's a function at the top level
                if isinstance(node, ast.FunctionDef):
                    func_name = node.name
                    self.graph.add_node(func_name, type='function', file=file_path)
                    self.graph.add_edge(file_path, func_name, type='contains')
                
                # If it's a class
                elif isinstance(node, ast.ClassDef):
                    class_name = node.name
                    self.graph.add_node(class_name, type='class', file=file_path)
                    self.graph.add_edge(file_path, class_name, type='contains')
                    
                    # Iterate through the body of the class to find methods
                    for body_item in node.body:
                        if isinstance(body_item, ast.FunctionDef):
                            method_name = body_item.name
                            method_full_name = f"{class_name}.{method_name}"
                            self.graph.add_node(method_full_name, type='method', file=file_path)
                            self.graph.add_edge(class_name, method_full_name, type='defines_method')

        except Exception as e:
            print(f"    [!] Failed to parse {file_path}: {e}")