from django.core.management.base import BaseCommand
from datetime import datetime, timedelta
import random


class Command(BaseCommand):
    help = "Seed realistic demo data for the DSA Tracker (progress over time, etc.)"

    def handle(self, *args, **options):
        from tracker.models import DSAProblem  # import inside handle

        # 🧹 Clear old data
        DSAProblem.objects.all().delete()
        self.stdout.write("🧹 Old DSA problems cleared...")

        topics = [t[0] for t in DSAProblem.TOPICS]
        statuses = ["Solved", "Pending"]

        base_date = datetime(2025, 9, 1)
        today = datetime(2025, 10, 30)

        total_days = (today - base_date).days
        total_problems = 30

        for i in range(total_problems):
            topic = random.choice(topics)

            # Bias: more recent problems likely to be "Solved"
            days_offset = random.randint(0, total_days)
            problem_date = base_date + timedelta(days=days_offset)

            # 70% chance of being solved if it's within last 15 days
            if (today - problem_date).days <= 15:
                status = random.choices(["Solved", "Pending"], [0.8, 0.2])[0]
            else:
                status = random.choices(["Solved", "Pending"], [0.5, 0.5])[0]

            date_solved = problem_date if status == "Solved" else None

            DSAProblem.objects.create(
                title=f"DSA Problem {i + 1}",
                topic=topic,
                status=status,
                date_solved=date_solved,
            )

        self.stdout.write(self.style.SUCCESS("✅ 30 DSA problems seeded successfully with realistic progress data!"))
        self.stdout.write("📈 Check your dashboard — 'Progress Over Time' should now show upward trends.")
