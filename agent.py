import os
import openai
from openai import OpenAI
from agents import Agent, tool
from model_context import model
from query_executor import execute_sql


@tool
def query_mysql(natural_language_query: str) -> str:
    """
    Converts human language to SQL using the model context and runs it.
    """
    prompt = f"""
    You are a SQL assistant. Given the following table schema:
    {model.describe()}

    Convert the following natural language query into MySQL:
    "{natural_language_query}"
    """
    response = OpenAI().chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )
    sql_query = response.choices[0].message.content.strip()
    result = execute_sql(sql_query)
    return f"SQL: {sql_query}\nResults: {result}"

agent = Agent(tools=[query_mysql])
