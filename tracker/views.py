# tracker/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Count, Avg
from django.http import JsonResponse
from PyPDF2 import PdfReader

from .models import Application, DSAProblem, AptitudeQuestion
from .forms import ApplicationForm, DSAProblemForm, AptitudeQuestionForm

import json
import random
from pathlib import Path
from .models import ResumeData


from django.views.decorators.csrf import csrf_exempt
from tracker.models import ResumeData, InterviewSession, InterviewQuestion   # <-- from Module 3 (adjust model name if different)

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

import spacy
import re
import nltk
from nltk.corpus import stopwords



# -------------------- spaCy NLP --------------------
nlp = spacy.load("en_core_web_sm")
COMMON_SKILLS = [
    "python", "java", "c++", "sql", "javascript", "django", "react",
    "html", "css", "excel", "power bi", "tableau", "data analysis",
    "machine learning", "nlp"
]

try:
    STOPWORDS = set(stopwords.words('english'))
except LookupError:
    nltk.download('stopwords')
    STOPWORDS = set(stopwords.words('english'))

def extract_skills_from_text(text):
    """Extract skills from resume text based on COMMON_SKILLS"""
    tokens = [token.text for token in nlp(text) if token.is_alpha]
    skills_found = {skill: 0 for skill in COMMON_SKILLS}
    for skill in COMMON_SKILLS:
        if skill.lower() in tokens:
            skills_found[skill] = 100  # simple 100% match if found
    return skills_found

# -------------------- Application CRUD --------------------
def application_list(request):
    status_filter = request.GET.get('status')
    if status_filter:
        applications = Application.objects.filter(status=status_filter)
    else:
        applications = Application.objects.all()
    return render(request, 'tracker/application_list.html', {'applications': applications})

def application_add(request):
    if request.method == 'POST':
        form = ApplicationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Application added successfully!')
            return redirect('application_list')
    else:
        form = ApplicationForm()
    return render(request, 'tracker/application_form.html', {'form': form})

def application_edit(request, pk):
    application = get_object_or_404(Application, pk=pk)
    if request.method == 'POST':
        form = ApplicationForm(request.POST, instance=application)
        if form.is_valid():
            form.save()
            messages.success(request, "Application updated successfully ✏️")
            return redirect('application_list')
    else:
        form = ApplicationForm(instance=application)
    return render(request, 'tracker/application_form.html', {'form': form})

def application_delete(request, pk):
    application = get_object_or_404(Application, pk=pk)
    if request.method == 'POST':
        application.delete()
        messages.success(request, "Application deleted successfully 🗑️")
        return redirect('application_list')
    return render(request, 'tracker/application_confirm_delete.html', {'application': application})

# -------------------- DSAProblem CRUD --------------------
# tracker/views.py

from collections import defaultdict
from .models import DSAProblem

def problem_list(request):
    problems = DSAProblem.objects.all()

    # Count solved and pending problems overall
    solved_count = problems.filter(status='Solved').count()
    pending_count = problems.filter(status='Pending').count()

    # Count solved/pending per topic
    topic_counts = defaultdict(lambda: {'solved': 0, 'pending': 0})
    for p in problems:
        if p.status == 'Solved':
            topic_counts[p.topic]['solved'] += 1
        else:
            topic_counts[p.topic]['pending'] += 1

    # Convert to list of tuples for template
    topic_counts_items = [(topic, counts) for topic, counts in topic_counts.items()]

    return render(request, 'tracker/problem_list.html', {
        'problems': problems,
        'solved_count': solved_count,
        'pending_count': pending_count,
        'topics': DSAProblem.TOPICS,
        'topic_counts_items': topic_counts_items,
    })



def problem_create(request):
    if request.method == 'POST':
        form = DSAProblemForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Problem added ✅")
            return redirect('problem_list')
    else:
        form = DSAProblemForm()
    return render(request, 'tracker/problem_form.html', {'form': form})

