# from fastapi import FastAPI
# from pydantic import BaseModel

# class PipelinePayload(BaseModel):
#     nodes: list
#     edges: list


# def build_adjacency_list(nodes, edges):
#     """Create adjacency list from directed edges."""
#     adjacency = {node: [] for node in nodes}

#     for edge in edges:
#         source = edge.get('source')
#         target = edge.get('target')
#         if source is None or target is None:
#             continue

#         adjacency.setdefault(source, []).append(target)
#         adjacency.setdefault(target, adjacency.get(target, []))

#     return adjacency


# def has_cycle(adjacency):
#     """
#     Detect cycles in a directed graph using DFS with coloring.
#     Returns True if a back edge (cycle) is found.
#     """
#     WHITE, GRAY, BLACK = 0, 1, 2  # unvisited, visiting, visited
#     state = {node: WHITE for node in adjacency}

#     def dfs(node):
#         state[node] = GRAY
#         for neighbor in adjacency.get(node, []):
#             if state.get(neighbor, WHITE) == WHITE:
#                 if dfs(neighbor):
#                     return True
#             elif state[neighbor] == GRAY:
#                 return True  # back edge => cycle
#         state[node] = BLACK
#         return False

#     for node in adjacency:
#         if state[node] == WHITE:
#             if dfs(node):
#                 return True
#     return False


# app = FastAPI()

# @app.get('/')
# def read_root():
#     return {'Ping': 'Pong'}

# @app.post('/pipelines/parse')
# def parse_pipeline(payload: PipelinePayload):
#     num_nodes = len(payload.nodes)
#     num_edges = len(payload.edges)
#     adjacency = build_adjacency_list(payload.nodes, payload.edges)
#     # Empty graph is acyclic by definition; DFS handles both empty and populated graphs.
#     is_dag = not has_cycle(adjacency)

#     return {
#         'num_nodes': num_nodes,
#         'num_edges': num_edges,
#         'is_dag': is_dag,
#     }






from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
from collections import defaultdict, deque

app = FastAPI()

origins = [
    "http://localhost:3000",
    "http://localhost:5173",
    "http://localhost:3001",
    "http://localhost:3002",
    "http://localhost:3003",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Node(BaseModel):
    id: str

class Edge(BaseModel):
    source: str
    target: str

class Pipeline(BaseModel):
    nodes: List[Node]
    edges: List[Edge]

def is_dag(nodes, edges):
    graph = defaultdict(list)
    indegree = {node.id: 0 for node in nodes}

    for edge in edges:
        graph[edge.source].append(edge.target)
        indegree[edge.target] += 1

    queue = deque([n for n in indegree if indegree[n] == 0])
    visited = 0

    while queue:
        node = queue.popleft()
        visited += 1
        for neighbor in graph[node]:
            indegree[neighbor] -= 1
            if indegree[neighbor] == 0:
                queue.append(neighbor)

    return visited == len(nodes)

@app.post("/pipelines/parse")
def parse_pipeline(pipeline: Pipeline):
    return {
        "num_nodes": len(pipeline.nodes),
        "num_edges": len(pipeline.edges),
        "is_dag": is_dag(pipeline.nodes, pipeline.edges),
    }