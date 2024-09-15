import pytest
from httpx import AsyncClient, ASGITransport

from main import app

pytest_plugins = ('pytest_asyncio',)


@pytest.fixture
def test_data():
    return {
            "name": "test_name",
            "email": "email@gmaiola.com",
            "phone": "+79876543241",
    }


@pytest.fixture
def test_update_data():
    return {
            "name": "test_name",
            "email": "email@gmaiola.com",
            "phone": "+70000000103",
    }


@pytest.mark.asyncio
async def test_register(test_data, ac: AsyncClient):
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        response = await ac.post("/users/create", json=test_data | {
            "password": "c0Rrect&password",
            "password_2": "c0Rrect&password"
        })

    assert response.status_code == 200
    assert response.json() == test_data


@pytest.mark.asyncio
async def test_login(test_data):
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        response = await ac.post("/users/token", json=test_data | {"password": "c0Rrect&password"})
    assert response.status_code == 200
    token = response.json().get('access_token')
    with open('tests/token.txt', 'w') as f:
        f.write(token)


@pytest.mark.asyncio
async def test_update(test_update_data, ac: AsyncClient):
    with open('tests/token.txt') as f:
        token = f.readline().strip()
    async with AsyncClient(
            transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        response = await ac.put('users/update', headers={'Authorization': f'Bearer {token}'},  json=test_update_data)
    assert response.status_code == 200
    assert response.json().get('phone') == '+70000000103'


@pytest.mark.asyncio
async def test_me(test_data, ac: AsyncClient):
    with open('tests/token.txt') as f:
        token = f.readline().strip()
    async with AsyncClient(
            transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        response = await ac.get('users/me', headers={'Authorization': f'Bearer {token}'})
    assert response.status_code == 200
    assert response.json() == {
            "name": "test_name",
            "email": "email@gmaiola.com",
            "phone": "+70000000103",
    }


@pytest.mark.asyncio
async def test_delete(ac: AsyncClient):
    with open('tests/token.txt') as f:
        token = f.readline().strip()
    async with AsyncClient(
            transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        response = await ac.delete('users/delete', headers={'Authorization': f'Bearer {token}'})
    assert response.status_code == 200
