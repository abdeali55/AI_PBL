# Step1: Setup FastAPI backend
from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn

from ai_agent import simple_agent, parse_response

app = FastAPI()

# Step2: Receive and validate request from Frontend
class Query(BaseModel):
    message: str


@app.post("/ask")
async def ask(query: Query):
    try:
        # Use the simple agent instead of complex agent executor
        result = simple_agent(query.message)
        tool_called_name, final_response = parse_response(result)

        # Step3: Send response to the frontend
        return {"response": final_response,
                "tool_called": tool_called_name}
    except Exception as e:
        print(f"Error in ask endpoint: {e}")
        return {"response": "I apologize, but I encountered an error processing your request. Please try again.",
                "tool_called": "Error"}


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)






