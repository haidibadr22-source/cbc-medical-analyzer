# agents.py

import os
import json

from dotenv import load_dotenv

from langchain_openai import ChatOpenAI

from prompts import (
    PARSER_PROMPT,
    VALIDATOR_PROMPT,
    SUMMARY_PROMPT,
)

from utils import clean_json_response

load_dotenv()


# -------------------------------------------------------
# LLM
# -------------------------------------------------------

llm = ChatOpenAI(

    model="gpt-4.1",

    temperature=0,

    api_key=os.getenv("OPENAI_API_KEY")

)

# -------------------------------------------------------
# Parser Agent
# -------------------------------------------------------

def parser_agent(report: str):

    prompt = PARSER_PROMPT.format(
        report=report
    )

    response = llm.invoke(prompt)

    content = response.content

    try:

        data = clean_json_response(content)

        return data

    except Exception:

        raise Exception(
            "Parser Agent returned invalid JSON."
        )


# -------------------------------------------------------
# Validator Agent
# -------------------------------------------------------

def validator_agent(

        report: str,
        extracted_json: dict

):

    prompt = VALIDATOR_PROMPT.format(

        report=report,

        json_data=json.dumps(
            extracted_json,
            indent=4
        )

    )

    response = llm.invoke(prompt)

    return response.content


# -------------------------------------------------------
# Summary Agent
# -------------------------------------------------------

def summary_agent(

        report: str,
        extracted_json: dict

):

    prompt = SUMMARY_PROMPT.format(

        report=report,

        json_data=json.dumps(
            extracted_json,
            indent=4
        )

    )

    response = llm.invoke(prompt)

    return response.content
