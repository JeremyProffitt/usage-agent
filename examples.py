from agent import query_mysql

queries = [
    "Get total number of vans.",
    "Get total number of users.",
    "Get total number of projects.",
    "Get total number of prc events.",
    "Get total number of events for user named Kristy Allgood for the past week"
]

for query in queries:
    print(f"> {query}")
    print(query_mysql(query))
    print()
