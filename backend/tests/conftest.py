"""Shared fixtures for RAG system tests."""
import pytest
from unittest.mock import MagicMock, patch
from fastapi.testclient import TestClient


# ---------------------------------------------------------------------------
# Minimal test app (avoids importing app.py which mounts ../frontend)
# ---------------------------------------------------------------------------

def make_test_app(rag_system_mock):
    """Build a FastAPI app wired to a mock RAGSystem."""
    from fastapi import FastAPI, HTTPException
    from fastapi.middleware.cors import CORSMiddleware
    from pydantic import BaseModel
    from typing import List, Optional

    test_app = FastAPI()
    test_app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_methods=["*"],
        allow_headers=["*"],
    )

    class QueryRequest(BaseModel):
        query: str
        session_id: Optional[str] = None

    class QueryResponse(BaseModel):
        answer: str
        sources: List[str]
        session_id: str

    class CourseStats(BaseModel):
        total_courses: int
        course_titles: List[str]

    @test_app.post("/api/query", response_model=QueryResponse)
    async def query_documents(request: QueryRequest):
        try:
            session_id = request.session_id
            if not session_id:
                session_id = rag_system_mock.session_manager.create_session()
            answer, sources = rag_system_mock.query(request.query, session_id)
            return QueryResponse(answer=answer, sources=sources, session_id=session_id)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    @test_app.get("/api/courses", response_model=CourseStats)
    async def get_course_stats():
        try:
            analytics = rag_system_mock.get_course_analytics()
            return CourseStats(
                total_courses=analytics["total_courses"],
                course_titles=analytics["course_titles"],
            )
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    @test_app.get("/")
    async def root():
        return {"status": "ok"}

    return test_app


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture
def mock_rag_system():
    """A MagicMock that mimics RAGSystem."""
    rag = MagicMock()

    # session_manager.create_session returns a predictable ID
    rag.session_manager.create_session.return_value = "session_test"

    # Default query response
    rag.query.return_value = ("This is a test answer.", ["Source A", "Source B"])

    # Default analytics
    rag.get_course_analytics.return_value = {
        "total_courses": 2,
        "course_titles": ["Course One", "Course Two"],
    }

    return rag


@pytest.fixture
def client(mock_rag_system):
    """TestClient backed by the lightweight test app."""
    app = make_test_app(mock_rag_system)
    return TestClient(app)


@pytest.fixture
def sample_query_payload():
    return {"query": "What is retrieval-augmented generation?"}


@pytest.fixture
def sample_query_with_session():
    return {"query": "Tell me about lesson 2.", "session_id": "existing_session"}