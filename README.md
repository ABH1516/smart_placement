# Smart Placement Tracker 🚀

![Django](https://img.shields.io/badge/Django-4.x-green.svg)
![Python](https://img.shields.io/badge/Python-3.x-blue.svg)
![Bootstrap](https://img.shields.io/badge/Bootstrap-5-purple.svg)
![SQLite](https://img.shields.io/badge/Database-SQLite-lightgrey.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

A *full-stack Django-based web application* designed to help students and job seekers streamline their placement preparation.

Track *DSA problems, **aptitude questions, **job applications, and practice interviews with an interactive **mock interview bot*. Features dashboards with charts for progress visualization.

Perfect for managing end-to-end placement activities — built with scalable backend architecture and responsive UI.

## 🌟 Key Features

### 1. DSA Problem Tracker
- Log and track DSA problems with topic-wise filtering.
- Mark status (Solved/Pending).
- *Interactive dashboards* with overall and topic-wise progress charts.

### 2. Aptitude Question Tracker
- Record aptitude questions by topic.
- Track solved/unsolved status.
- Visual performance analytics.

### 3. Job Application Tracker
- Manage applications with details (company, role, status: Applied/Interview/Rejected/Selected).
- Add notes and deadlines.
- Status badges for quick overview.

### 4. Mock Interview Bot
- Practice interviews: HR, Technical, or Resume-based.
- Optional timer per question.
- Modal-based interactive Q&A experience.

## 🛠 Tech Stack
- *Backend*: Django (Python), REST framework basics
- *Database*: SQLite (with optimized models)
- *Frontend*: Bootstrap 5, HTML/CSS, JavaScript for interactivity
- *Charts*: Integrated visualizations for analytics
- *Version Control*: Git

## 📸 Screenshots


- Dashboard Overview: ![Dashboard](https://github.com/ABH1516/smart_placement/blob/main/screenshots/Dashboard%20(2).png) 
- DSA Tracker: ![DSA Tracker](https://github.com/ABH1516/smart_placement/blob/main/screenshots/DSA.png)
- Job Applications: ![Applications](https://github.com/ABH1516/smart_placement/blob/main/screenshots/Aptitude.png)
- Mock Interview Bot: ![Mock Interview](https://github.com/ABH1516/smart_placement/blob/main/screenshots/MockInterview.png)

## 🚀 Setup & Installation
1. Clone the repo:
   ```bash
   git clone https://github.com/ABH1516/smart_placement.git
   cd smart_placement
2.Create virtual environment:
  ```bash 
  python -m venv venv
  source venv/bin/activate  # Linux/Mac
  # or venv\Scripts\activate  # Windows
 ```
3.Install dependencies:
  ```
  pip install -r requirements.txt
  ```
4.Apply migrations:
  ```
  python manage.py migrate
  ```
5.Run server:
  ```
  python manage.py runserver
  ```
6.Access at: http://127.0.0.1:8000/

📂 Project Structure
smart_placement/
├── tracker/              # Main Django app (models, views, templates, static)
├── smart_placement/      # Project settings
├── manage.py
├── requirements.txt
└── db.sqlite3

🔮 Future Improvements

1.User authentication and multi-user support.
2.Export reports to PDF/Excel.
3.Integrate external APIs for real interview questions.
4.Advanced analytics and scoring for mocks.

📄 License
MIT License — free to use and modify!
