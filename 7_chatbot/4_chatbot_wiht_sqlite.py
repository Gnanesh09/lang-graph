from typing import TypedDict, Annotated
from langgraph.graph import add_messages, StateGraph, END
from langchain_groq import ChatGroq
from langchain_core.messages import AIMessage, HumanMessage
from dotenv import load_dotenv
from langgraph.prebuilt import ToolNode
from langchain_tavily import TavilySearch
# from langgraph.checkpoint.memory import MemorySaver
from langgraph.checkpoint.sqlite import SqliteSaver
import sqlite3

load_dotenv()
sqlite_conn  =sqlite3.connect("checkpoint.sqlite",check_same_thread=False )

memory = SqliteSaver(sqlite_conn)
llm = ChatGroq(model="llama-3.3-70b-versatile")

class  BasicChatState(TypedDict):
    messages: Annotated[list, add_messages]

def chatbot(state: BasicChatState): 
    return{
    "messages": [llm.invoke(state["messages"])]
    }


graph  = StateGraph(BasicChatState)
graph.add_node("chatbot", chatbot)
graph.set_entry_point("chatbot")
graph.add_edge("chatbot",END)

app = graph.compile(checkpointer=memory)

config = {"configurable": {
    "thread_id": 9
}}

while True: 
    user_input = input("user: ")
    if user_input.lower() in ["exit", "end","close"]:
        break
    else:
        result = app.invoke({
            "messages": [HumanMessage(content=user_input)]
        }, config=config)
        print(result.get("messages")[-1].content)