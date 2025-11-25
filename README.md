Задание 1 Анализ багов UI

Анализ скриншота выполнен в файле TASK_1.md. Обнаружено 8 багов с приоритетами от Low до Medium.



Задание 2.1 Тестирование API 

Предварительные требования:
- Python 3.8+
- Установленные зависимости  pip install -r requirements.txt

Установка переменного окружения и запуск тестов:
1. $env:BASE_URL = 'https://qa-internship.avito.com/api/1'
2. pytest test_api.py -v

Описание тестов:
1. test_1_create_item_success - тест успешного создания объявления 
2. test_2_no_stats_error - тест ошибки при отсутствии statistics 
3. test_3_get_by_non_existent_id - тест получения несуществующего объявления 
4. test_4_get_all_seller_items - тест получения всех объявлений продавца 
5. test_5_get_seller_with_no_items - тест получения объявлений несуществующего продавца 
6. test_6_get_statistics_success - тест получения статистики
