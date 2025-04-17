# Graph RAG is creating data for statistics, creating Nodes & Edges. Creating relationships of data and answering complex question.
# networkx or Neo4j are used in it.
# Example :-
## “Who won the last match between India and Pakistan in Asia Cup?”
## Data :
 - Match 1: India vs Pakistan, Asia Cup 2022, Winner: India
 - Match 2: India vs Pakistan, Asia Cup 2023, Winner: Pakistan
 - Match 3: India vs Pakistan, World Cup 2023, Winner: India
 - Match 4: India vs Australia, Asia Cup 2023, Winner: India

## Nodes:
- India
- Pakistan
- Asia Cup
- 2022
- 2023
- Winner: India
- Winner: Pakistan
- Match_X (each match can be a node)

## Edges:
- India -- played --> Match_1
- Match_1 -- event --> Asia Cup
- Match_1 -- year --> 2022
- Match_1 -- winner --> India
- Match_2 -- winner --> Pakistan


## “Who won the last match between India and Pakistan in Asia Cup?”

## it will Filter matches where both India and Pakistan played, then filter again to only those in Asia Cup, Sorts by latest year (2023) & Finds: Match_2, Winner: Pakistan

## Answer : “Pakistan won the last Asia Cup match against India in 2023.”




