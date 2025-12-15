Part 4: Backend Integration

Step 1: Understand Existing Backend
Reviewed the existing FastAPI backend in /backend
Identified /pipelines/parse endpoint for pipeline processing


Step 2: Enable Frontend–Backend Communication
Configured CORS middleware in FastAPI
Allowed frontend to send requests to backend without CORS errors


Step 3: Update Frontend Submit Logic
Updated /frontend/src/submit.js
On submit button click:
Sent pipeline nodes and edges to backend /pipelines/parse endpoint
Used POST request with pipeline data as payload


Step 4: Define Backend Request Handling
Updated /pipelines/parse endpoint in backend/main.py
Extracted nodes and edges from request body


Step 5: Calculate Pipeline Metrics
Implemented logic to calculate:
Total number of nodes
Total number of edges


Step 6: DAG Validation Logic
Implemented Directed Acyclic Graph (DAG) check
Verified whether the pipeline contains any cycles
Ensured pipeline follows valid DAG structure

Step 7: Backend Response Format
Returned response in required format:
{
  "num_nodes": int,
  "num_edges": int,
  "is_dag": bool
}

Step 8: Frontend Alert Integration
Displayed alert when backend response is received
Alert shows:
Number of nodes
Number of edges
Whether pipeline is a DAG
Made response user-friendly and easy to understand

Step 9: Final Testing
Tested full flow:
Create pipeline on frontend
Submit pipeline
Receive backend validation alert
Verified correct counts and DAG detection