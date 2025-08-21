from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
from langchain.agents import initialize_agent,tool
from langchain_community.tools import TavilySearchResults
# from langchain_tavily import TavilySearch

import datetime



load_dotenv()



llm = ChatGoogleGenerativeAI(model = "gemini-2.5-flash")
searchTool = TavilySearchResults( max_results=5)

@tool
def get_stem_date(format: str ="%Y-%m-%d %H:%M%S"):
    """returns the current date and time in the specifed format"""
    current_time = datetime.datetime.now()
    formated_time  = current_time.strftime(format)
    return formated_time

tools = [searchTool,get_stem_date]
agent = initialize_agent(llm=llm, tools=tools,agent="zero-shot-react-description", verbose = True, handle_parsing_errors=True   )
agent.invoke("when was isro's last launch and how many days was ti from today")
