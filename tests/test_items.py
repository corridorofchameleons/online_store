import pytest
from httpx import AsyncClient, ASGITransport

from main import app


@pytest.fixture
def test_data():
    return {
            "name": "test_name",
            "email": "email@yandxz.com",
            "phone": "+79001002040",
    }


@pytest.fixture
def test_item():
    return {
        "name": "item",
        "price": 100,
        "is_active": True
    }


@pytest.mark.asyncio
async def test_register(test_data, ac: AsyncClient):
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        response = await ac.post("/users/create", json=test_data | {
            "password": "c0Rrect&password",
            "password_2": "c0Rrect&password",
            "is_admin": True
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
async def test_create(test_item):
    with open('tests/token.txt') as f:
        token = f.readline().strip()
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        response = await ac.post("/store/items/create", headers={'Authorization': f'Bearer {token}'}, json=test_item)
    assert response.status_code == 200
    assert len(response.json()) == 4
    id_ = response.json().get('id')
    with open('tests/id.txt', 'w') as f:
        f.write(str(id_))


@pytest.mark.asyncio
async def test_add_to_cart():
    with open('tests/token.txt') as f:
        token = f.readline().strip()
    with open('tests/id.txt') as f:
        id_ = f.readline().strip()
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        response = await ac.post("/store/cart/add", headers={'Authorization': f'Bearer {token}'},
                                 json={
                                     "item_id": int(id_),
                                     "qty": 5
                                 })

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


@pytest.mark.asyncio
async def test_cart():
    with open('tests/token.txt') as f:
        token = f.readline().strip()
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        response = await ac.get("/store/cart", headers={'Authorization': f'Bearer {token}'})

    assert response.status_code == 200
    assert response.json().get('total') == 500
    assert len(response.json().get('items')) == 1
