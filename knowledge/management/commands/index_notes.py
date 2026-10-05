from django.core.management.base import BaseCommand
from knowledge.services.indexer import index_all_notes

NOTES_DIR = r"C:\Users\Sanjay G L\Downloads\library\all notes"

class Command(BaseCommand):
    help = 'Scans and indexes all notes into the knowledge engine.'

    def handle(self, *args, **kwargs):
        self.stdout.write("+--------------------------------------+")
        self.stdout.write("|       OLMS AI KNOWLEDGE ENGINE       |")
        self.stdout.write("+--------------------------------------+\n")
        self.stdout.write("Knowledge directory:")
        self.stdout.write("all notes/\n")
        self.stdout.write("Scanning...\n")
        
        stats = index_all_notes(NOTES_DIR)
        
        self.stdout.write(f"Files found             : {stats['files_found']}")
        self.stdout.write(f"New documents           : {stats['new']}")
        self.stdout.write(f"Already indexed         : {stats['already_indexed']}")
        self.stdout.write(f"Modified                : {stats['modified']}")
        self.stdout.write(f"Unsupported             : {stats['unsupported']}\n")
        
        self.stdout.write(f"Documents processed     : {stats['processed']}")
        self.stdout.write(f"Chunks created          : {stats['chunks_created']}")
        self.stdout.write(f"Failed                  : {stats['failed']}\n")
        
        if stats['processed'] > 0 or stats['modified'] > 0:
            self.stdout.write(self.style.SUCCESS("✓ Knowledge index updated."))
        else:
            self.stdout.write(self.style.SUCCESS("✓ Knowledge index is already up to date."))
