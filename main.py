import os
from typing import Dict, TypedDict, List
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv

# LangGraph & LangChain imports
from langgraph.graph import StateGraph, END
from langchain_groq import ChatGroq
from langchain_community.tools import DuckDuckGoSearchRun

load_dotenv()

# Ensure API Key exists
if not os.environ.get("GROQ_API_KEY"):
    raise ValueError("GROQ_API_KEY is not set in the environment variables.")

app = FastAPI(title="AI Research & Report Agent API")

# Enable CORS for Frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 1. Define Agent State
class AgentState(TypedDict):
    topic: str
    research_notes: str
    report: str

# 2. Initialize Tools and Groq LLM (Using Llama 3.3 70B for strong reasoning)
search_tool = DuckDuckGoSearchRun()
llm = ChatGroq(model="openai/gpt-oss-120b", temperature=0.3)

# 3. Define Graph Nodes (Steps)
def researcher_node(state: AgentState) -> Dict:
    """Executes web queries to extract hard factual data about the topic."""
    topic = state["topic"]
    
    # Perform a broad search query
    search_query = f"{topic} latest updates trends facts"
    try:
        search_results = search_tool.invoke(search_query)
    except Exception as e:
        search_results = f"Search failed due to: {str(e)}"
        
    # Synthesize research data
    research_prompt = (
        f"You are an expert Research Agent. Analyze the following search results for the topic '{topic}' "
        f"and compile extensive, comprehensive research notes containing key facts, numbers, and findings.\n\n"
        f"Search Results:\n{search_results}"
    )
    
    response = llm.invoke(research_prompt)
    return {"research_notes": str(response.content)}

def reporter_node(state: AgentState) -> Dict:
    """Drafts a beautifully formatted structure using markdown text."""
    topic = state["topic"]
    notes = state["research_notes"]
    
    report_prompt = (
        f"You are an elite Technical Reporter. Use these research notes to compile a comprehensive, professional "
        f"executive report regarding '{topic}'. Use Markdown formatting with clean headings, bullet points, "
        f"and a summary conclusion section.\n\n"
        f"Research Notes:\n{notes}"
    )
    
    response = llm.invoke(report_prompt)
    return {"report": str(response.content)}

# 4. Compile the LangGraph
workflow = StateGraph(AgentState)

workflow.add_node("researcher", researcher_node)
workflow.add_node("reporter", reporter_node)

workflow.set_entry_point("researcher")
workflow.add_edge("researcher", "reporter")
workflow.add_edge("reporter", END)

agent_executor = workflow.compile()

# 5. Pydantic Schema for Requests
class ResearchRequest(BaseModel):
    topic: str

@app.post("/api/research")
async def generate_report(request: ResearchRequest):
    try:
        inputs = {"topic": request.topic, "research_notes": "", "report": ""}
        result = await agent_executor.ainvoke(inputs)
        return {
            "success": True,
            "research_notes": result.get("research_notes"),
            "report": result.get("report")
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
