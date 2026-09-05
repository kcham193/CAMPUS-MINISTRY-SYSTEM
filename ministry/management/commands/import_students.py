"""
Bulk-import students from data/students.xlsx (KoboToolbox export).

Idempotent: re-runs skip rows whose (generated or real) email already exists.
"""
from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand
from django.db import transaction

from ministry.models import Category, Student, University


UNIVERSITY_ALIASES = {
    'eastc': ('EASTC', 'Eastern Africa Statistical Training Centre', -6.7726, 39.2410),
    'wi': ('WI', 'Water Institute', -6.7794, 39.2183),
    'maji': ('WI', 'Water Institute', -6.7794, 39.2183),
    'maji collage': ('WI', 'Water Institute', -6.7794, 39.2183),
    'water institute': ('WI', 'Water Institute', -6.7794, 39.2183),
    'aru': ('ARU', 'Ardhi University', -6.7735, 39.2320),
    'dmi': ('DMI', 'Dar es Salaam Maritime Institute', -6.8199, 39.2916),
    'udsm': ('UDSM', 'University of Dar es Salaam', -6.7756, 39.2076),
    'tanzania institute of accountancy (tia)': ('TIA', 'Tanzania Institute of Accountancy', -6.8163, 39.2803),
    'tia': ('TIA', 'Tanzania Institute of Accountancy', -6.8163, 39.2803),
}

# xlsx column indexes (0-based) — matches the KoboToolbox export layout.
COL_NAME = 5
COL_UNIVERSITY = 7
COL_YEAR = 8
COL_PHONE = 10
COL_EMAIL = 11
CAT_COLS = {
    13: 'gospel',
    14: 'business',
    15: 'political',
    16: 'career',
    17: 'worship',
}


class Command(BaseCommand):
    help = 'Import students from data/students.xlsx (KoboToolbox export).'

    def add_arguments(self, parser):
        parser.add_argument('--dry-run', action='store_true', help='Parse and validate without saving.')
        parser.add_argument('--path', default=None, help='Override xlsx path.')

    def handle(self, *args, **opts):
        try:
            import openpyxl
        except ImportError:
            self.stderr.write('openpyxl not installed. Add to requirements.txt and pip install.')
            return

        xlsx_path = Path(opts['path']) if opts['path'] else Path(settings.BASE_DIR) / 'data' / 'students.xlsx'
        if not xlsx_path.exists():
            self.stderr.write(f'File not found: {xlsx_path}')
            return

        wb = openpyxl.load_workbook(xlsx_path, data_only=True)
        ws = wb.active

        categories_by_slug = {c.slug: c for c in Category.objects.all()}
        for slug, _label in Category.CATEGORY_CHOICES:
            if slug not in categories_by_slug:
                categories_by_slug[slug] = Category.objects.create(slug=slug)

        universities_cache = {}
        created_count = 0
        skipped_count = 0
        errors = []

        for row_num, row in enumerate(ws.iter_rows(min_row=2, values_only=True), start=2):
            raw_name = row[COL_NAME]
            if not raw_name:
                continue

            first_name, last_name = self._split_name(str(raw_name))
            phone = self._normalize_phone(row[COL_PHONE])
            email = self._email_or_placeholder(row[COL_EMAIL], first_name, last_name, phone)
            year = self._parse_year(row[COL_YEAR])
            university = self._resolve_university(row[COL_UNIVERSITY], universities_cache)
            category_slugs = [slug for col_idx, slug in CAT_COLS.items() if row[col_idx] == 1]

            if Student.objects.filter(email=email).exists():
                skipped_count += 1
                continue

            if opts['dry_run']:
                self.stdout.write(
                    f'[dry] row {row_num}: {first_name} {last_name} | {email} | '
                    f'{university} | year={year} | cats={category_slugs}'
                )
                created_count += 1
                continue

            try:
                with transaction.atomic():
                    student = Student.objects.create(
                        first_name=first_name,
                        last_name=last_name,
                        email=email,
                        phone=phone,
                        university=university,
                        year_of_study=year,
                    )
                    student.categories.set(
                        [categories_by_slug[s] for s in category_slugs if s in categories_by_slug]
                    )
                created_count += 1
            except Exception as e:
                errors.append(f'row {row_num} ({first_name} {last_name}): {e}')

        self.stdout.write(self.style.SUCCESS(
            f'Import complete. Created: {created_count}, Skipped (already exist): {skipped_count}'
        ))
        if errors:
            self.stdout.write(self.style.WARNING(f'{len(errors)} errors:'))
            for err in errors:
                self.stdout.write(f'  {err}')

    @staticmethod
    def _split_name(raw):
        parts = raw.strip().split()
        if len(parts) == 1:
            return parts[0].title(), ''
        return parts[0].title(), ' '.join(parts[1:]).title()

    @staticmethod
    def _normalize_phone(raw):
        if raw is None:
            return ''
        s = str(raw).strip().replace(' ', '')
        if s and not s.startswith('0') and not s.startswith('+'):
            s = '0' + s  # Tanzanian numbers exported as int lose the leading 0
        return s[:20]

    @staticmethod
    def _email_or_placeholder(raw, first, last, phone):
        if raw and '@' in str(raw):
            return str(raw).strip().lower()
        # Deterministic placeholder — same input yields same email, so re-runs dedupe.
        slug = f'{first}.{last}.{phone or "nophone"}'.lower().replace(' ', '')
        return f'{slug}@placeholder.local'

    @staticmethod
    def _parse_year(raw):
        try:
            y = int(raw)
            return y if 0 <= y <= 6 else 1
        except (TypeError, ValueError):
            return 1

    @staticmethod
    def _resolve_university(raw, cache):
        if not raw:
            return None
        key = str(raw).strip().lower()
        if key in cache:
            return cache[key]

        alias = UNIVERSITY_ALIASES.get(key)
        if alias:
            abbr, full_name, lat, lng = alias
            uni, _ = University.objects.get_or_create(
                abbreviation=abbr,
                defaults={'name': full_name, 'latitude': lat, 'longitude': lng},
            )
        else:
            # Unknown school — create a stub with 0,0 coords for later cleanup.
            abbr = str(raw).strip().upper()[:30]
            uni, _ = University.objects.get_or_create(
                abbreviation=abbr,
                defaults={'name': str(raw).strip(), 'latitude': 0.0, 'longitude': 0.0},
            )
        cache[key] = uni
        return uni
