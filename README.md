# 💰 TacketSmart AI

TacketSmart AI is an AI-powered smart budgeting application that helps users create practical budget recommendations based on their budget amount and requirements.

## 🚀 Features

- 🏠 Home Budget Planning
- 🎉 Party Budget Planning
- 💎 Jewelry Budget Planning
- 🤖 Gemini AI Budget Recommendations
- 🔄 Fallback recommendation when AI is temporarily unavailable
- 🌐 FastAPI backend
- 💻 Simple responsive web interface
- 📚 Swagger API documentation

## 🛠️ Technologies Used

- Python
- FastAPI
- Uvicorn
- HTML
- CSS
- JavaScript
- Google Gemini API
- Pydantic
- Python-dotenv

## 📁 Project Structure

```text
tacketsmart/
│
├── ai/
│   ├── gemini_service.py
│   ├── image_service.py
│   └── __init__.py
│
├── app/
│   ├── config.py
│   ├── main.py
│   ├── models.py
│   ├── routes.py
│   └── __init__.py
│
├── outputs/
├── services/
├── static/
│
├── templates/
│   └── index.html
│
├── .env
├── .env.example
├── .gitignore
├── README.md
└── requirements.txt