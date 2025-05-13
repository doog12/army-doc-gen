# 📄 Telegram Document Generator Bot (NGU)

Цей бот створений для допомоги військовослужбовцям Національної гвардії України у формуванні рапортів, заяв та інших документів через Telegram.

🔐 Доступ захищений паролем.  
📥 Користувач може вибрати тип документа, отримувача та підтип, після чого завантажити шаблон у форматі DOCX.

<p align="center">
  <a href="https://www.python.org">
    <img src="https://img.shields.io/badge/Python-3.13.3-3776AB.svg?style=flat&logo=python&logoColor=white" alt="python">
  </a>
  <a href="https://github.com/doog12/army-doc-gen">
    <img src="https://img.shields.io/badge/status-active-brightgreen" alt="Project Status">
  </a>
  <a href="./LICENSE">
    <img src="https://img.shields.io/badge/license-MIT-blue.svg" alt="MIT License">
  </a>
  <a href="https://github.com/psf/black">
    <img alt="Code style: black" src="https://img.shields.io/badge/code%20style-black-000000.svg">
  </a>
  <a href="https://github.com/pycqa/isort">
    <img alt="Import sorter: isort" src="https://img.shields.io/badge/imports-isort-ef8336.svg">
  </a>
  <a href="https://pre-commit.com/">
    <img alt="pre-commit enabled" src="https://img.shields.io/badge/pre--commit-enabled-brightgreen.svg">
  </a>
</p>

---

## ⚙️ Функціональність

- Авторизація за паролем  
- Кроковий вибір документа  
- Перегляд PDF-прев’ю (через Google Drive)  
- Асинхронне завантаження DOCX-шаблону за один клік  
- Підтримка заяв та рапортів (з розподілом на командирів/начальників)  
- Максимальне очищення зайвих повідомлень
- Інтеграція з Google Drive для зберігання шаблонів
- Розділ FAQ (/faq)
- Розділ піддтримки (/help)

---

## 🧩 Технології

- [Python 3.11+](https://www.python.org/)  
- [Aiogram v3](https://docs.aiogram.dev)  
- [Dotenv](https://saurabh-kumar.com/python-dotenv/)  
- [FSM (Finite State Machine)](https://docs.aiogram.dev/en/latest/dispatcher/finite_state_machine/index.html#) для керування станами користувача  
- [Aiohttp](https://docs.aiohttp.org/en/stable/) для асинхронного завантаження файлів
- [Logging](https://docs.python.org/3/library/logging.html) для еффективного логування 

---

## 📁 Структура проєкту

```
project/
├── main.py                   # Запуск бота
├── .env                      # Секрети (токен, пароль)
├── config.py                 # Конфіг з ID документів
├── handlers/
│   ├── auth.py               # Авторизація користувача
│   ├── callbacks.py          # Обробка натискань кнопок
│   ├── faq.py                # FAQ
│   └── help.py               # Help
├── modules/
│   └── downloadFile.py       # Логіка завантаження DOCX
├── configs/
│   ├── faqText.py            # Текст для FAQ
│   └── helpText.py           # Текст для Help
├── keyboards/
│   └── inline.py             # Клавіатури
├── requirements.txt          # Список бібліотек
├── .gitignore
```

---

## 🛠️ Налаштування

1. Клонуй репозиторій:

```bash
git clone https://github.com/doog12/army-doc-gen.git
cd army-doc-gen
```

2. Створи `.env` файл в корні проєкта:

```env
TELEGRAM_BOT_TOKEN=your_token_here
BOT_PASSWORD=your_password_here

ADMIN_USERNAME="@admin_username"
CHIEF_NUMBER="380661111111"
```

3. Встанови залежності:

```bash
pip install -r requirements.txt
```

3. Налаштуй конфігурацію

У файлі `config.example.py` зберігаються **прикладові значення** для ID шаблонів Google Drive, які використовуються в боті.  
Щоб запустити бота, створи власний файл `config.py`, базуючись на `config.example.py`:

Linux:
```bash
cp config.example.py config.py
```

Windows:
```cmd
copy config.example.py config.py
```

У файлі `config.py` потрібно прописати реальні ID документів, які ти хочеш використовувати.

> ❗ **Не додавай `config.py` до репозиторію!**  
> Він уже доданий до `.gitignore`, щоб уникнути витоку чутливих даних.

4. Запусти бота:

```bash
python main.py
```

---

## 🧼 Форматування коду

Цей проєкт використовує [`pre-commit`](https://pre-commit.com/) для автоматичного форматування коду перед кожним комітом. Під капотом використовуються:

- [`black`](https://github.com/psf/black) — автоматичне форматування Python-коду
- [`isort`](https://pycqa.github.io/isort/) — сортування імпортів

---

## 📝 Приклад використання

1. Користувач запускає бота командою `/start`  
2. Вводить пароль  
3. Обирає:
    - Тип документа (рапорт, заява)
    - Отримувача (командир/начальник)
    - Підтип (відпустка, прийняття на забезпечення тощо)
4. Завантажує готовий DOCX-файл  

---

## 🔒 Безпека

- Бот не зберігає особисті дані користувачів  
- Доступ до функцій тільки після авторизації  

---

## 📌 TODO

- Реалізація ролей (admin/user)  
- База користувачів з ролями
- Адмін-панель для управління шаблонами
- Підтримка заповнення шаблону даними автоматично (генерація)
- Збереження осіб після авторизації за допомогою Telegram UserID

---

## 📬 Зворотній зв'язок
Для зворотного зв’язку або багрепортів:

[![Telegram](https://img.shields.io/badge/-Telegram-090909?style=for-the-badge&logo=telegram&logoColor=27A0D9)](https://t.me/doog121)
[![E-mail](https://img.shields.io/badge/-Email-090909?style=for-the-badge&logo=gmail&logoColor=27A0D9)](mailto:drannikov.kirill@gmail.com)
[![LinkedIn](https://img.shields.io/badge/-LinkedIn-090909?style=for-the-badge&logo=linkedin&logoColor=007BB6)](https://www.linkedin.com/in/kirilldrannikov/)