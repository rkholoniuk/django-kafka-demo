from django.core.management.base import BaseCommand
from datasender.queue_listener import DataCreatedListener


class Command(BaseCommand):
    help = 'Launches Listener for data_created message : Kafka'

    def handle(self, *args, **options):
        td = DataCreatedListener()
        td.start()
        self.stdout.write("Started Consumer Thread")
