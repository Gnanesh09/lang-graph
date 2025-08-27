from typing import Annotated, Sequence, TypedDict
from dotenv import load_dotenv
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage
from langgraph.graph import END, StateGraph
from langgraph.graph.message import add_messages

from chains import generation_chain, reflection_chain

load_dotenv()

# Define state with messages reducer
class State(TypedDict):
    messages: Annotated[Sequence[BaseMessage], add_messages]

GENERATE = "generate"
REFLECT = "reflect"

# Nodes now return partial state updates (not full state mutation)
def generate_node(state: State):
    # Expect generation_chain to read prior messages and return an AIMessage or list of messages
    # Normalize to list[BaseMessage]
    result = generation_chain.invoke({"messages": state["messages"]})
    if isinstance(result, BaseMessage):
        new_messages = [result]
    elif isinstance(result, dict) and "messages" in result:
        # If chain returns {"messages": [...]}
        new_messages = result["messages"]
    elif isinstance(result, Sequence):
        new_messages = list(result)
    else:
        # Fallback: wrap as AIMessage string
        new_messages = [AIMessage(content=str(result))]
    return {"messages": new_messages}

def reflect_node(state: State):
    response = reflection_chain.invoke({"messages": state["messages"]})
    # Ensure reflection is appended as a HumanMessage (mirrors original)
    content = getattr(response, "content", response)
    return {"messages": [HumanMessage(content=content)]}

# Conditional router
def should_continue(state: State):
    return END if len(state["messages"]) > 6 else REFLECT

# Build the graph
builder = StateGraph(State)
builder.add_node(GENERATE, generate_node)
builder.add_node(REFLECT, reflect_node)
builder.set_entry_point(GENERATE)
builder.add_conditional_edges(GENERATE, should_continue)
builder.add_edge(REFLECT, GENERATE)

app = builder.compile()

# Visualize
print(app.get_graph().draw_mermaid())
app.get_graph().print_ascii()

# Invoke
response = app.invoke({"messages": [HumanMessage(content="AI Agents taking over content creation")]})
print(response)
