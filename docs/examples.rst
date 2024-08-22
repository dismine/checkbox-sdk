Приклади
=========

Перевірка режиму роботи каси
*******************************

Після успішної аутентифікації важливо перевірити режим роботи каси, щоб визначити, чи вона працює в офлайн- або онлайн-режимі. Це дозволить правильно налаштувати подальші запити та обробку даних.

**Синхронний приклад**

.. code-block:: python

    from checkbox_sdk.client.synchronous import CheckBoxClient
    import time

    # Зберігаємо токен в змінній або базі даних
    token = "ВАШ_ТОКЕН"

    # Створюємо клієнта з токеном
    with CheckBoxClient() as client:
        client = client.cashier.authenticate(token=token, license_key="ВАШ_КЛЮЧ_ЛІЦЕНЗІЇ")

        # Перевіряємо режим роботи каси
        register = client.cash_registers.get_cash_register()
        if not register["offline_mode"]:
            print("Каса працює в онлайн-режимі.")
            client.cash_registers.get_offline_codes()
        else:
            print("Каса працює в офлайн-режимі.")
            max_retries = 5
            delay_between_retries = 60

            retries = 0

            while retries < max_retries:
                ping = client.cash_registers.ping_tax_service()
                if ping["error"] is None:
                    response = client.cash_registers.go_online()
                    if response["status"] == "ok":
                        time.sleep(delay_between_retries) # Каса виходить у онлайн не відразу
                        register = client.cash_registers.get_cash_register()
                        if not register["offline_mode"]:
                            client.cash_registers.get_offline_codes()
                            break
                    else:
                        print(f"Спроба {retries + 1} не привела до переведення касового апарату в режим он-лайн.")

                    retries += 1

            if retries == max_retries:
                print(f"Не вдалося перевести касу в режим онлайн після {max_retries} спроб.")

        # Подальші дії з касою: відкриття зміни, створення чеків і т.д.

        # Завершення роботи
        client.cashier.sign_out(storage)

**Асинхронний приклад**

.. code-block:: python

    from checkbox_sdk.client.asynchronous import AsyncCheckBoxClient
    import asyncio


    async def main():
        # Зберігаємо токен в змінній або базі даних
        token = "ВАШ_ТОКЕН"

        # Створюємо клієнта з токеном
        async with AsyncCheckBoxClient(token=token, license_key="ВАШ_КЛЮЧ_ЛІЦЕНЗІЇ") as client:
            # Перевіряємо режим роботи каси
            register = await client.cash_registers.get_cash_register()
            if not register["offline_mode"]:
                print("Каса працює в онлайн-режимі.")
                await client.cash_registers.get_offline_codes()
            else:
                print("Каса працює в офлайн-режимі.")
                while True:
                    ping = await client.cash_registers.ping_tax_service()
                    if ping["error"] is None:
                        response = await client.cash_registers.go_online()
                        if response["status"] == "ok":
                            await asyncio.sleep(60)  # Каса виходить у онлайн не відразу
                            break
                    await asyncio.sleep(5)

            # Подальші дії з касою: відкриття зміни, створення чеків і т.д.

            # Завершення роботи
            await client.cashier.sign_out()

    # Запускаємо асинхронну функцію
    asyncio.run(main())


В обох прикладах ми перевіряємо режим роботи каси після аутентифікації, використовуючи відповідний метод API. Якщо каса знаходиться в онлайн-режимі, запитуємо список офлайн кодів. Якщо каса в офлайн-режимі, перевіряємо зв'язок з ДПС і, у разі успіху, починаємо вихід в онлайн. Не забудьте замінити ``ВАШ_ТОКЕН`` на реальний токен, отриманий під час аутентифікації.

Робота з касовою зміною
*************************

Касова зміна не відкривається автоматично із першим чеком. Її потрібно відкрити окремою командою. Для цього скористайтесь відповідним методом API.

**Синхронний приклад**

.. code-block:: python

    from checkbox_sdk.client.synchronous import CheckBoxClient
    from checkbox_sdk.exceptions import StatusException

    # Зберігаємо токен в змінній або базі даних
    token = "ВАШ_ТОКЕН"

    with CheckBoxClient() as client:
        client.cashier.authenticate_token(token, license_key="ВАШ_КЛЮЧ_ЛІЦЕНЗІЇ")

        try:
            shift = client.shifts.create_shift(timeout=5)
            if shift["status"] == "OPENED":
                print("Касова зміна відкрита успішно")
        except StatusException as e:
            print(f"Сталася помилка при відкритті касової зміни: {e}")

        # Видаємо чеки

        try:
            client.shifts.close_shift(timeout=5)
        except StatusException as e:
            print(f"Сталася помилка при закритті касової зміни: {e}")

        client.cashier.sign_out()

