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
