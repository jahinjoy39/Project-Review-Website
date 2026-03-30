from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from projects.models import Project, Rating

User = get_user_model()

class Command(BaseCommand):
    help = 'Seed demo data'

    def handle(self, *args, **kwargs):
        presenter, _ = User.objects.get_or_create(username='presenter1', defaults={'email': 'presenter@example.com', 'role': 'presenter'})
        presenter.set_password('password123')
        presenter.save()
        reviewer, _ = User.objects.get_or_create(username='reviewer1', defaults={'email': 'reviewer@example.com', 'role': 'reviewer'})
        reviewer.set_password('password123')
        reviewer.save()

        project, _ = Project.objects.get_or_create(
            creator=presenter,
            title='AI Project Review Demo',
            defaults={'description': 'Demo project for the course.', 'category': 'AI', 'video_url': 'https://example.com/demo'}
        )
        Rating.objects.get_or_create(reviewer=reviewer, project=project, defaults={'score': 5, 'clarity': 5, 'design': 4, 'research_depth': 5, 'technical_skill': 4, 'presentation_impact': 5})
        self.stdout.write(self.style.SUCCESS('Demo data inserted.'))
