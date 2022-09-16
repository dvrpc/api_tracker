"""API Tracker API. Check api_tracker database for specific urls.

crawler/crawler.py in this repo populates the database.
"""
from typing import List
import sys

from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import psycopg2
from pydantic import BaseModel, Field

sys.path.append("..")

from config import PG_CREDS


class Message(BaseModel):
    message: str


class Result(BaseModel):
    path: str
    line_number: int = Field(None, alias="line number")
    line: str


app = FastAPI(
    title="API Tracker API",
    openapi_url="/api_tracker/v1/openapi.json",
    docs_url="/api_tracker/v1/docs",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET"],
    allow_headers=["*"],
)


def get_conn():
    """Connect to database, yield it, close it."""
    conn = psycopg2.connect(PSQL_CREDS)
    try:
        yield conn
    finally:
        conn.close()


@app.get(
    "/api_tracker/v1/paths",
    responses={500: {"model": Message, "description": "Internal Server Error"}},
    response_model=List[Result],
)
def get_paths(string: str, conn=Depends(get_conn)):
    """Return list of dictionaries of all records containing submitted string."""

    cur = conn.cursor()
    try:
        cur.execute(
            "SELECT DISTINCT file_path, line_number, string_hit FROM matches WHERE string_hit LIKE %s",
            ["%{}%".format(string)],
        )
    except psycopg2.Error as e:
        return JSONResponse(status_code=500, content={"message": "Database error: " + str(e)})

    results = cur.fetchall()

    if not results:
        return []

    paths = []
    for row in results:
        paths.append(
            {
                "path": row[0],
                "line number": row[1],
                "line": row[2],
            }
        )

    return paths
