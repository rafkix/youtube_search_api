# app/main.py
from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel, Field
from typing import List, Optional, Any
from api.yt_search import YoutubeSearch

app = FastAPI(title="YT Search API", version="1.0")

class SearchRequest(BaseModel):
    q: str = Field(..., min_length=1, description="Search query")
    max_results: Optional[int] = Field(8, ge=1, le=50, description="Max results to return (1-50)")
    clear_cache: Optional[bool] = True

@app.post("/search", response_model=List[dict])
async def search_post(body: SearchRequest):
    if not body.q.strip():
        raise HTTPException(status_code=400, detail="q must not be empty")

    ys = YoutubeSearch(search_terms=body.q, max_results=body.max_results)
    await ys.fetch_results()
    return await ys.to_dict(clear_cache=body.clear_cache)

# also provide a GET shortcut for quick testing
@app.get("/search", response_model=List[dict])
async def search_get(q: str = Query(..., min_length=1), max_results: int = Query(8, ge=1, le=50), clear_cache: bool = True):
    ys = YoutubeSearch(search_terms=q, max_results=max_results)
    await ys.fetch_results()
    return await ys.to_dict(clear_cache=clear_cache)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
