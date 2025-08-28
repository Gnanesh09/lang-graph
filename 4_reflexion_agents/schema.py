from pydantic import BaseModel, Field
from typing import List

class Reflection(BaseModel):
    missing:str = Field(description="critique of what is missing")
    superfluous: str = Field(description="critique of what is superfluous")

class AnswerQuestion(BaseModel):
    """ answer the question """
    answer:str = Field(description="~300 words detailed answer the question")
    search_queries: List[str]= Field(
        description="1-3 search quaries for researching imporvements to adress the critique of your current answer"
    )
    reflection:Reflection = Field(
        description="refection on your initial answeer"
    )



class FinalAnswer_revised(BaseModel):
    """revise your original answer to the question"""
    reference:List[str] = Field(
        description="citiations motivationg to your updated answer"
    )






