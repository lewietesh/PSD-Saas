# accounts/management/commands/cleanup_sessions.py
from django.core.management.base import BaseCommand
from django.contrib.sessions.models import Session
from django.utils import timezone


class Command(BaseCommand):
    help = 'Delete all expired sessions from the database'

    def handle(self, *args, **options):
        # Delete expired sessions
        expired_count = Session.objects.filter(expire_date__lt=timezone.now()).count()
        Session.objects.filter(expire_date__lt=timezone.now()).delete()
        
        self.stdout.write(
            self.style.SUCCESS(f'Successfully deleted {expired_count} expired sessions')
        )
        
        # Show remaining active sessions
        active_count = Session.objects.count()
        self.stdout.write(
            self.style.SUCCESS(f'Active sessions remaining: {active_count}')
        )
