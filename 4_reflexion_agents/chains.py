from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
import datetime
from schema import AnswerQuestion, FinalAnswer_revised
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_nvidia import ChatNVIDIA
from langchain_core.messages import HumanMessage
from langchain_core.output_parsers.openai_tools import PydanticToolsParser
from dotenv import load_dotenv
load_dotenv()



llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash")
pydantic_parser = PydanticToolsParser(tools=[AnswerQuestion])

# actor agent
actor_promt_template = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """you ar an exprt ai reacearcher. 
            
            current time: {time}
            1. {first_instruction}
            2. reflect and critique your answer , be severe to maximize imporvement
            3. after the reflection, list 1-3  search quaries sepereatly for researching imporvements. and do not include them inside reflection
            """,
        ),
        MessagesPlaceholder(variable_name="messages"),
        ("system","answer the user's question above using the required format" )
    ]
).partial(time =lambda:datetime.datetime.now().isoformat())

first_responder_prompt_template = actor_promt_template.partial(first_instruction="provide the detail ~300 word answer")

first_responder_chain = first_responder_prompt_template | llm.bind_tools(tools=[AnswerQuestion], tool_choice="AnswerQuestion") | pydantic_parser


revise_instruction = """
                    REVISE YOUR PREVIOUSE ANSWER WITH NEW INFORMATION
                    -you should use previous critique to add important information ot answer 
                    -you must include numerical citation in your revised answer to ensure it can be verified
                    -add a "References" section to the bottom of your answer (which does not count towards the word limit). in form of :
                        -[1] https://example.com 
                        -[2] https://example.com 

                    - you should use the previous critique to remove supperfluous information from from your answer and make sure it is not more than 250 words
                     """
revisor_chain = actor_promt_template.partial(
    first_instruction = revise_instruction
)| llm.bind_tools(tools=[FinalAnswer_revised], tool_choice="FinalAnswer_revised")

response = first_responder_chain.invoke({
    "messages": [HumanMessage(content="write a ablog post on how ai can be adopted in healthcare sector")]
})


print(response)