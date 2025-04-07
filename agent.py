from openai import OpenAI
import os
import requests
from dotenv import load_dotenv
from query_executor import execute_sql


load_dotenv()

MCP_SERVER_URL = os.getenv("MCP_SERVER_URL")

client = OpenAI(
    # This is the default and can be omitted
    api_key=os.environ.get("OPENAI_API_KEY"),
)

def query_mysql(natural_language_query: str) -> str:
    schema_context = requests.get(MCP_SERVER_URL).text
    prompt = f"""
    You are a SQL assistant. Given the following table schema:
    {schema_context}

    Convert the following natural language query into MySQL:
    \"{natural_language_query}\"
    """

    completion = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}]
    )
    sql_query = completion.choices[0].message.content.strip()
    result = execute_sql(sql_query)
    return f"SQL: {sql_query}\nResults: {result}"