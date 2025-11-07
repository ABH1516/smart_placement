import os
import sys
import django

# Add project root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Set Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'smart_placement.settings')
django.setup()

from tracker.models import InterviewQuestion, InterviewSession
from django.contrib.auth.models import User

# -----------------------------
# Configuration
# -----------------------------
QUESTIONS = {
    "HR": [
        {
            "text": "Tell me about yourself.",
            "keywords": ["experience", "skills", "education"],
            "max_score": 5
        },
        {
            "text": "Why do you want to join this company?",
            "keywords": ["motivation", "interest", "culture"],
            "max_score": 5
        },
        {
            "text": "What are your strengths?",
            "keywords": ["strengths", "skills", "abilities"],
            "max_score": 5
        },
        {
            "text": "What are your weaknesses?",
            "keywords": ["weaknesses", "improvement", "growth"],
            "max_score": 5
        },
        {
            "text": "Where do you see yourself in 5 years?",
            "keywords": ["career goals", "planning", "growth"],
            "max_score": 5
        },
        # Add 2 more HR questions
        {
            "text": "Describe a challenging situation you faced and how you overcame it.",
            "keywords": ["challenge", "problem solving", "resilience"],
            "max_score": 5
        },
        {
            "text": "How do you handle conflict in a team?",
            "keywords": ["conflict", "teamwork", "communication"],
            "max_score": 5
        }
    ],
    "Technical": [
        {
            "text": "Explain polymorphism in OOP.",
            "keywords": ["polymorphism", "object oriented", "methods"],
            "max_score": 5
        },
        {
            "text": "What is a relational database?",
            "keywords": ["database", "tables", "SQL"],
            "max_score": 5
        },
        {
            "text": "Explain the difference between stack and queue.",
            "keywords": ["stack", "queue", "LIFO", "FIFO"],
            "max_score": 5
        },
        {
            "text": "What is a REST API?",
            "keywords": ["REST", "API", "HTTP"],
            "max_score": 5
        },
        {
            "text": "Explain the concept of recursion.",
            "keywords": ["recursion", "function", "call"],
            "max_score": 5
        },
        # Add 2 more Technical questions
        {
            "text": "What are indexes in a database and why are they important?",
            "keywords": ["indexes", "database", "performance"],
            "max_score": 5
        },
        {
            "text": "Explain the difference between GET and POST requests.",
            "keywords": ["GET", "POST", "HTTP", "requests"],
            "max_score": 5
        }
    ],
    "Resume": [
        {
            "text": "List your key projects and explain your role.",
            "keywords": ["projects", "role", "contribution"],
            "max_score": 5
        },
        {
            "text": "What skills from your resume are most relevant for this position?",
            "keywords": ["skills", "relevant", "position"],
            "max_score": 5
        },
        {
            "text": "Explain a gap in your resume if any.",
            "keywords": ["gap", "reason", "experience"],
            "max_score": 5
        },
        # Add 2 more Resume questions
        {
            "text": "Which achievement in your resume are you most proud of?",
            "keywords": ["achievement", "success", "proud"],
            "max_score": 5
        },
        {
            "text": "Describe your experience with teamwork or leadership.",
            "keywords": ["teamwork", "leadership", "experience"],
            "max_score": 5
        }
    ]
}

# -----------------------------
# Seed function
# -----------------------------
def seed_questions():
    # Optional: Delete old questions
    print("Deleting existing questions...")
    InterviewQuestion.objects.all().delete()

    # You can also create a dummy session for seeding
    dummy_user = User.objects.first()
    if not dummy_user:
        print("No user found. Please create a superuser first.")
        return

    print("Creating questions...")
    for role, qs in QUESTIONS.items():
        session = InterviewSession.objects.create(user=dummy_user, role=role)
        for q in qs:
            InterviewQuestion.objects.create(
                session=session,
                text=q["text"],
                max_score=q["max_score"],
                keywords=q["keywords"]
            )
    print("Seeding complete!")

# -----------------------------
# Run script
# -----------------------------
if __name__ == "__main__":
    seed_questions()
