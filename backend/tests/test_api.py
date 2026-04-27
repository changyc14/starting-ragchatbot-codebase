"""API endpoint tests for the RAG system."""
import pytest


class TestQueryEndpoint:
    """Tests for POST /api/query"""

    def test_query_returns_200(self, client, sample_query_payload):
        response = client.post("/api/query", json=sample_query_payload)
        assert response.status_code == 200

    def test_query_response_shape(self, client, sample_query_payload):
        response = client.post("/api/query", json=sample_query_payload)
        data = response.json()
        assert "answer" in data
        assert "sources" in data
        assert "session_id" in data

    def test_query_creates_session_when_none_provided(self, client, mock_rag_system, sample_query_payload):
        response = client.post("/api/query", json=sample_query_payload)
        assert response.status_code == 200
        # session_manager.create_session should have been called
        mock_rag_system.session_manager.create_session.assert_called_once()
        assert response.json()["session_id"] == "session_test"

    def test_query_uses_provided_session(self, client, mock_rag_system, sample_query_with_session):
        response = client.post("/api/query", json=sample_query_with_session)
        assert response.status_code == 200
        # Should NOT create a new session
        mock_rag_system.session_manager.create_session.assert_not_called()
        assert response.json()["session_id"] == "existing_session"

    def test_query_returns_answer_and_sources(self, client, sample_query_payload):
        response = client.post("/api/query", json=sample_query_payload)
        data = response.json()
        assert data["answer"] == "This is a test answer."
        assert data["sources"] == ["Source A", "Source B"]

    def test_query_missing_query_field_returns_422(self, client):
        response = client.post("/api/query", json={})
        assert response.status_code == 422

    def test_query_propagates_rag_exception_as_500(self, client, mock_rag_system):
        mock_rag_system.query.side_effect = RuntimeError("vector store unavailable")
        response = client.post("/api/query", json={"query": "anything"})
        assert response.status_code == 500
        assert "vector store unavailable" in response.json()["detail"]

    def test_query_calls_rag_system_with_correct_args(self, client, mock_rag_system):
        client.post("/api/query", json={"query": "test question", "session_id": "s1"})
        mock_rag_system.query.assert_called_once_with("test question", "s1")


class TestCoursesEndpoint:
    """Tests for GET /api/courses"""

    def test_courses_returns_200(self, client):
        response = client.get("/api/courses")
        assert response.status_code == 200

    def test_courses_response_shape(self, client):
        data = client.get("/api/courses").json()
        assert "total_courses" in data
        assert "course_titles" in data

    def test_courses_returns_expected_values(self, client):
        data = client.get("/api/courses").json()
        assert data["total_courses"] == 2
        assert data["course_titles"] == ["Course One", "Course Two"]

    def test_courses_propagates_exception_as_500(self, client, mock_rag_system):
        mock_rag_system.get_course_analytics.side_effect = RuntimeError("db error")
        response = client.get("/api/courses")
        assert response.status_code == 500
        assert "db error" in response.json()["detail"]


class TestRootEndpoint:
    """Tests for GET /"""

    def test_root_returns_200(self, client):
        response = client.get("/")
        assert response.status_code == 200

    def test_root_returns_status_ok(self, client):
        assert client.get("/").json() == {"status": "ok"}