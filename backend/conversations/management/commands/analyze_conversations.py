from django.core.management.base import BaseCommand
from conversations.celery import analyze_new_conversations


class Command(BaseCommand):
    help = 'Analyzes all conversations that do not have an analysis yet'

    def add_arguments(self, parser):
        parser.add_argument(
            '--async',
            action='store_true',
            help='Run analysis asynchronously using Celery',
        )

    def handle(self, *args, **options):
        if options['async']:
            self.stdout.write('Starting conversation analysis asynchronously...')
            task = analyze_new_conversations.delay()
            self.stdout.write(
                self.style.SUCCESS(f'Task queued with ID: {task.id}')
            )
        else:
            self.stdout.write('Starting conversation analysis...')
            try:
                count = analyze_new_conversations()
                self.stdout.write(
                    self.style.SUCCESS(f'Successfully analyzed {count} conversations')
                )
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f'Error during analysis: {str(e)}')
                )

