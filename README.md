# usage-agent



### mysql-query-agent/README.md

# MySQL Query Agent

This project allows users to query a MySQL database using natural language. It leverages:

- **OpenAI Agents SDK** for agent orchestration
- **modelcontextprotocol/python-sdk** for describing SQL schema
- **OpenAI LLM** for natural language to SQL conversion
- **MySQL Connector** for executing queries

---

## 🧰 Requirements

```bash
pip install -r requirements.txt
```

Or run with Docker:

```bash
docker-compose up --build
```

---

## 🔧 Setup

1. **.env** configuration:

```
MYSQL_HOST=db
MYSQL_USER=root
MYSQL_PASSWORD=yourpassword
MYSQL_DATABASE=testdb
OPENAI_API_KEY=sk-...
```

2. **MySQL Schema**:

```sql
CREATE TABLE Users (
    id INT PRIMARY KEY,
    name VARCHAR(255),
    email VARCHAR(255)
);

CREATE TABLE Orders (
    id INT PRIMARY KEY,
    user_id INT,
    amount INT
);
```

---

## 🚀 Run Example Queries

### Locally:
```bash
python examples.py
```

### Docker:
```bash
docker-compose up --build
```

---

## 📁 Project Structure

```
mysql-query-agent/
├── agent.py              # Agent setup using OpenAI Agents SDK
├── model_context.py      # Data model using modelcontextprotocol
├── query_executor.py     # MySQL query execution
├── examples.py           # Example prompts and queries
├── requirements.txt
├── Dockerfile            # Container for app
├── docker-compose.yml    # Service orchestration
└── .env                  # DB credentials
```

---

## 🧠 Example Prompts

- "List all users and their email addresses."
- "Show all orders above $100."
- "Get the total order amount for each user."

---

## 📦 Files

### `requirements.txt`
```txt
openai
openai-agents
modelcontext
mysql-connector-python
python-dotenv
```

### `Dockerfile`
```Dockerfile
FROM python:3.10-slim

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "examples.py"]
```

### `docker-compose.yml`
```yaml
version: '3.8'

services:
  app:
    build: .
    environment:
      - MYSQL_HOST=db
      - MYSQL_USER=root
      - MYSQL_PASSWORD=yourpassword
      - MYSQL_DATABASE=testdb
      - OPENAI_API_KEY=${OPENAI_API_KEY}
    depends_on:
      - db
    volumes:
      - .:/app

  db:
    image: mysql:8.0
    environment:
      MYSQL_ROOT_PASSWORD: yourpassword
      MYSQL_DATABASE: testdb
    ports:
      - "3306:3306"
    volumes:
      - mysql_data:/var/lib/mysql

volumes:
  mysql_data:
```

### `model_context.py`
```python
from modelcontext import Table, Column, Integer, String, ModelContext

class Users(Table):
    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String)

class Orders(Table):
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    amount = Column(Integer)

model = ModelContext(tables=[Users, Orders])
```

### `query_executor.py`
```python
import mysql.connector
from dotenv import load_dotenv
import os

load_dotenv()

def execute_sql(query: str):
    conn = mysql.connector.connect(
        host=os.getenv("MYSQL_HOST"),
        user=os.getenv("MYSQL_USER"),
        password=os.getenv("MYSQL_PASSWORD"),
        database=os.getenv("MYSQL_DATABASE"),
    )
    cursor = conn.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    columns = [desc[0] for desc in cursor.description]
    conn.close()
    return {"columns": columns, "rows": results}
```

### `agent.py`
```python
import openai
from openai import OpenAI
from openai.agents import Agent, tool
from model_context import model
from query_executor import execute_sql
import os

openai.api_key = os.getenv("OPENAI_API_KEY")

@tool
def query_mysql(natural_language_query: str) -> str:
    """
    Converts human language to SQL using the model context and runs it.
    """
    prompt = f"""
    You are a SQL assistant. Given the following table schema:
    {model.describe()}

    Convert the following natural language query into MySQL:
    \"{natural_language_query}\"
    """
    response = OpenAI().chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )
    sql_query = response.choices[0].message.content.strip()
    result = execute_sql(sql_query)
    return f"SQL: {sql_query}\nResults: {result}"

agent = Agent(tools=[query_mysql])
```

### `examples.py`
```python
from agent import agent

queries = [
    "List all users and their email addresses.",
    "Show all orders above $100.",
    "Get the total order amount for each user.",
]

for query in queries:
    print(f"> {query}")
    print(agent.run(query))
    print()
```

---

You're all set to run the project locally or in Docker. Ideal for a GitHub repo setup!
