from typing import TypedDict, Annotated
from langgraph.graph import add_messages, StateGraph, END
from langchain_groq import ChatGroq
from langchain_core.messages import AIMessage, HumanMessage
from dotenv import load_dotenv
from langgraph.prebuilt import ToolNode
from langchain_tavily import TavilySearch
from langgraph.checkpoint.memory import MemorySaver

load_dotenv()
memory = MemorySaver()
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
    "thread_id": 909009
}}
res1 = app.invoke({
    "messages":HumanMessage(content="hi,i am priyansh from bihar")
}, config=config)
res2 = app.invoke({
    "messages":HumanMessage(content="wht is my name")
}, config=config)

print(res1, "\n")
print(res2)
      
