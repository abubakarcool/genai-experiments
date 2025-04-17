# Step 1: Install necessary libraries
# pip install openai networkx

import openai
import json
import networkx as nx

# Step 2: Load the dataset
with open("champions_trophy_matches_2017_2025.json") as f:
    matches = json.load(f)


graph = nx.DiGraph() # Step 3: Create the graph

for match in matches:
    match_id = match["match_id"]
    teams = match["teams"]
    winner = match["winner"]
    venue = match["venue"]
    date = match["date"]
    tournament = match["tournament"]
    stage = match["stage"]

    graph.add_node(match_id, type="match", date=date, tournament=tournament, stage=stage)

    for team in teams:
        graph.add_node(team, type="team")
        graph.add_edge(team, match_id, relation="played_in")

    if winner and winner != "None":
        graph.add_edge(match_id, winner, relation="won_by")

    graph.add_node(venue, type="venue")
    graph.add_edge(match_id, venue, relation="venue")

# Step 4: Define a function to query graph

def get_matches_won_by_team(team_name):
    matches = []
    for source, destination, attributes in graph.edges(data=True):
        if attributes.get("relation") == "won_by" and destination == team_name:
            matches.append(source)
    return matches

openai.api_key = "openai key "

def ask_openai(query, context):
    messages = [
        {"role": "system", "content": "You are a cricket expert assistant."},
        {"role": "user", "content": f"Query: {query}\nContext: {context}"}
    ]

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=messages,
        temperature=0.2,
    )
    return response['choices'][0]['message']['content']

# Step 6: Example dynamic query
user_query = "Which matches did India win in Dubai?"

# Find all matches won by India
india_wins = get_matches_won_by_team("India")

# Filter those held in Dubai
matches_in_dubai = []
for match_id in india_wins:
    if graph.nodes[match_id].get("venue") == "Dubai":
        matches_in_dubai.append(match_id)

# Prepare context
context_data = [
    f"Match ID: {m}, Stage: {graph.nodes[m]['stage']}, Date: {graph.nodes[m]['date']}"
    for m in matches_in_dubai
]
context = "\n".join(context_data)

# Ask OpenAI
answer = ask_openai(user_query, context)
print("Answer:", answer)