**Асинхронний приклад**

.. code-block:: python

    from checkbox_sdk.client.asynchronous import AsyncCheckBoxClient
    from checkbox_sdk.exceptions import StatusException
    import asyncio

    async def main():
        # Зберігаємо токен в змінній або базі даних
        token = "ВАШ_ТОКЕН"

        async with AsyncCheckBoxClient(token=token, license_key="ВАШ_КЛЮЧ_ЛІЦЕНЗІЇ") as client:
            try:
                shift = await client.shifts.create_shift(timeout=5)
                if shift["status"] == "OPENED":
                    print("Касова зміна відкрита успішно")
            except StatusException as e:
                print(f"Сталася помилка при відкритті касової зміни: {e}")

            # Видаємо чеки

            try:
                await client.shifts.close_shift(timeout=5)
            except StatusException as e:
                print(f"Сталася помилка при закритті касової зміни: {e}")

            await client.cashier.sign_out()

    # Запускаємо асинхронну функцію
    asyncio.run(main())

Продаж
*******

Ось оновлена секція "Продаж" з урахуванням мінімального набору даних та обмеження по частоті запитів:

---

# Продаж

## Проведення продажу

Для проведення продажу за допомогою API Checkbox необхідно надати мінімальний набір даних. Цей набір включає:

- **Код товару**: Ідентифікатор товару.
- **Назва товару**: Опис товару або послуги.
- **Ціна**: Ціна одиниці товару.
- **Кількість**: Кількість одиниць товару.
- **Тип оплати**: Спосіб оплати (готівка, картка і т.д.).
- **Сума оплати**: Загальна сума оплати.

**Синхронний приклад**

.. code-block:: python

    from checkbox_sdk.client.synchronous import CheckBoxClient
    from checkbox_sdk.exceptions import StatusException

    # Зберігаємо токен в змінній або конфігураційному файлі
    token = "ВАШ_ТОКЕН"

    with CheckBoxClient() as client:
        client.cashier.authenticate_token(token, license_key="ВАШ_КЛЮЧ_ЛІЦЕНЗІЇ")

        # Відкриття касової зміни

        receipt_data =
        {
          "goods": [
            {
              "good": {
                "code": "T100",
                "name": "Тестовий товар 1",
                "price": 5500
              },
              "quantity": 1000
            },
            {
              "good": {
                "code": "T200",
                "name": "Тестовий товар 2",
                "price": 15200
              },
              "quantity": 1000
            }
          ],
          "discounts": [
            {
              "type": "DISCOUNT",
              "mode": "VALUE",
              "value": 2500,
              "name": "Знижка"
            }
          ],
          "payments": [
            {
              "type": "CASHLESS",
              "value": 18200
            }
          ]
        }

        try:
            client.receipts.create_receipt(
                receipt=receipt_data,
                timeout=5,
            )
        except StatusException as e:
                print(f"Сталася помилка при створенні чеку: {e}")

        # Закриття зміни

        client.cashier.sign_out()

**Асинхронний приклад**

.. code-block:: python

    from checkbox_sdk.client.asynchronous import AsyncCheckBoxClient
    from checkbox_sdk.exceptions import StatusException
    import asyncio

    async def main():
        # Зберігаємо токен в змінній або конфігураційному файлі
        token = "ВАШ_ТОКЕН"

        async with AsyncCheckBoxClient(token=token, license_key="ВАШ_КЛЮЧ_ЛІЦЕНЗІЇ") as client:
            # Відкриття касової зміни

            receipt_data = {
                "goods": [
                    {
                        "good": {
                            "code": "T100",
                            "name": "Тестовий товар 1",
                            "price": 5500
                        },
                        "quantity": 1000
                    },
                    {
                        "good": {
                            "code": "T200",
                            "name": "Тестовий товар 2",
                            "price": 15200
                        },
                        "quantity": 1000
                    }
                ],
                "discounts": [
                    {
                        "type": "DISCOUNT",
                        "mode": "VALUE",
                        "value": 2500,
                        "name": "Знижка"
                    }
                ],
                "payments": [
                    {
                        "type": "CASHLESS",
                        "value": 18200
                    }
                ]
            }

            try:
                await client.receipts.create_receipt(
                    receipt=receipt_data,
                    timeout=5,
                )
            except StatusException as e:
                print(f"Сталася помилка при створенні чеку: {e}")

            # Закриття зміни

            await client.cashier.sign_out()

    # Запускаємо асинхронну функцію
    asyncio.run(main())

