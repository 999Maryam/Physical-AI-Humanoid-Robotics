#!/usr/bin/env python3
"""
FastAPI server for RAG backend integration.

This module creates a FastAPI application that exposes a /ask endpoint
for RAG queries, reusing the existing create_rag_response() function
from agent.py.
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import logging
from dotenv import load_dotenv
import os

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

from agent import create_rag_response

# Initialize FastAPI app
app = FastAPI(
    title="RAG API",
    description="API for RAG queries using existing create_rag_response function",
    version="1.0.0"
)

# Add CORS middleware for local development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Define request and response models
class QueryRequest(BaseModel):
    query: str
    response_length: Optional[int] = None  # Not directly used but available for future use
    search_depth: Optional[int] = None     # Not directly used but available for future use
    result_format: Optional[str] = None    # Not directly used but available for future use

class QueryResponse(BaseModel):
    response: str
    status: Optional[str] = "success"
    error_message: Optional[str] = None

# Error handling wrapper around create_rag_response
def safe_create_rag_response(query: str) -> QueryResponse:
    try:
        response = create_rag_response(query)
        return QueryResponse(response=response)
    except Exception as e:
        logging.error(f"Error in create_rag_response: {str(e)}")
        return QueryResponse(
            response="An error occurred while processing your request",
            status="error",
            error_message=str(e)
        )

@app.get("/")
def health_check():
    """Health check endpoint"""
    return {"message": "RAG API is running"}

@app.post("/ask", response_model=QueryResponse)
def ask_rag(request: QueryRequest):
    """Submit a query to the RAG system"""
    logger.info(f"Received query request with parameters: response_length={request.response_length}, search_depth={request.search_depth}, result_format={request.result_format}")

    if not request.query or len(request.query.strip()) == 0:
        raise HTTPException(status_code=400, detail="Query is required and must not be empty")

    # Limit query length to prevent overly long requests
    if len(request.query) > 1000:
        raise HTTPException(status_code=400, detail="Query is too long. Maximum length is 1000 characters.")

    # Validate query parameters
    if request.response_length is not None and request.response_length <= 0:
        raise HTTPException(status_code=400, detail="Response length must be positive")

    if request.search_depth is not None and request.search_depth <= 0:
        raise HTTPException(status_code=400, detail="Search depth must be positive")

    if request.result_format is not None and request.result_format not in ["text", "json", "detailed"]:
        raise HTTPException(status_code=400, detail="Result format must be one of: text, json, detailed")

    result = safe_create_rag_response(request.query)
    logger.info(f"Query processed successfully, response length: {len(result.response) if result.response else 0} characters")
    return result