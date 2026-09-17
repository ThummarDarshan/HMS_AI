from django.core.management.base import BaseCommand
from ai_assistant.ingestion.pipeline import MedicationIngestionPipeline


class Command(BaseCommand):
    help = "Sync medication documentation from CDSCO, DailyMed, and OpenFDA providers"

    def add_arguments(self, parser):
        parser.add_argument("--drug", type=str, help="Specific drug name to ingest")

    def handle(self, *args, **options):
        drug = options.get("drug")
        pipeline = MedicationIngestionPipeline()

        if drug:
            self.stdout.write(f"Syncing medication '{drug}' from official providers...")
            count = pipeline.ingest_drug(drug)
            self.stdout.write(self.style.SUCCESS(f"Ingested {count} section chunks for '{drug}'."))
        else:
            self.stdout.write("Syncing all verified monographs from regulatory providers...")
            stats = pipeline.seed_all_verified_monographs()
            self.stdout.write(self.style.SUCCESS(f"Sync complete. Stats: {stats}"))
