from llama_index.core.tools import FunctionTool
from llama_index.llms.ollama import Ollama
from llama_index.core.agent import ReActAgent

from .knowledge_graph import build_graph_for_repo
from .code_query_tool import CodeQueryTool

# --- Configuration ---
REPO_URL = "https://github.com/psf/requests.git"
LOCAL_REPO_PATH = "./temp_repo"
TARGET_FOLDER = "src/requests"
# --- One-time Setup: Build the Knowledge Graph and Tools ---
# This code runs ONLY ONCE when the application starts.
# This is a critical optimization. We don't want to rebuild the graph on every query.
print("--- Initializing RAG Engine: Building Knowledge Graph ---")
knowledge_graph = build_graph_for_repo(REPO_URL, LOCAL_REPO_PATH, TARGET_FOLDER)
code_tool = CodeQueryTool(knowledge_graph)
print("--- RAG Engine Initialized Successfully ---")


# --- Tool Definition ---
# We wrap our CodeQueryTool's methods into "FunctionTools".
# This tells the LLM Agent what functions are available for it to use.
# The docstrings inside the functions are very important, as the LLM uses them
# to decide which tool to use for a given question.

all_tools = [
    FunctionTool.from_defaults(
        fn=code_tool.get_all_classes,
        name="get_all_classes",
        description="Use this tool to get a list of all class names in the codebase."
    ),
    FunctionTool.from_defaults(
        fn=code_tool.get_methods_in_class,
        name="get_methods_in_class",
        description="Use this tool to get a list of all method names within a specific class. It takes one argument: 'class_name' (string)."
    ),
    FunctionTool.from_defaults(
        fn=code_tool.get_all_files,
        name="get_all_files",
        description="Use this tool to get a list of all file paths in the codebase."
    ),
    FunctionTool.from_defaults(
        fn=code_tool.find_code_by_name,
        name="find_code_by_name",
        description="Use this tool to find information about a specific function, method, or class by its exact name. It takes one argument: 'name' (string)."
    ),
]

# --- Agent Initialization ---
# We use a ReAct (Reasoning + Acting) Agent. It can reason about which tool to use,
# use the tool, observe the result, and repeat until it has an answer.

# We connect the agent to our local Ollama LLM
llm = Ollama(model="llama3", request_timeout=600.0)

# The System Prompt is the most important part. It's the "job description" for our AI agent.
agent_system_prompt = """
You are an expert software engineering assistant. Your goal is to answer questions about a Python codebase.
You have a set of tools to help you. For any user query, follow these steps:
1.  **Think:** First, think about what the user is asking.
2.  **Choose a tool:** Based on the user's question, choose the best tool from the available list.
3.  **Use the tool:** Call the tool with the correct arguments.
4.  **Observe:** Look at the output from the tool.
5.  **Answer:** Based on the tool's output, provide a clear, concise, and helpful answer to the user in natural language.
Do not make up information. If you cannot find the answer using the tools, say "I could not find the information in the codebase."
"""

# Create the agent
code_agent = ReActAgent.from_tools(all_tools, llm=llm, verbose=True, system_prompt=agent_system_prompt)
