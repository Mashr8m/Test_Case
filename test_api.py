import requests
import pytest
import random
import os

API_BASE_URL = os.environ.get("BASE_URL")

def generate_seller_id():
    return random.randint(100000, 900000)

def create_valid_payload(seller_id):
    return {
        "sellerId": seller_id,
        "name": f"Test Item {random.randint(1, 9999)}",
        "price": random.randint(100, 5000),
        "statistics": {
            "likes": random.randint(0, 10),
            "viewCount": random.randint(0, 50),
            "contacts": random.randint(0, 5)
        }
    }

@pytest.fixture(scope="session") #фикстуры
def session_seller_id():
    return generate_seller_id()

@pytest.fixture(scope="session")
def created_item_id(session_seller_id):
    payload = create_valid_payload(session_seller_id)

    response = requests.post(f"{API_BASE_URL}/item", json=payload)

    if response.status_code != 200:
        pytest.fail(f" {response.status_code}, {response.text}")

    response_text = response.json().get("status", "")
    if "Сохранили объявление - " in response_text:
        item_id = response_text.split("Сохранили объявление - ")[1]
    else:
        pytest.fail(f"Не удалось извлечь ID из ответа: {response_text}")

    assert item_id is not None, "ID не пришел в ответе после создания!"
    return item_id


# ТЕСТЫ НА POST
def test_1_create_item_success(session_seller_id): #создание объявления

    test_payload = create_valid_payload(session_seller_id)

    response = requests.post(f"{API_BASE_URL}/item", json=test_payload)

    assert response.status_code == 200
    data = response.json()
    assert "status" in data
    assert "Сохранили объявление - " in data["status"]


def test_2_no_stats_error(session_seller_id): #без statistics

    bad_payload = {
        "sellerId": session_seller_id,  # Исправлено: sellerId вместо sellerID
        "name": "Item without stats",
        "price": 100,
    }

    response = requests.post(f"{API_BASE_URL}/item", json=bad_payload)

    assert response.status_code == 400
    assert "result" in response.json()


# ТЕСТЫ НА GET
def test_3_get_by_non_existent_id(): #несуществующее объявление

    non_existent_id = "11111111-2222-3333-4444-555555555555"

    response = requests.get(f"{API_BASE_URL}/item/{non_existent_id}")

    assert response.status_code == 404


def test_4_get_all_seller_items(session_seller_id, created_item_id): #все объявления

    response = requests.get(f"{API_BASE_URL}/{session_seller_id}/item")

    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)


def test_5_get_seller_with_no_items(): #несуществующий продавец

    no_items = random.randint(800000, 900000)

    response = requests.get(f"{API_BASE_URL}/{no_items}/item")

    assert response.status_code == 200
    assert response.json() == []


# СТАТИСТИКА
def test_6_get_statistics_success(created_item_id):

    response = requests.get(f"{API_BASE_URL}/statistic/{created_item_id}")

    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1

    stats_data = data[0]
    assert "likes" in stats_data and isinstance(stats_data.get("likes"), int)
    assert "viewCount" in stats_data and isinstance(stats_data.get("viewCount"), int)
    assert "contacts" in stats_data and isinstance(stats_data.get("contacts"), int)