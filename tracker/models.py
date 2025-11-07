from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Application(models.Model):
    STATUS_CHOICES = [
        ('applied', 'Applied'), 
        ('interviewed', 'Interviewed'), 
        ('rejected', 'Rejected'),
        ('selected', 'Selected'),
    ]

    company_name = models.CharField(max_length=100)
    job_title = models.CharField(max_length=100)
    application_date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Applied')
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.company_name} - {self.job_title}"
    
class DSAProblem(models.Model):
    TOPICS = [
        ('Array', 'Array'),
        ('String', 'String'),
        ('Linked List', 'Linked List'),
        ('Stack', 'Stack'),
        ('Queue', 'Queue'),
        ('Tree', 'Tree'),
        ('Graph', 'Graph'),
        ('DP', 'Dynamic Programming'),
    ]

    title = models.CharField(max_length=200)
    topic = models.CharField(max_length=50, choices=TOPICS)
    status = models.CharField(
        max_length=20,
        choices=[('Solved', 'Solved'), ('Pending', 'Pending')],
        default='Pending'
    )
    date_solved = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.title} ({self.topic})"
    
class AptitudeQuestion(models.Model):
    TOPICS = [
        ('Quant', 'Quantitative Ability'),
        ('LR', 'Logical Reasoning'),
        ('DI', 'Data Interpretation'),
        ('Verbal', 'Verbal Ability'),
    ]
    
    STATUS = [
        ('Unsolved', 'Unsolved'),
        ('Solved', 'Solved'),
    ]
    
    title = models.CharField(max_length=200)
    topic = models.CharField(max_length=20, choices=TOPICS)
    status = models.CharField(max_length=10, choices=STATUS, default='Unsolved')
    solution = models.TextField(blank=True, null=True)  # optional solution
    created_at = models.DateTimeField(auto_now_add=True)
    score = models.IntegerField(default=0)
    
    def __str__(self):
        return self.title
    

# tracker/models.py

class InterviewSession(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'role')


class InterviewQuestion(models.Model):
    session = models.ForeignKey(InterviewSession, on_delete=models.CASCADE, related_name="questions")
    text = models.TextField()
    role = models.CharField(max_length=50, default="HR")
    max_score = models.IntegerField(default=5)
    keywords = models.JSONField(default=list, blank=True)
    answer = models.TextField(blank=True, null=True)  # store user’s answer
    score = models.IntegerField(default=0)



class ResumeData(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    skills = models.TextField(blank=True, null=True)        # e.g., "Python, Java"
    projects = models.TextField(blank=True, null=True)      # e.g., "Resume Analyzer, Mock Interview Bot"
    experience = models.TextField(blank=True, null=True)    # e.g., "Intern at Google"
    education = models.TextField(blank=True, null=True)     # e.g., "B.Tech in CS"
    certifications = models.TextField(blank=True, null=True)
    internships = models.TextField(blank=True, null=True)
    achievements = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.user.username}'s Resume"

    




    


