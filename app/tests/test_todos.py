import pytest
import httpx

@pytest.mark.asyncio
async def test_create_todo():
    async with httpx.AsyncClient(base_url="http://localhost:8000") as client:
        response = await client.post("/todos/", json={"title": "Test ToDo", "description": "Test Description", "completed": False})
        assert response.status_code == 200
        data = response.json()
        assert data["title"] == "Test ToDo"
        assert data["description"] == "Test Description"
        assert data["completed"] is False

@pytest.mark.asyncio
async def test_read_todos():
    async with httpx.AsyncClient(base_url="http://localhost:8000") as client:
        response = await client.get("/todos/")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) >= 0

@pytest.mark.asyncio
async def test_read_todo():
    async with httpx.AsyncClient(base_url="http://localhost:8000") as client:
        # First, create a new todo to read it later
        create_response = await client.post("/todos/", json={"title": "Another ToDo", "description": "Another Description", "completed": False})
        assert create_response.status_code == 200
        todo_id = create_response.json()["id"]

        # Now, read the created todo
        response = await client.get(f"/todos/{todo_id}")
        assert response.status_code == 200
        data = response.json()
        assert data["title"] == "Another ToDo"
        assert data["description"] == "Another Description"

@pytest.mark.asyncio
async def test_update_todo():
    async with httpx.AsyncClient(base_url="http://localhost:8000") as client:
        # First, create a new todo to update it later
        create_response = await client.post("/todos/", json={"title": "Update ToDo", "description": "Update Description", "completed": False})
        assert create_response.status_code == 200
        todo_id = create_response.json()["id"]

        # Now, update the created todo
        response = await client.put(f"/todos/{todo_id}", json={"title": "Updated ToDo", "description": "Updated Description", "completed": True})
        assert response.status_code == 200
        data = response.json()
        assert data["title"] == "Updated ToDo"
        assert data["description"] == "Updated Description"
        assert data["completed"] is True

@pytest.mark.asyncio
async def test_delete_todo():
    async with httpx.AsyncClient(base_url="http://localhost:8000") as client:
        # First, create a new todo to delete it later
        create_response = await client.post("/todos/", json={"title": "Delete ToDo", "description": "Delete Description", "completed": False})
        assert create_response.status_code == 200
        todo_id = create_response.json()["id"]

        # Now, delete the created todo
        response = await client.delete(f"/todos/{todo_id}")
        assert response.status_code == 200

        # Verify the todo is deleted
        get_response = await client.get(f"/todos/{todo_id}")
        assert get_response.status_code == 404
