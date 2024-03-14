import pytest
from httpx import AsyncClient
from server import app


@pytest.mark.asyncio
async def test_create_task_sum() -> None:
    async with AsyncClient(app=app, base_url="http://localhost:8000") as ac:
        response = await ac.post("/task/", json={"task_name": "Sum", "parameters": {"a": 5, "b": 7}})
    assert response.status_code == 200
    assert "task_id" in response.json()
    sum_task_id = response.json()["task_id"]

    response = await ac.get(f"/task/{sum_task_id}")
    assert response.status_code == 200
    assert response.json()["result"] == 12


@pytest.mark.asyncio
async def test_create_task_concat() -> None:
    async with AsyncClient(app=app, base_url="http://localhost:8000") as ac:
        response = await ac.post("/task/", json={"task_name": "Concat",
                                                 "parameters": {"str1": "Hello", "str2": " ", "str3": "World"}})
    assert response.status_code == 200
    assert "task_id" in response.json()
    concat_task_id = response.json()["task_id"]

    response = await ac.get(f"/task/{concat_task_id}")
    assert response.status_code == 200
    assert response.json()["result"] == "Hello World"


@pytest.mark.asyncio
async def test_get_task_result_not_found() -> None:
    async with AsyncClient(app=app, base_url="http://localhost:8000") as ac:
        response = await ac.get("/task/non_existing_task_id")
    assert response.status_code == 404
