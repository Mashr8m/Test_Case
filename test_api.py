import requests
import pytest
import random
import os

API_BASE_URL = os.environ.get("BASE_URL")

def generate_seller_id(): #случайнфй ID
    return random.randint(100000, 900000)

# объявление
def create_valid_payload(seller_id):
    return {
        "sellerId": seller_id,
        "name": f"AAA {random.randint(1, 9999)}",
        "price": random.randint(100, 5000),
        "likes": random.randint(0, 10),
        "viewCount": random.randint(0, 50),
        "contacts": random.randint(0, 5)
    }

# фикстуры
@pytest.fixture(scope="session")
def session_seller_id():
    return generate_seller_id()


@pytest.fixture(scope="session")
def created_item_id(session_seller_id):
    payload = create_valid_payload(session_seller_id)
    response = requests.post(f"{API_BASE_URL}/item", json=payload)

    if response.status_code != 200:
        pytest.fail(f"Ошибка создания: {response.status_code}, {response.text}")

    response_text = response.json().get("status", "")
    if "Сохранили объявление " in response_text:
        item_id = response_text.split("Сохранили объявление ")[1]
    else:
        pytest.fail(f"Не нашли ID в ответе: {response_text}")

    return item_id

# создание объявления (падает из-за бага в API)
@pytest.mark.xfail(reason="API говорит 'поле likes обязательно', хотя оно есть")
def test_1(session_seller_id):
    test_payload = create_valid_payload(session_seller_id)
    response = requests.post(f"{API_BASE_URL}/item", json=test_payload)
    assert response.status_code == 200
    data = response.json()
    assert "status" in data
    assert "Сохранили объявление " in data["status"]

# ошибки при отсутствии полей
def test_2(session_seller_id):
    bad_payload = {
        "sellerId": session_seller_id,
        "name": "Item without stats",
        "price": 100,
    }
    response = requests.post(f"{API_BASE_URL}/item", json=bad_payload)
    assert response.status_code == 400
    assert "result" in response.json()

# несуществующее объявление
def test_3():
    fake_id = "11111111-2222-3333-4444-555555555555"
    response = requests.get(f"{API_BASE_URL}/item/{fake_id}")
    assert response.status_code == 404

# все объявления продавца (падает из-за бага в API)
@pytest.mark.xfail(reason="Не может создать объявление для теста")
def test_4(session_seller_id, created_item_id):
    response = requests.get(f"{API_BASE_URL}/{session_seller_id}/item")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)

# объявлений несуществующего продавца
def test_5():
    fake_seller = random.randint(800000, 900000)
    response = requests.get(f"{API_BASE_URL}/{fake_seller}/item")
    assert response.status_code == 200
    assert response.json() == []

#статистика (падает из-за бага в API)
@pytest.mark.xfail(reason="Не может создать объявление для теста")
def test_6(created_item_id):
    response = requests.get(f"{API_BASE_URL}/statistic/{created_item_id}")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1

    stats = data[0]
    assert "likes" in stats and isinstance(stats.get("likes"), int)
    assert "viewCount" in stats and isinstance(stats.get("viewCount"), int)
    assert "contacts" in stats and isinstance(stats.get("contacts"), int)