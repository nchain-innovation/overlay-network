
from fastapi import FastAPI
from typing import Dict


tags_metadata = [
    {
        "name": "Example Application REST API",
        "description": "Example Application REST API",
    },
]


app = FastAPI(
    title="Example Application REST API",
    description="Example Application REST API",
    openapi_tags=tags_metadata,
)


@app.get("/", tags=["Web"])
def root() -> Dict[str, str]:
    """Web server Root"""
    return {
        "name": "Example Application REST API",
        "description": "Example Application REST API",
    }
