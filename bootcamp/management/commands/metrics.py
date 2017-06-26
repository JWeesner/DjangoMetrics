from django.core.management.base import BaseCommand
import argparse
from django.conf import settings
from django.core.management import call_command

class Command(BaseCommand):
    help = 'Enable or disable the tracking of Django metrics'

    def add_arguments(self, parser):
        parser = argparse.ArgumentParser(description="Parse bool")
        metric_parser = parser.add_mutually_exclusive_group(required=False)
        metric_parser.add_argument('--metrics', dest='metrics', action='store_true')
        metric_parser.add_argument('--no-metrics', dest='metrics', action='store_false')
        parser.set_defaults(metrics=False)

    def handle(self, *args, **options):
        settings.METRICS = True
        call_command('runserver', *args, **options)