def problem_update(request, pk):
    problem = get_object_or_404(DSAProblem, pk=pk)
    if request.method == 'POST':
        form = DSAProblemForm(request.POST, instance=problem)
        if form.is_valid():
            form.save()
            messages.success(request, "Problem updated ✏️")
            return redirect('problem_list')
    else:
        form = DSAProblemForm(instance=problem)
    return render(request, 'tracker/problem_form.html', {'form': form})

def problem_delete(request, pk):
    problem = get_object_or_404(DSAProblem, pk=pk)
    if request.method == 'POST':
        problem.delete()
        messages.success(request, "Problem deleted 🗑️")
        return redirect('problem_list')
    return render(request, 'tracker/problem_confirm_delete.html', {'problem': problem})

# -------------------- AptitudeQuestion CRUD --------------------
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Avg
from django.db.models.functions import TruncDate
from .models import AptitudeQuestion
from .forms import AptitudeQuestionForm

# -------------------- Aptitude CRUD --------------------
def aptitude_list(request):
    topic_filter = str(request.GET.get('topic', ''))
    status_filter = str(request.GET.get('status', ''))
    qs = AptitudeQuestion.objects.all().order_by('-id')

    if topic_filter:
        qs = qs.filter(topic=topic_filter)
    if status_filter:
        qs = qs.filter(status=status_filter)

    # Overall counts
    solved_count = qs.filter(status='Solved').count()
    unsolved_count = qs.filter(status='Unsolved').count()

    # Counts per topic
    topic_counts = {}
    for code, name in AptitudeQuestion.TOPICS:
        topic_qs = qs.filter(topic=code)
        topic_counts[name] = {
            'solved': topic_qs.filter(status='Solved').count(),
            'unsolved': topic_qs.filter(status='Unsolved').count()
        }

    return render(request, 'tracker/aptitude_list.html', {
        'questions': qs,
        'topics': AptitudeQuestion.TOPICS,
        'solved_count': solved_count,
        'unsolved_count': unsolved_count,
        'topic_counts': topic_counts,
    })


def aptitude_create(request):
    if request.method == 'POST':
        form = AptitudeQuestionForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Question added ✅")
            return redirect('aptitude_list')
    else:
        form = AptitudeQuestionForm()
    return render(request, 'tracker/aptitude_form.html', {'form': form})


def aptitude_update(request, pk):
    question = get_object_or_404(AptitudeQuestion, pk=pk)
    if request.method == 'POST':
        form = AptitudeQuestionForm(request.POST, instance=question)
        if form.is_valid():
            form.save()
            messages.success(request, "Question updated ✏️")
            return redirect('aptitude_list')
    else:
        form = AptitudeQuestionForm(instance=question)
    return render(request, 'tracker/aptitude_form.html', {'form': form})


def aptitude_delete(request, pk):
    question = get_object_or_404(AptitudeQuestion, pk=pk)
    if request.method == 'POST':
        question.delete()
        messages.success(request, "Question deleted 🗑️")
        return redirect('aptitude_list')
    return render(request, 'tracker/aptitude_confirm_delete.html', {'question': question})

##########################################################################################################################

from django.db.models import Count, Q
from django.utils.dateparse import parse_date
from django.db.models.functions import TruncMonth
from .models import Application

# ---------------- Placement Analytics ----------------
def placement_status_distribution(request):
    qs = Application.objects.all()

    company = request.GET.get('company')
    status = request.GET.get('status')
    month = request.GET.get('month')  # format: YYYY-MM

    if company:
        company_list = [c.strip() for c in company.split(',') if c.strip()]
        qs = qs.filter(company_name__in=company_list)
    if status:
        status_list = [s.strip().lower() for s in status.split(',') if s.strip()]
        qs = qs.filter(status__in=[s.capitalize() for s in status_list])
    if month:
        try:
            year, mon = map(int, month.split('-'))
            qs = qs.filter(application_date__year=year, application_date__month=mon)
        except:
            pass

    data = qs.values('status').annotate(count=Count('id')).order_by('status')
    result = [{'status': d['status'], 'count': d['count']} for d in data]

    return JsonResponse(result, safe=False)


