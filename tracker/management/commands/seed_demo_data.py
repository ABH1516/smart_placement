from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta, datetime
import random

class Command(BaseCommand):
    help = "Seed demo data for Placement, DSA, and Aptitude trackers"

    def handle(self, *args, **options):
        # ✅ Import models inside handle() to avoid circular imports
        from tracker.models import Application, DSAProblem, AptitudeQuestion

        # Clear existing demo data
        Application.objects.all().delete()
        DSAProblem.objects.all().delete()
        AptitudeQuestion.objects.all().delete()

        self.stdout.write("🧹 Cleared old data...")

        # ------------------ Placement Tracker ------------------
        companies = ["Google", "Amazon", "TCS", "Infosys", "Wipro", "Accenture"]
        statuses = ["applied", "interviewed", "rejected", "selected"]
        base_date = datetime(2025, 9, 25)

        for i in range(10):
            Application.objects.create(
                company_name=random.choice(companies),
                job_title=f"Software Engineer {i+1}",
                application_date=base_date + timedelta(days=i),
                status=random.choice(statuses),
                notes=f"Demo application {i+1}"
            )

        self.stdout.write("✅ Placement tracker seeded (10 rows).")

        # ------------------ DSA Tracker ------------------
        topics = [t[0] for t in DSAProblem.TOPICS]
        dsa_statuses = ["Solved", "Pending"]

        for i in range(10):
            solved_date = base_date + timedelta(days=i)
            DSAProblem.objects.create(
                title=f"Problem {i+1}",
                topic=random.choice(topics),
                status=random.choice(dsa_statuses),
                date_solved=solved_date
            )

        self.stdout.write("✅ DSA tracker seeded (10 rows).")

        # ------------------ Aptitude Tracker ------------------
        apt_topics = [t[0] for t in AptitudeQuestion.TOPICS]
        apt_statuses = ["Solved", "Unsolved"]

        for i in range(10):
            created_date = base_date + timedelta(days=i)
            status = random.choice(apt_statuses)
            question = AptitudeQuestion.objects.create(
                title=f"Aptitude Question {i+1}",
                topic=random.choice(apt_topics),
                status=status,
                score=random.randint(40, 100),
                solution="Demo solution" if status == "Solved" else ""
            )
            # Spread out creation dates
            question.created_at = created_date
            question.save(update_fields=["created_at"])

        self.stdout.write("✅ Aptitude tracker seeded (10 rows).")

        self.stdout.write(self.style.SUCCESS("🎉 Demo data seeded successfully!"))
