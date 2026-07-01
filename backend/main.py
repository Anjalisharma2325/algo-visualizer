from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Optional

from algorithms import SORT_ALGORITHMS, SEARCH_ALGORITHMS

app = FastAPI(
    title="Algo Visualizer API",
    description="Run sorting and searching algorithms and get back performance metrics.",
    version="1.0.0",
)

# Allow the frontend (any origin, for a portfolio project) to call this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


class SortRequest(BaseModel):
    array: List[float] = Field(..., min_items=0, max_items=500)
    algorithm: str = Field(..., description="One of: bubble, merge, quick")


class SearchRequest(BaseModel):
    array: List[float] = Field(..., min_items=0, max_items=500)
    target: float
    algorithm: str = Field(..., description="One of: linear, binary")


@app.get("/")
def root():
    return {
        "message": "Algo Visualizer API is running",
        "endpoints": ["/sort", "/search", "/algorithms"],
    }


@app.get("/algorithms")
def list_algorithms():
    return {
        "sort": list(SORT_ALGORITHMS.keys()),
        "search": list(SEARCH_ALGORITHMS.keys()),
    }


@app.post("/sort")
def sort_array(req: SortRequest):
    if req.algorithm not in SORT_ALGORITHMS:
        raise HTTPException(
            status_code=400,
            detail=f"Unknown algorithm '{req.algorithm}'. Choose from {list(SORT_ALGORITHMS.keys())}.",
        )
    fn = SORT_ALGORITHMS[req.algorithm]
    outcome = fn(req.array)
    return {
        "algorithm": req.algorithm,
        "input_size": len(req.array),
        **outcome,
    }


@app.post("/search")
def search_array(req: SearchRequest):
    if req.algorithm not in SEARCH_ALGORITHMS:
        raise HTTPException(
            status_code=400,
            detail=f"Unknown algorithm '{req.algorithm}'. Choose from {list(SEARCH_ALGORITHMS.keys())}.",
        )
    fn = SEARCH_ALGORITHMS[req.algorithm]
    outcome = fn(req.array, req.target)
    return {
        "algorithm": req.algorithm,
        "input_size": len(req.array),
        "target": req.target,
        **outcome,
    }
