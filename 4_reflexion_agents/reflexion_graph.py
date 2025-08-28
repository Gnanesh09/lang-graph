from langchain_core.messages import BaseMessage, ToolMessage
from langgraph.graph import END,MessageGraph
from typing import List

from chains import revisor_chain,first_responder_chain
from execute_tools import execute_tools

graph = MessageGraph()
graph.add_node("draft", first_responder_chain)
graph.add_node("revisor", execute_tools)
graph.add_node("execute_tools", execute_tools)

graph.add_edge("draft", "execute_tools")
graph.add_edge("execute_tools", "revisor"