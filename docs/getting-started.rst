Початок роботи
===============

Цей документ допоможе вам швидко розпочати роботу з пакетом `checkbox-sdk`. Нижче наведено інструкції з встановлення, базового використання та приклади коду.

Встановлення
------------

Для встановлення пакету `checkbox-sdk`, використовуйте pip:

.. prompt:: bash $

    pip install checkbox-sdk

Налаштування
------------

Після встановлення пакету вам потрібно налаштувати клієнт для взаємодії з API Checkbox. `checkbox-sdk` надає можливість використовувати як синхронний, так і асинхронний клієнти.

Для початку роботи, вам необхідно отримати токен доступу, який буде використовуватись для авторизації ваших запитів до API Checkbox.

Рекомендований спосіб отримання токену доступу — використання ключа ліцензії каси та пінкоду касира. Це забезпечує безпечну авторизацію та доступ до функціоналу касового апарату через API.

**Приклад отримання токену доступу:**

.. code-block:: python

    from checkbox_sdk.client.synchronous import CheckBoxClient

    client = CheckBoxClient()
    token_response = client.cashier.authenticate_pin_code(license_key="ВАШ_КЛЮЧ_ЛІЦЕНЗІЇ", pin_code="ВАШ_ПІНКОД_КАСИРА")
    token = client.storage.token
    print(f"Токен доступу: {token}")

**Асинхронний приклад:**

.. code-block:: python

    from checkbox_sdk.client.asynchronous import AsyncCheckBoxClient
    import asyncio

    async def get_token():
        client = AsyncCheckBoxClient()
        token_response = await client.cashier.authenticate_pin_code(license_key="ВАШ_КЛЮЧ_ЛІЦЕНЗІЇ", pin_code="ВАШ_ПІНКОД_КАСИРА")
        token = client.storage.token
        print(f"Токен доступу: {token}")

    asyncio.run(get_token())

У відповідь ви отримаєте JWT токен авторизації. Він автоматично додається до заголовків запитів інших методів, що дозволяє вам виконувати дії від імені касира, який пройшов авторизацію. Після кожної нової авторизації ви будете отримувати новий токен доступу, при цьому попередні токени залишатимуться активними. Для деактивації токену необхідно скористатися методом :meth:`checkbox_sdk.client.api.cashier.Cashier.sign_out`.

.. warning::
    Зверніть увагу, що один активний касир може мати не більше 10 діючих токенів. При отриманні нового токену старі токени автоматично видаляються. Якщо ви отримали помилку виду "Невірний токен доступу", це може означати, що ваш токен став недійсним або ви перевищили максимальну кількість активних токенів. У такому випадку вам слід отримати новий токен та використовувати його для подальших запитів.

Використання збереженого токену
-------------------------------

Щоб уникнути необхідності отримувати новий токен кожного разу, ви можете зберегти раніше отриманий токен і повторно використовувати його для аутентифікації. Це дозволяє зменшити кількість запитів до API та спростити процес інтеграції.

**Приклад збереження і повторного використання токену:**

.. code-block:: python

    from checkbox_sdk.client.synchronous import CheckBoxClient

    # Зберігаємо токен в змінній або базі данних
    saved_token = "ВАШ_ЗБЕРЕЖЕНИЙ_ТОКЕН"

    client = CheckBoxClient()
    client.cashier.authenticate_token(saved_token, license_key="ВАШ_КЛЮЧ_ЛІЦЕНЗІЇ")

    # Тепер можна використовувати клієнта з збереженим токеном
    response = client.some_method()
    print(response)

**Асинхронний приклад:**

.. code-block:: python

    from checkbox_sdk.client.asynchronous import AsyncCheckBoxClient
    import asyncio

    # Зберігаємо токен в змінній або базі данних
    saved_token = "ВАШ_ЗБЕРЕЖЕНИЙ_ТОКЕН"

    async def use_client():
        client = AsyncCheckBoxClient()
        client.cashier.authenticate_token(saved_token, license_key="ВАШ_КЛЮЧ_ЛІЦЕНЗІЇ")

        # Тепер можна використовувати клієнта з збереженим токеном
        response = await client.some_method()
        print(response)

    asyncio.run(use_client())


У разі отримання помилки аутентифікації, отримайте новий токен за допомогою раніше описаних методів та використовуйте його.