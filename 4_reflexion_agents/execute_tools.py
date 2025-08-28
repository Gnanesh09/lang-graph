import json

from typing import List, Dict, Any
from langchain_core.messages import AIMessage,HumanMessage, BaseMessage,ToolMessage
from langchain_community.tools import TavilySearchResults
from dotenv import load_dotenv


load_dotenv()

tavil_tool = TavilySearchResults(max_results=7)

# function to execute search quaries from answerQuetion tool calls

def execute_tools(state:List[BaseMessage])->List[BaseMessage]:
    last_ai_message:AIMessage = state[-1]

    # extract the tool calss form the ai message
    if not hasattr(last_ai_message,"tool_calls") or not last_ai_message.tool_calls:
        return[]
    
    tool_messages = []
    # process the answerquestion or revise tool calls to extract search quaries 
    tool_messages = []
    for tool_call in last_ai_message.tool_calls:
        if tool_call["name"] in ["AnswerQuestion", "ReviseAnswer"]:
            call_id = tool_call["id"]
            search_quaries = tool_call["args"].get("search_quaries", [])
            query_results= {}
            for query in search_quaries:
                result= tavil_tool.invoke(query)
                query_results[query] = result

            tool_messages.append(
                ToolMessage(
                    content=json.dumps(query_results),
                    tool_call_id = call_id
                )
            )

    return tool_messages






