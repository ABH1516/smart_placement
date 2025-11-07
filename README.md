# Smart Placement Tracker

A **Django-based web application** to help students and job seekers track their **DSA problems**, **aptitude questions**, **job applications**, and practice with a **mock interview bot**.

---

## 🛠 Features

### 1. DSA Problem Tracker
- Track your **DSA problem-solving progress**.
- Filter by **topic** and **status** (Solved/Pending).
- **Dashboard charts**: Overall and topic-wise progress.

### 2. Aptitude Question Tracker
- Maintain a record of **aptitude questions**.
- Filter by topic and status (Solved/Unsolved).
- Topic-wise **performance visualization**.

### 3. Job Application Tracker
- Keep track of **applications**, **status** (Applied, Interview, Rejected, Selected), and **notes**.
- Add, edit, and delete applications.
- Visual status badges for quick glance.

### 4. Mock Interview Bot
- Conduct mock interviews:
  - HR-based
  - Technical
  - Resume-based
- Optional **timer** for each question.
- Interactive modal-based Q&A experience.

---

## 🎨 UI/UX
- Modern, responsive design using **Bootstrap 5**.
- **Charts and dashboards** for visual progress.
- Modal pop-ups and badges for better UX.

---

## ⚙️ Setup & Installation

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/smart_placement.git
cd smart_placement
Create a virtual environment

bash
Copy code
python -m venv venv
source venv/bin/activate      # Linux/Mac
venv\Scripts\activate         # Windows
Install dependencies

bash
Copy code
pip install -r requirements.txt
Apply migrations

bash
Copy code
python manage.py migrate
Run the development server

bash
Copy code
python manage.py runserver
Access the app

Open your browser: http://127.0.0.1:8000/

📂 Project Structure
bash
Copy code
smart_placement/
│
├── tracker/           # Django app containing models, views, templates, static files
├── smart_placement/   # Project settings
├── db.sqlite3         # SQLite database
├── manage.py
├── requirements.txt
└── README.md
📸 Screenshots
Add screenshots of each module: DSA tracker, aptitude tracker, applications, and mock interview bot.

🔧 Future Improvements
User authentication with roles (admin/student).

Export progress reports to PDF/Excel.

Integration with external APIs for interview questions.

Enhanced scoring and analytics for mock interviews.

📄 License
This project is MIT licensed.

