from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_nvidia_ai_endpoints import ChatNVIDIA
from dotenv import load_dotenv

load_dotenv()

generation_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "your are a twitter techie influencer assistant tasked with writing excellent twitter posts"
            "generate the best twitter post possible for the user's request"
            "if the user provides critique, respond with a arevised version of tour previous attemt",
        ),
        MessagesPlaceholder(variable_name="messages")
    ]
)

reflection_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "u are a viral twitter influencer grading a atweet. genrate crtique and recommndations for the user's tweet "
            "always provide detailed recomendation , including request for length, virality , style , etc",
        ), 
        MessagesPlaceholder(variable_name="messages")
    ]
)


# llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash")
llm = ChatNVIDIA(model="mistralai/mixtral-8x22b-instruct-v0.1")
generation_chain = generation_prompt | llm
reflection_chain = reflection_prompt| llm