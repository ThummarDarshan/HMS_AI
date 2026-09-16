from django.core.management.base import BaseCommand
from ai_assistant.ingestion.pipeline import MedicationIngestionPipeline
from ai_assistant.models import MedicationDocument


class Command(BaseCommand):
    help = "Seed verified authoritative CDSCO and DailyMed medication documentation"

    def handle(self, *args, **options):
        self.stdout.write(self.style.NOTICE("Seeding verified medication monographs into database..."))
        pipeline = MedicationIngestionPipeline()
        stats = pipeline.seed_all_verified_monographs()

        total = MedicationDocument.objects.count()
        self.stdout.write(
            self.style.SUCCESS(
                f"Successfully seeded medication knowledge base! Stats: {stats}. Total documents in DB: {total}"
            )
        )
