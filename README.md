p+s+p+a+d+k/
├── tests/
│   ├── ui/               # UI-тесты
│   │   ├── test_login.py
│   │   └── test_dynamic_properties.py
│   ├── api/              # API-тесты
│   │   ├── test_api_auth.py
│   │   └── test_api_products.py
│   └── conftest.py       # Фикстуры pytest
├── pages/                # Page Object Model (POM)
│   ├── base_page.py      # Базовый класс
│   ├── login_page.py     # Страница авторизации
│   └── dynamic_page.py   # Страница с динамическими элементами
├── utils/                # Утилиты (логи, параметры)
│   ├── logger.py         # Настройка логирования
│   └── config.py         # Чтение .env
├── requirements.txt      # Зависимости
├── .env                  # Секреты (логины/пароли)
├── pytest.ini            # Настройки pytest
├── Dockerfile            # Контейнеризация тестов
├── docker-compose.yml    # Docker для Selenium Grid
└── k8s/                 # Манифесты Kubernetes
    ├── deployment.yaml   # Развертывание тестов
    └── service.yaml      # Сервис для доступа