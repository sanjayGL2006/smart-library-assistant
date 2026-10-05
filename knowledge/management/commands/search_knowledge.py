from django.core.management.base import BaseCommand

from knowledge.services.search import semantic_search

class Command(BaseCommand):
    help = "Search the OLMS AI knowledge base."

    def add_arguments(self, parser):
        parser.add_argument(
            "query",
            type=str
        )

        parser.add_argument(
            "--limit",
            type=int,
            default=5
        )

    def handle(self, *args, **options):
        query = options["query"]
        limit = options["limit"]

        self.stdout.write(
            f"\nSearching knowledge base for:\n"
            f'"{query}"\n'
        )

        results = semantic_search(
            query,
            limit=limit
        )

        if not results:
            self.stdout.write(
                self.style.WARNING(
                    "\nNo relevant knowledge found."
                )
            )
            return

        self.stdout.write(
            f"\nFound {len(results)} results:\n"
        )

        for index, result in enumerate(results, start=1):
            metadata = result["metadata"]

            self.stdout.write(
                "\n"
                + "=" * 70
            )

            self.stdout.write(
                f"\n#{index}"
            )

            self.stdout.write(
                f"\nFile: {metadata.get('filename')}"
            )

            self.stdout.write(
                f"\nSubject: {metadata.get('subject')}"
            )

            self.stdout.write(
                f"\nTopic: {metadata.get('topic')}"
            )

            self.stdout.write(
                f"\nDistance: {result['distance']}"
            )

            self.stdout.write(
                "\n\n"
                + result["content"][:1000]
            )
