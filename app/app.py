import os
import json
import asyncio
from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse, HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

from google.antigravity import Agent
from .agent import get_health_agent_config

app = FastAPI(title="Lumina Health - AI Health Coach")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global variables for agent
agent_instance = None
agent_context_manager = None

class ChatRequest(BaseModel):
    message: str

@app.on_event("startup")
async def startup_event():
    global agent_instance, agent_context_manager
    # Set up app data dir inside workspace for persistence and clean logs
    app_data_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".antigravity_health"))
    os.makedirs(app_data_dir, exist_ok=True)
    
    config = get_health_agent_config(app_data_dir=app_data_dir)
    
    # Check for GEMINI_API_KEY
    if not os.environ.get("GEMINI_API_KEY"):
        print("WARNING: GEMINI_API_KEY is not set in environment or .env file.")
        
    # Initialize agent context manager
    agent_context_manager = Agent(config)
    agent_instance = await agent_context_manager.__aenter__()
    print("Lumina Health Agent successfully initialized!")

@app.on_event("shutdown")
async def shutdown_event():
    global agent_context_manager
    if agent_context_manager:
        await agent_context_manager.__aexit__(None, None, None)
        print("Lumina Health Agent shutdown.")

# Import health database helper
from .tools import METRICS_PATH, ORDERED_KITS

@app.get("/api/metrics")
async def get_metrics():
    # Fetch metrics from health_metrics.json
    try:
        if os.path.exists(METRICS_PATH):
            with open(METRICS_PATH, 'r') as f:
                data = json.load(f)
            return JSONResponse(content={"metrics": data})
        else:
            return JSONResponse(status_code=404, content={"message": "Metrics database file not found"})
    except Exception as e:
        return JSONResponse(status_code=500, content={"message": str(e)})

@app.get("/api/orders")
async def get_orders():
    # Return ordered kit statuses
    return JSONResponse(content={"orders": ORDERED_KITS})

@app.post("/api/chat")
async def chat_endpoint(request: ChatRequest):
    if not os.environ.get("GEMINI_API_KEY"):
        async def api_key_error_generator():
            yield "data: " + json.dumps({
                "type": "error", 
                "content": "API Key Missing: Please set your GEMINI_API_KEY in the `.env` file to start chatting."
            }) + "\n\n"
        return StreamingResponse(api_key_error_generator(), media_type="text/event-stream")
        
    async def sse_generator():
        try:
            response = await agent_instance.chat(request.message)
            
            # 1. Stream thought process if present
            if hasattr(response, "thoughts") and response.thoughts:
                async for thought in response.thoughts:
                    yield "data: " + json.dumps({"type": "thought", "content": thought}) + "\n\n"
                    await asyncio.sleep(0.01) # Small sleep for smooth front-end streaming
            
            # 2. Stream final text chunks
            async for chunk in response:
                yield "data: " + json.dumps({"type": "content", "content": chunk}) + "\n\n"
                await asyncio.sleep(0.01)
                
            # 3. Stream updated orders list to trigger frontend refresh
            from . import tools
            kits = getattr(tools, "ORDERED_KITS", [])
            yield "data: " + json.dumps({"type": "orders_update", "orders": kits}) + "\n\n"
            
        except Exception as e:
            yield "data: " + json.dumps({"type": "error", "content": str(e)}) + "\n\n"

    return StreamingResponse(sse_generator(), media_type="text/event-stream")

# Mount static files
static_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "static"))
app.mount("/", StaticFiles(directory=static_dir, html=True), name="static")