def placement_applications_per_company(request):
    qs = Application.objects.all()

    company = request.GET.get('company')
    status = request.GET.get('status')
    month = request.GET.get('month')  # format: YYYY-MM

    if company:
        company_list = [c.strip() for c in company.split(',') if c.strip()]
        qs = qs.filter(company_name__in=company_list)
    if status:
        status_list = [s.strip().lower() for s in status.split(',') if s.strip()]
        qs = qs.filter(status__in=[s.capitalize() for s in status_list])
    if month:
        try:
            year, mon = map(int, month.split('-'))
            qs = qs.filter(application_date__year=year, application_date__month=mon)
        except:
            pass

    data = qs.values('company_name').annotate(count=Count('id')).order_by('company_name')
    result = [{'company_name': d['company_name'], 'count': d['count']} for d in data]

    return JsonResponse(result, safe=False)


from django.http import JsonResponse
from django.db.models import Count, Avg, Q
from .models import DSAProblem, AptitudeQuestion
from datetime import datetime

# -------------------- DSA Analytics --------------------

from django.http import JsonResponse
from django.db.models import Count, Avg, Q
from .models import Application, DSAProblem, AptitudeQuestion
from datetime import datetime

# ------------------ DSA ------------------

def dsa_progress_per_topic(request):
    qs = DSAProblem.objects.all()
    topic = request.GET.get('topic')
    status = request.GET.get('status')
    from_date = request.GET.get('from_date')
    to_date = request.GET.get('to_date')

    if topic:
        qs = qs.filter(topic=topic)
    if status:
        qs = qs.filter(status=status)
    if from_date:
        qs = qs.filter(date_solved__gte=from_date)
    if to_date:
        qs = qs.filter(date_solved__lte=to_date)

    data = qs.values('topic').annotate(
        solved=Count('id', filter=Q(status='Solved')),
        pending=Count('id', filter=Q(status='Pending'))
    ).order_by('topic')

    # return solved count for charts
    result = [{'topic': d['topic'], 'solved': d['solved']} for d in data]
    return JsonResponse(result, safe=False)


from django.http import JsonResponse
from django.db.models import Count
from .models import DSAProblem

def dsa_progress_over_time(request):
    qs = DSAProblem.objects.filter(status='Solved')
    topic = request.GET.get('topic')
    from_date = request.GET.get('from_date')
    to_date = request.GET.get('to_date')

    if topic:
        qs = qs.filter(topic=topic)
    if from_date:
        qs = qs.filter(date_solved__gte=from_date)
    if to_date:
        qs = qs.filter(date_solved__lte=to_date)

    data = qs.values('date_solved').annotate(
        solved=Count('id')
    ).order_by('date_solved')

    # ✅ Ensure frontend expects "date", not "date_solved"
    result = []
    for d in data:
        if d['date_solved']:
            result.append({
                'date': d['date_solved'].strftime('%Y-%m-%d'),
                'solved': d['solved']
            })
    return JsonResponse(result, safe=False)


# ------------------ Aptitude ------------------

def aptitude_average_per_topic(request):
    qs = AptitudeQuestion.objects.all()
    topic = request.GET.get('topic')
    status = request.GET.get('status')
    from_date = request.GET.get('from_date')
    to_date = request.GET.get('to_date')

    if topic:
        qs = qs.filter(topic=topic)
    if status:
        qs = qs.filter(status=status)
    if from_date:
        qs = qs.filter(created_at__date__gte=from_date)
    if to_date:
        qs = qs.filter(created_at__date__lte=to_date)

    data = qs.values('topic').annotate(
        avg_score=Avg('score')
    ).order_by('topic')

    result = [{'topic': d['topic'], 'avg_score': round(d['avg_score'] or 0, 1)} for d in data]
    return JsonResponse(result, safe=False)


