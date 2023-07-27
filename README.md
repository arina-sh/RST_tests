## Итоговый проект по автоматизации тестирования на Python

Исполнитель: Шабалина Арина, QAP-1028

Объект тестирования: новый интерфейс авторизации в личном кабинете от заказчика Ростелеком Информационные Технологии https://b2c.passport.rt.ru

В рамках задания:
1. Были протестированы требования, [результат тестирования (файл с комментариями)](https://github.com/arina-sh/RST_tests/tree/master/requirements) расположен в папке requirements
2. Сформирован [набор тест-кейсов](https://docs.google.com/spreadsheets/d/1oM1kWKwHLAVKJbyuSus9zOkwEqD3Ml9twRvwUUMruWM/edit?usp=sharing)
3. Разработаны [автотесты](https://github.com/arina-sh/RST_tests/tree/master/tests)
4. Сформированы [баг-репорты](https://trello.com/invite/b/kCanOTx4/ATTIdacb1c391e0bb4a09e56f1e879a4949059260CBE/баги-формы-авторизации-в-лк-ростелеком)

При разработке тест-кейсов использованы следующие техники тест-дизайна:
- эквивалентное разделение;
- таблица решений (для проверки различных опций авторизации);
- диаграмма состояний и переходов (для анализа и проверки форм, на которые можно перейти с формы авторизации);
- граничные значения не определены в требованиях, поэтому отдельных тест-кейсов на максимальное количество символов в полях ввода нет, так как необходимо сначала уточнить вопрос ограничений на ввод в требованиях;
- предугадавание ошибки.

Были использованы следующие инструменты:
- для документирования тест-кейсов, формирования таблицы решений - Google таблицы;
- для диаграммы состояний и переходов - xmind.works;
- для поиска, просмотра элементов страницы, запросов - DevTools;
- Trello - для документирования баг-репортов;
- среда разработки PyCharm - для автотестов.

Для того, чтобы запустить автотесты необходимо:
  * клонировать проект из GitHub
  * создать файл .env, в котором необходимо указать
    - валидные значения электронной почты/номера телефона/логина/лицевого счёта и пароля зарегистрированного пользователя,
    - невалидные значения электронной почты/номера телефона/логина/лицевого счёта и пароля (подробнее описано в [тест-кейсах](https://docs.google.com/spreadsheets/d/1oM1kWKwHLAVKJbyuSus9zOkwEqD3Ml9twRvwUUMruWM/edit?usp=sharing)).
  * создать виртуальное окружение (для этого необходимо перейти в директорию своего проекта и выполнить: python -m venv venv)
  * установить библиотеки
    - Python 3.11,
    - pytest 7.4.0,
    - selenium 4.10.0,
    - python-dotenv 1.0.0.
