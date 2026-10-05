from django.core.management.base import BaseCommand

from knowledge.models import KnowledgeDocument
from knowledge.services.vector_indexer import index_document
from knowledge.services.vector_store import get_collection_count

class Command(BaseCommand):
    help = "Generate embeddings and build the OLMS AI vector index."

    def handle(self, *args, **options):
        self.stdout.write(
            self.style.SUCCESS(
                "\nOLMS AI \u2014 VECTOR INDEXER\n"
            )
        )

        documents = KnowledgeDocument.objects.filter(
            indexed=True
        )

        total_documents = documents.count()
        total_chunks = 0

        self.stdout.write(
            f"Documents available: {total_documents}\n"
        )

        for document in documents:
            try:
                count = index_document(document)
                total_chunks += count
                self.stdout.write(
                    self.style.SUCCESS(
                        f"\u2713 {document.filename} "
                        f"-> {count} chunks"
                    )
                )
            except Exception as exc:
                self.stdout.write(
                    self.style.ERROR(
                        f"\u2717 {document.filename}: {exc}"
                    )
                )

        vector_count = get_collection_count()

        self.stdout.write("\n")
        self.stdout.write(
            self.style.SUCCESS(
                "Vector indexing completed."
            )
        )

        self.stdout.write(
            f"Documents processed: {total_documents}"
        )

        self.stdout.write(
            f"\nChunks indexed: {total_chunks}"
        )

        self.stdout.write(
            f"\nVectors in database: {vector_count}"
        )
