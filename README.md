# Webframework

Библиотека для написания асинхронных веб-приложений на Python.
Вдохновлена современными веб-фреймворками (FastAPI).

## Особенности

- **Совместимость с ASGI**. Приложение можно запускать с использованием любого ASGI сервера (например, uvicorn).

- **Внедрение зависимостей**. Улучшает читаемость кода, длаете его более функциональным.

## Установка

Для установки используйте следующую команду:

```bash
pip install git+https://github.com/ArtemKondratenko/WebFramework.git
```

Проект не использует никаких сторонних зависимостей (кроме development зависимостей).

## Примеры

В проекте также включен [пример приложения (example.py)](example.py), которое демонстрирует:

- создание / удаление / изменение пользователей
- внедрение зависимостей
- простейшая аутентификация (Basic HTTP Authorization)
- работа с объектам Request и Response

## Архитектура

### ASGI интерфейс (`application.py`)

Предоставляет класс `App`, реализующий интерфейс ASGI приложения, позволяющий запускать веб-приложение через любой ASGI сервер.

### Роутер (`router.py`)

Используется для регистрации обработчиков запроса, по методу и пути, а также получения обработчика запроса. Для распространенных методов HTTP (GET, POST, PUT, DELETE) предоставляет декораторы, которые можно напрямую использовать при определении обработчика.

Например:

```python
@router.get("/users/{user_id}")
def get_users(...) -> Response:
    ...

@router.post("/users")
def create_user(...) -> Response:
    ...
```

### Внедрение зависимостей (`injector.py`)

Получает на вход функцию, если параметр является аннотированным, то вызвает эту функцию, получает результат и записывает в параметр.

```python
# Значение для `x` будет вычислено с помощью функции `provide_x`
def function(x: Annotated[int, provide_x]) -> None:
    ...
```

Также вызов может быть вложенным:

```python
# При этом сам `provide_x` также может нуждаться в зависимостях
# (Injector автоматически их определит по такому же алгоритму)
def provide_x(y: Annotated[str, provide_y]) -> int:
    ...
```

Библиотека предоставляет набор полезных функций-провайдеров для извлечения информации из самого запроса:

```python
# 1. Извлечение информации из пути:
@router.get("/users/{username}")
def get_user(username: Annotated[str, path("username")]) -> Response:
    ...

# 2. Парсинг данных
# В примере мы не просто берем строчку из пути, но также
# преобразуем ее в целое число:
@router.get("/users/{user_id}")
def get_user(user_id: Annotated[int, parsed(path("username"), int)]) -> Response:
    ...

# 3. Извлечение информации из тела запроса:

# 3.1. Берем тело запроса целиком и преобразуем его в объект User:
@router.post("/users")
def create_user(User: Annotated[User, parsed(body(), User.from_dict)]) -> Response:
    ...

# 3.2. Можно извлечь и одно единственное поле из тела запроса.
# В этом примере мы извлекаем из тела запроса только поле по ключу "username":
@router.post("/users")
def create_user(username: Annotated[str, body("username")]) -> Response:
    ...

# 4. Извлечение информации из заголовка:
# В этом примере мы извлекаем информацию для аутентификации пользователя из заголовка Authorization:
@router.get("/protected")
def get_protected_resource(
    auth: Annotated[
        BasicHTTPAuthCredentials,
        parsed(header("Authorization"), BasicHTTPAuthCredentials.parse),
    ],
) -> Response:
```