def aptitude_scores_over_time(request):
    qs = AptitudeQuestion.objects.all()
    topic = request.GET.get('topic')
    status = request.GET.get('status')
    from_date = request.GET.get('from_date')
    to_date = request.GET.get('to_date')

    if topic:
        qs = qs.filter(topic=topic)
    if status:
        qs = qs.filter(status=status)
    if from_date:
        qs = qs.filter(created_at__date__gte=from_date)
    if to_date:
        qs = qs.filter(created_at__date__lte=to_date)

    data = qs.values('created_at__date').annotate(
        avg_score=Avg('score')
    ).order_by('created_at__date')

    result = [{'date': d['created_at__date'].strftime('%Y-%m-%d'), 'avg_score': round(d['avg_score'] or 0, 1)} for d in data]
    return JsonResponse(result, safe=False)





# -------------------- Resume Analyzer --------------------
# -------------------- Resume Analyzer (Updated) --------------------
# Install RapidFuzz first
# pip install rapidfuzz

# from rapidfuzz import fuzz, process

# import io
# from PyPDF2 import PdfReader

def extract_text_from_pdf(pdf_file):
    """Extract text from PDF"""
    reader = PdfReader(pdf_file)
    text = ""
    for page in reader.pages:
        text += page.extract_text() or ""
    return text.lower()

# def extract_text_from_pdf(pdf_file):
#     """Extract text from a PDF file object."""
#     pdf_reader = PdfReader(pdf_file)
#     text = ""
#     for page in pdf_reader.pages:
#         text += page.extract_text() or ""
#     return text

# # Updated skill extraction with fuzzy matching
# def extract_skills_fuzzy(text):
#     """Extract skills from text using fuzzy matching."""
#     text_lower = text.lower()
#     matched_skills = []
#     for skill in COMMON_SKILLS:
#         # If fuzzy similarity > 80%, consider it a match
#         if fuzz.partial_ratio(skill.lower(), text_lower) > 80:
#             matched_skills.append(skill)
#     return matched_skills

# Updated resume analyzer
# def resume_analyzer(request):
#     overall_score = None
#     skills_match = {}
#     job_skills = []

#     if request.method == "POST" and request.FILES.get("resume"):
#         resume_file = request.FILES["resume"]
#         resume_text = extract_text_from_pdf(resume_file).lower()

#         job_description = request.POST.get("job_description", "")
#         # Extract skills from job description using predefined COMMON_SKILLS
#         job_skills = [skill for skill in COMMON_SKILLS if skill.lower() in job_description.lower()]

#         if job_skills:
#             for skill in job_skills:
#                 skills_match[skill] = 100 if skill.lower() in resume_text else 0

#             overall_score = int(sum(skills_match.values()) / len(skills_match))

#     return render(request, "tracker/resume_analyzer.html", {
#         "overall_score": overall_score,
#         "skills_match": skills_match,
#         "job_skills": job_skills,
#     })

# def resume_analyzer(request):
#     overall_score = None
#     skills_match = {}
#     job_skills = []
#     matched_skills = []
#     missing_skills = []

#     if request.method == "POST" and request.FILES.get("resume"):
#         resume_file = request.FILES["resume"]
#         resume_text = extract_text_from_pdf(resume_file).lower()

#         job_description = request.POST.get("job_description", "")
#         job_skills = [skill for skill in COMMON_SKILLS if skill.lower() in job_description.lower()]

#         if job_skills:
#             for skill in job_skills:
#                 if skill.lower() in resume_text:
#                     skills_match[skill] = 100
#                     matched_skills.append(skill)
#                 else:
#                     skills_match[skill] = 0
#                     missing_skills.append(skill)

#             overall_score = int(sum(skills_match.values()) / len(skills_match))

#     return render(request, "tracker/resume_analyzer.html", {
#         "overall_score": overall_score,
#         "skills_match": skills_match,
#         "job_skills": job_skills,
#         "matched_skills": matched_skills,
#         "missing_skills": missing_skills,
#     })

import PyPDF2
from django.shortcuts import render
from .models import ResumeData

# Predefined list of common skills
COMMON_SKILLS = [
    "Python", "Java", "C++", "SQL", "Machine Learning",
    "Data Analysis", "Deep Learning", "Communication",
    "Problem Solving", "Project Management", "Excel",
    "Power BI", "Tableau", "AWS", "Docker", "Kubernetes"
]

