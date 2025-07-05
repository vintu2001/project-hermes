from fastapi import APIRouter, HTTPException
from ..models.pydantic_models import QueryRequest, QueryResponse
# We now import our powerful code agent
from ..core.rag_engine import code_agent

router = APIRouter()

@router.post("/query", response_model=QueryResponse)
def handle_query(query_request: QueryRequest):
    """
    This endpoint now receives a query and passes it to our Code Agent.
    """
    print(f"API received query: '{query_request.query}'")
    
    try:
        # Pass the user's query directly to the agent's chat method
        agent_response = code_agent.chat(query_request.query)
        
        # The agent's response is an object, we convert it to a string for the answer
        answer = str(agent_response)

        return QueryResponse(answer=answer)
        
    except Exception as e:
        print(f"[ERROR] An error occurred in the agent: {e}")
        raise HTTPException(status_code=500, detail="An error occurred while processing the query with the AI agent.")