import random
import openai

BASE_QUESTIONS = {
    "HR": [
        {"text": "Tell me about yourself.", "keywords": ["experience", "skills"], "max_score": 10},
        {"text": "What are your strengths?", "keywords": ["strength", "example"], "max_score": 5},
    ],
    "Technical": [
        {"text": "Explain OOP concepts with examples.", "keywords": ["inheritance", "polymorphism"], "max_score": 10},
        {"text": "What is the difference between SQL and NoSQL?", "keywords": ["schema", "scalability"], "max_score": 10},
    ],
}

def generate_questions(role="General", count=5):
    # Pick questions from the base pool
    if role in BASE_QUESTIONS:
        selected = random.sample(BASE_QUESTIONS[role], min(count, len(BASE_QUESTIONS[role])))
    else:
        selected = random.sample(BASE_QUESTIONS["HR"], min(count, len(BASE_QUESTIONS["HR"])))

    return selected

def ai_generate_questions(role="Software Developer", count=5):
    prompt = f"Generate {count} interview questions for a {role} role. Mix HR and technical."
    
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "system", "content": prompt}],
        temperature=0.7
    )
    questions = [q.strip() for q in response["choices"][0]["message"]["content"].split("\n") if q.strip()]
    
    return [{"text": q, "keywords": [], "max_score": 10} for q in questions]


def generate_resume_based_questions(skills, count=5):
    questions = []
    for skill in skills[:count]:
        questions.append({
            "text": f"Can you explain your experience with {skill}?",
            "keywords": [skill],
            "max_score": 10
        })
    return questions