def extract_text_from_pdf(file):
    pdf_reader = PyPDF2.PdfReader(file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text() + " "
    return text.lower()


def save_resume_data(user, skills_list, projects_list=None):
    """Save extracted skills/projects into ResumeData model"""
    skills = ",".join(skills_list)
    projects = ",".join(projects_list) if projects_list else ""
    obj, created = ResumeData.objects.update_or_create(
        user=user,
        defaults={"skills": skills, "projects": projects}
    )
    return obj


def resume_analyzer(request):
    overall_score = None
    skills_match = {}
    job_skills = []
    matched_skills = []
    missing_skills = []

    extracted_skills = []  # will store all skills found in resume

    if request.method == "POST" and request.FILES.get("resume"):
        resume_file = request.FILES["resume"]
        resume_text = extract_text_from_pdf(resume_file)

        # Extract job description
        job_description = request.POST.get("job_description", "").lower()

        # Detect skills from job description (optional for comparison)
        job_skills = [skill for skill in COMMON_SKILLS if skill.lower() in job_description]

        # Detect all skills in resume
        for skill in COMMON_SKILLS:
            if skill.lower() in resume_text:
                skills_match[skill] = 100
                extracted_skills.append(skill)
                if skill in job_skills:
                    matched_skills.append(skill)
            else:
                skills_match[skill] = 0
                if skill in job_skills:
                    missing_skills.append(skill)

        # Overall score: percentage of JD skills present in resume
        if job_skills:
            overall_score = int(sum([skills_match[s] for s in job_skills]) / len(job_skills))
        else:
            overall_score = None  # No JD skills provided

        # Save extracted skills to ResumeData for the logged-in user
        if request.user.is_authenticated:
            save_resume_data(request.user, extracted_skills)

    return render(request, "tracker/resume_analyzer.html", {
        "overall_score": overall_score,
        "skills_match": skills_match,
        "job_skills": job_skills,
        "matched_skills": matched_skills,
        "missing_skills": missing_skills,
    })






# -------------------- Dashboard --------------------
# def analytics_dashboard(request):
#     return render(request, 'tracker/analytics_dashboard.html')
from django.shortcuts import render
from django.http import JsonResponse
from django.db.models import Count, Avg
from .models import Application, DSAProblem, AptitudeQuestion


# =================== DASHBOARD ===================
def analytics_dashboard(request):
    # Placement Tracker filters
    companies = Application.objects.values_list("company_name", flat=True).distinct()
    placement_statuses = Application.objects.values_list("status", flat=True).distinct()
    
    # DSA Tracker filters
    dsa_topics = DSAProblem.objects.values_list("topic", flat=True).distinct()
    dsa_statuses = DSAProblem.objects.values_list("status", flat=True).distinct()
    
    # Aptitude Tracker filters
    apt_topics = AptitudeQuestion.objects.values_list("topic", flat=True).distinct()
    apt_statuses = AptitudeQuestion.objects.values_list("status", flat=True).distinct()

    return render(request, "tracker/analytics_dashboard.html", {
        "companies": companies,
        "placement_statuses": placement_statuses,
        "dsa_topics": dsa_topics,
        "dsa_statuses": dsa_statuses,
        "apt_topics": apt_topics,
        "apt_statuses": apt_statuses,
    })


# =================== PLACEMENT APIs ===================
def placement_status_distribution(request):
    qs = Application.objects.all()

    company = request.GET.get("company")
    status = request.GET.get("status")
    month = request.GET.get("month")

    if company:
        qs = qs.filter(company_name=company)
    if status:
        qs = qs.filter(status=status)
    if month:  # format YYYY-MM
        year, mon = month.split("-")
        qs = qs.filter(application_date__year=year, application_date__month=mon)

    data = qs.values("status").annotate(count=Count("id"))
    return JsonResponse(list(data), safe=False)


def placement_applications_per_company(request):
    qs = Application.objects.all()

    company = request.GET.get("company")
    status = request.GET.get("status")
    month = request.GET.get("month")

    if company:
        qs = qs.filter(company_name=company)
    if status:
        qs = qs.filter(status=status)
    if month:
        year, mon = month.split("-")
        qs = qs.filter(application_date__year=year, application_date__month=mon)

    data = qs.values("company_name").annotate(count=Count("id"))
    return JsonResponse(list(data), safe=False)


# =================== DSA APIs ===================
def dsa_progress_per_topic(request):
    qs = DSAProblem.objects.all()

    topic = request.GET.get("topic")
    status = request.GET.get("status")
    from_date = request.GET.get("from_date")
    to_date = request.GET.get("to_date")

    if topic:
        qs = qs.filter(topic=topic)
    if status:
        qs = qs.filter(status=status)
    if from_date:
        qs = qs.filter(date_solved__gte=from_date)
    if to_date:
        qs = qs.filter(date_solved__lte=to_date)

    data = qs.values("topic").annotate(solved=Count("id"))
    return JsonResponse(list(data), safe=False)


def dsa_progress_over_time(request):
    qs = DSAProblem.objects.filter(status="Solved")

    topic = request.GET.get("topic")
    status = request.GET.get("status")
    from_date = request.GET.get("from_date")
    to_date = request.GET.get("to_date")

    if topic:
        qs = qs.filter(topic=topic)
    if status:
        qs = qs.filter(status=status)
    if from_date:
        qs = qs.filter(date_solved__gte=from_date)
    if to_date:
        qs = qs.filter(date_solved__lte=to_date)

    data = qs.values("date_solved").annotate(solved=Count("id")).order_by("date_solved")
    return JsonResponse(list(data), safe=False)


# =================== APTITUDE APIs ===================
def aptitude_average_per_topic(request):
    qs = AptitudeQuestion.objects.all()

    topic = request.GET.get("topic")
    status = request.GET.get("status")
    from_date = request.GET.get("from_date")
    to_date = request.GET.get("to_date")

    if topic:
        qs = qs.filter(topic=topic)
    if status:
        qs = qs.filter(status=status)
    if from_date:
        qs = qs.filter(created_at__date__gte=from_date)
    if to_date:
        qs = qs.filter(created_at__date__lte=to_date)

    data = qs.values("topic").annotate(avg_score=Avg("score"))
    return JsonResponse(list(data), safe=False)


def aptitude_scores_over_time(request):
    qs = AptitudeQuestion.objects.all()

    topic = request.GET.get("topic")
    status = request.GET.get("status")
    from_date = request.GET.get("from_date")
    to_date = request.GET.get("to_date")

    if topic:
        qs = qs.filter(topic=topic)
    if status:
        qs = qs.filter(status=status)
    if from_date:
        qs = qs.filter(created_at__date__gte=from_date)
    if to_date:
        qs = qs.filter(created_at__date__lte=to_date)

    data = qs.extra(select={"date": "date(created_at)"}).values("date").annotate(avg_score=Avg("score")).order_by("date")
    return JsonResponse(list(data), safe=False)

# --------------------------------mock interview view -----------------------------------------
import json, os, random
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from .models import ResumeData, InterviewSession, InterviewQuestion

QUESTIONS_FILE = os.path.join(settings.BASE_DIR, "tracker", "data", "questions.json")

def load_questions():
    with open(QUESTIONS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def pick_questions(role, count=5):
    """Pick random questions from JSON for HR/Technical."""
    all_qs = load_questions()
    role_qs = [q for q in all_qs if q["role"].lower() == role.lower()]
    return random.sample(role_qs, min(count, len(role_qs)))

def generate_resume_questions(user, session, count_per_category=2):
    """Generate multiple custom questions from ResumeData and save in DB."""
    try:
        resume = ResumeData.objects.get(user=user)
    except ResumeData.DoesNotExist:
        return []

    questions = []

    # ---- Skills Questions ----
    if resume.skills:
        skills = [s.strip() for s in resume.skills.split(',')]
        for skill in skills[:count_per_category]:
            questions.append({
                "text": f"Can you explain how you have applied your skills in {skill}?",
                "keywords": [skill.lower()],
                "max_score": 5,
                "role": "Resume"
            })

    # ---- Projects Questions ----
    if resume.projects:
        projects = [p.strip() for p in resume.projects.split(',')]
        for proj in projects[:count_per_category]:
            questions.append({
                "text": f"Tell me more about your project: {proj}. What challenges did you face?",
                "keywords": ["challenge", "impact", "team", "tools"],
                "max_score": 5,
                "role": "Resume"
            })

    # ---- Experience Questions ----
    if resume.experience:
        experiences = [e.strip() for e in resume.experience.split(',')]
        for exp in experiences[:count_per_category]:
            questions.append({
                "text": f"Describe your experience working at {exp}.",
                "keywords": ["responsibility", "task", "contribution", "impact"],
                "max_score": 5,
                "role": "Resume"
            })

    # ---- Education Questions ----
    if resume.education:
        edus = [e.strip() for e in resume.education.split(',')]
        for edu in edus[:count_per_category]:
            questions.append({
                "text": f"How did your education at {edu} prepare you for this role?",
                "keywords": ["knowledge", "foundation", "skills", "learning"],
                "max_score": 5,
                "role": "Resume"
            })

    # Save questions to DB
    saved_questions = []
    for q in questions:
        iq = InterviewQuestion.objects.create(
            session=session,
            text=q["text"],
            role=q["role"],
            max_score=q["max_score"],
            keywords=q["keywords"]
        )
        saved_questions.append({
            "id": iq.id,
            "text": iq.text,
            "max_score": iq.max_score
        })

    return saved_questions

# =======-------------------------------------------------------------------------------
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
import json


@csrf_exempt
@login_required
def start_interview(request):
    """Start interview by fetching 5 random questions for selected role."""
    if request.method != "POST":
        return JsonResponse({"error": "Invalid method"}, status=405)

    data = json.loads(request.body)
    role = data.get("role", "HR").strip()

    # ---- Prevent duplicate sessions ----
    existing_sessions = InterviewSession.objects.filter(user=request.user, role=role)
    if existing_sessions.count() > 1:
        # Keep the latest one and delete extras
        latest = existing_sessions.latest("created_at")
        existing_sessions.exclude(id=latest.id).delete()
        session = latest
    elif existing_sessions.exists():
        session = existing_sessions.first()
    else:
        session = InterviewSession.objects.create(user=request.user, role=role)

    # ---- Resume role special handling ----
    if role.lower() == "resume":
        questions_list = generate_resume_questions(request.user, session)
        return JsonResponse({"questions": questions_list}, safe=False)

    # ---- Fetch questions for other roles ----
    questions = list(session.questions.all()[:5])  # get first 5 or random
    if not questions:
        return JsonResponse({"error": "No questions available. Please seed them first."}, status=404)

    questions_list = [
        {"id": q.id, "text": q.text, "max_score": q.max_score}
        for q in questions
    ]

    return JsonResponse({"questions": questions_list}, safe=False)


@csrf_exempt
@login_required
def submit_answer(request):
    """Submit answer, save to DB, and return score + feedback."""
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            qid = data.get("id")
            answer = data.get("answer", "")

            if not answer.strip():
                return JsonResponse({"error": "Answer cannot be empty"}, status=400)

            question = InterviewQuestion.objects.get(id=qid)
            
            # Score using keywords
            keywords = question.keywords or []
            max_score = question.max_score or 5
            score = sum(1 for kw in keywords if kw.lower() in answer.lower())
            score = min(score, max_score)

            if score == 0:
                feedback = "Try to include more relevant details."
            elif score < max_score:
                feedback = "Good attempt! You covered some points but can expand."
            else:
                feedback = "Excellent! Very detailed and complete."

            # Save answer and score
            question.answer = answer
            question.score = score
            question.save()

            return JsonResponse({"score": score, "feedback": feedback})

        except InterviewQuestion.DoesNotExist:
            return JsonResponse({"error": "Question not found"}, status=404)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Invalid method"}, status=405)


    
# --------------------------------------------------------------------------------------------

@login_required
def mock_interview_view(request):
    """Render the mock interview chat interface"""
    return render(request, "tracker/chat.html")



