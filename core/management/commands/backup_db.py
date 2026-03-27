import datetime
import shutil
from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Create a timestamped backup of local sqlite database."

    def handle(self, *args, **options):
        db_path = settings.DATABASES["default"]["NAME"]
        if not str(db_path).endswith(".sqlite3"):
            self.stdout.write(self.style.WARNING("backup_db currently supports sqlite only."))
            return
        source = Path(db_path)
        if not source.exists():
            self.stdout.write(self.style.ERROR(f"Database not found: {source}"))
            return
        backup_dir = Path(settings.BASE_DIR) / "backups"
        backup_dir.mkdir(exist_ok=True)
        stamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        target = backup_dir / f"db_{stamp}.sqlite3"
        shutil.copy2(source, target)
        self.stdout.write(self.style.SUCCESS(f"Backup created: {target}"))
