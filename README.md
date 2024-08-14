[![Software License](https://img.shields.io/badge/license-MIT-brightgreen.svg?style=flat-square)](LICENSE)
[![Python >=3.8](https://img.shields.io/badge/python-%3E%3D3.8-orange.svg?style=flat-square)](https://github.com/dismine/checkbox-sdk)
![GitHub last commit](https://img.shields.io/github/last-commit/dismine/checkbox-sdk)

# checkbox-sdk

### Python SDK для роботи з [Checkbox](https://checkbox.ua) (Україна)

#### Примітка:

> **Проєкт розроблявся для власних потреб.** Було додано підтримку всіх методів API сервісу Checkbox.
> Проте автор не має на меті використовувати їх усі, тому можливе існування методів, які потребують доопрацювання. Якщо
> ви знайдете помилки або маєте пропозиції щодо покращення коду, будемо вдячні за ваші зауваження.

> **Пакет розроблений на основі checkbox-api.** Основою для цього пакету став
> проєкт [checkbox-api](https://pypi.org/project/checkbox-api/), [автор](mailto:oleksandr.onufriichuk@itvaan.com.ua)
> якого, на жаль,
> не виходить на зв'язок і не зробив репозиторій публічним. Код був доопрацьований, оптимізований і покритий тестами для
> забезпечення його стабільності та функціональності.

#### Офіційна документація:

[Wiki](https://wiki.checkbox.ua/uk/api)

[Перелік методів - Swagger](https://api.checkbox.in.ua/api/redoc)

[Перелік методів - ReDoc](https://api.checkbox.in.ua/api/docs)

[Схема роботи з API](https://viewer.diagrams.net/?tags=%7B%7D&highlight=0000ff&edit=_blank&layers=1&nav=1&title=api_scheme_hard.drawio#Uhttps%3A%2F%2Fdrive.google.com%2Fuc%3Fid%3D1A_blv999c_-y2yUgPYMddYgfmpCNLE9T%26export%3Ddownload#%7B%22pageId%22%3A%227vV8fLOgreDzO-oaf-Jf%22%7D)

#### Опис

`checkbox-sdk` — це Python SDK для інтеграції з сервісом [checkbox.ua](https://checkbox.ua), який забезпечує
роботу з фіскальними реєстраторами та створенням електронних чеків. Пакет надає простий та інтуїтивно зрозумілий
інтерфейс для взаємодії з API Checkbox, дозволяючи виконувати такі операції, як створення чеків, генерація Z-звітів,
отримання інформації про товари та багато іншого.

Пакет використовує бібліотеку `httpx`, що забезпечує підтримку як синхронних, так і асинхронних викликів. Це дозволяє
легко інтегрувати SDK в різні типи додатків, від простих скриптів до складних асинхронних сервісів.

Цей SDK був створений для полегшення інтеграції з сервісом Checkbox у Python-додатках, мінімізуючи необхідність писати
власні HTTP-запити та обробку відповіді. Пакет підтримує всі основні функції API, однак можливе існування методів, які
потребують додаткової уваги та доопрацювання.

#### Онлайн-довідка

Більш детальну інформацію, приклади використання та документацію ви можете знайти
в [онлайн-довідці](https://checkbox-sdk.readthedocs.io).

#### Ліцензія

Checkbox-sdk випускається на умовах ліцензії MIT. Дивіться
файл [LICENSE](https://github.com/dismine/checkbox-sdk/blob/main/LICENSE) для більш детальної інформації.