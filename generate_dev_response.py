import os

from dotenv import load_dotenv

from prefect import task
from langchain_core.output_parsers import StrOutputParser
from langchain_community.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

load_dotenv()

model = ChatOpenAI(openai_api_key=OPENAI_API_KEY, model="gpt-3.5-turbo")
parser = StrOutputParser()

pirate_template = """
    Rewrite the following text in pirate language:

    Original Text: {text}
    
    Pirate Version:
    """
pirate_prompt = ChatPromptTemplate.from_template(pirate_template)
pirate_chain = pirate_prompt | model | parser

dev_template = """
    Rewrite the following horoscope as advice specifically for someone with the job title "{job_title}" in software development, engineering, or programming.
    Maintain the horoscope's underlying message, but translate it into humorous, satirical guidance tailored to the responsibilities and experiences of a {job_title}.
    Reference specific scenarios related to their role, mention common tools or workflows (e.g., Git for a Developer, Docker for DevOps, Jupyter for Data Scientists), and use relatable job experiences (e.g., endless debugging for developers, managing pipelines for DevOps, handling data wrangling for Data Scientists).

    Format the response to first mention the horoscope theme (e.g., "Your stars foresee...") and follow up with specific, humorous {job_title} scenarios. 

    Original Horoscope: {text}

    {job_title} Advice:
    """
dev_prompt = ChatPromptTemplate.from_template(dev_template)
dev_chain = dev_prompt | model | parser

@task
def rewrite_horoscope_as_dev(horoscope_text, job_title):
    response = dev_chain.invoke({"text": horoscope_text, "job_title": job_title})
    return response

@task
def rewrite_horoscope_as_pirate(horoscope_text, job_title):
    response = dev_chain.invoke({"text": horoscope_text})
    return response

