"""
Management command to seed initial data:
- All 5 categories with targets
- Universities/colleges in Dar es Salaam
- Sample students and events for demo
"""
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from ministry.models import Category, University, Student, Event, Attendance, MinistryGoal
from datetime import date, timedelta
import random


UNIVERSITIES = [
    {
        'name': 'University of Dar es Salaam',
        'abbreviation': 'UDSM',
        'type': 'university',
        'latitude': -6.7756,
        'longitude': 39.2076,
        'address': 'University Road, Mlimani, Dar es Salaam',
    },
    {
        'name': 'Ardhi University',
        'abbreviation': 'ARU',
        'type': 'university',
        'latitude': -6.7735,
        'longitude': 39.2320,
        'address': 'Observation Hill, Kinondoni, Dar es Salaam',
    },
    {
        'name': 'Muhimbili University of Health and Allied Sciences',
        'abbreviation': 'MUHAS',
        'type': 'university',
        'latitude': -6.8002,
        'longitude': 39.2218,
        'address': 'United Nations Road, Upanga, Dar es Salaam',
    },
    {
        'name': 'Institute of Finance Management',
        'abbreviation': 'IFM',
        'type': 'institute',
        'latitude': -6.8120,
        'longitude': 39.2750,
        'address': 'Shaaban Robert Street, Dar es Salaam',
    },
    {
        'name': 'College of Business Education',
        'abbreviation': 'CBE',
        'type': 'college',
        'latitude': -6.8150,
        'longitude': 39.2700,
        'address': 'Bibi Titi Mohamed Street, Dar es Salaam',
    },
    {
        'name': 'Dar es Salaam University College of Education',
        'abbreviation': 'DUCE',
        'type': 'college',
        'latitude': -6.8000,
        'longitude': 39.2400,
        'address': 'Chang\'ombe, Dar es Salaam',
    },
    {
        'name': 'Dar es Salaam Institute of Technology',
        'abbreviation': 'DIT',
        'type': 'institute',
        'latitude': -6.8124,
        'longitude': 39.2789,
        'address': 'Morogoro Road, Dar es Salaam',
    },
    {
        'name': 'Tanzania Institute of Accountancy',
        'abbreviation': 'TIA',
        'type': 'institute',
        'latitude': -6.8198,
        'longitude': 39.2839,
        'address': 'Shaaban Robert Street, Dar es Salaam',
    },
    {
        'name': 'Open University of Tanzania',
        'abbreviation': 'OUT',
        'type': 'university',
        'latitude': -6.8001,
        'longitude': 39.2445,
        'address': 'Kivukoni Road, Dar es Salaam',
    },
    {
        'name': 'Mzumbe University — Dar es Salaam Campus',
        'abbreviation': 'MU-DSM',
        'type': 'university',
        'latitude': -6.7859,
        'longitude': 39.2589,
        'address': 'Morogoro Road, Kinondoni, Dar es Salaam',
    },
    {
        'name': 'St. Augustine University of Tanzania — DSM Campus',
        'abbreviation': 'SAUT-DSM',
        'type': 'university',
        'latitude': -6.8169,
        'longitude': 39.2839,
        'address': 'Upanga, Dar es Salaam',
    },
    {
        'name': 'Hubert Kairuki Memorial University',
        'abbreviation': 'HKMU',
        'type': 'university',
        'latitude': -6.7900,
        'longitude': 39.2650,
        'address': '322 Regent Estate, Mikocheni, Dar es Salaam',
    },
    {
        'name': 'International Medical and Technological University',
        'abbreviation': 'IMTU',
        'type': 'university',
        'latitude': -6.8100,
        'longitude': 39.2650,
        'address': 'Tabata, Dar es Salaam',
    },
    {
        'name': 'St. Joseph University in Tanzania',
        'abbreviation': 'SJUT',
        'type': 'university',
        'latitude': -6.8000,
        'longitude': 39.2800,
        'address': 'Kinondoni, Dar es Salaam',
    },
    {
        'name': 'University of Dar es Salaam Business School',
        'abbreviation': 'UDBS',
        'type': 'college',
        'latitude': -6.8235,
        'longitude': 39.2800,
        'address': 'Mwenge, Dar es Salaam',
    },
    {
        'name': 'Dar es Salaam Maritime Institute',
        'abbreviation': 'DMI',
        'type': 'institute',
        'latitude': -6.8180,
        'longitude': 39.2900,
        'address': 'Magogoni Street, Dar es Salaam',
    },
]

SAMPLE_FIRST_NAMES = [
    'Emmanuel', 'Grace', 'Daniel', 'Faith', 'Joshua', 'Rehema', 'David',
    'Zawadi', 'Peter', 'Neema', 'John', 'Amina', 'Samuel', 'Salma', 'Joseph',
    'Tunaweza', 'Isaac', 'Upendo', 'Moses', 'Baraka', 'Nathan', 'Gloria',
    'Elijah', 'Mwajuma', 'Solomon', 'Aneth', 'Timothy', 'Josephine', 'Benjamin',
    'Christine', 'Michael', 'Prisca', 'George', 'Agnes', 'Robert', 'Veronica',
]

SAMPLE_LAST_NAMES = [
    'Mwanga', 'Kimaro', 'Nyambura', 'Msigwa', 'Kileo', 'Mollel', 'Massawe',
    'Mrema', 'Kibona', 'Swai', 'Lyimo', 'Minja', 'Urassa', 'Shao', 'Lema',
    'Mmbaga', 'Mosses', 'Munisi', 'Ngowi', 'Pallangyo', 'Marandu', 'Mtui',
    'Kimaro', 'Tesha', 'Mrema', 'Mwanga', 'Mbise', 'Maro', 'Laizer',
]

COURSES = [
    'Bachelor of Commerce', 'Bachelor of Science in Computer Science',
    'Bachelor of Laws (LLB)', 'Bachelor of Medicine', 'Bachelor of Education',
    'Bachelor of Engineering (Civil)', 'Bachelor of Business Administration',
    'Bachelor of Arts in Sociology', 'Bachelor of Science in Nursing',
    'Bachelor of Accountancy', 'Bachelor of Science in Information Technology',
    'Bachelor of Public Administration', 'Bachelor of Economics',
    'Bachelor of Science in Architecture', 'Bachelor of Arts in Mass Communication',
]


class Command(BaseCommand):
    help = 'Seed the database with initial Campus Impact data'

    def add_arguments(self, parser):
        parser.add_argument('--demo', action='store_true',
                            help='Also create demo students and events')

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('🌱 Seeding Campus Impact database...'))

        # ── Create superuser ──────────────────────────────────────────────
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser('admin', 'admin@tagsct.org', 'campusimpact2024')
            self.stdout.write('  ✓ Admin user created (username: admin, password: campusimpact2024)')

        # ── Create Categories ─────────────────────────────────────────────
        categories_data = [
            {'slug': 'gospel', 'target_count': 50,
             'description': "Students called to minister the Gospel and serve in church leadership"},
            {'slug': 'political', 'target_count': 100,
             'description': "Students aspiring to serve in government and political leadership with integrity"},
            {'slug': 'worship', 'target_count': 300,
             'description': "Students committed to worship, music, and praise ministry"},
            {'slug': 'business', 'target_count': 200,
             'description': "Students growing as business leaders and investors of Kingdom resources"},
            {'slug': 'career', 'target_count': 350,
             'description': "Students excelling in their careers as faithful workers in all sectors"},
        ]
        for cat_data in categories_data:
            cat, created = Category.objects.get_or_create(
                slug=cat_data['slug'],
                defaults=cat_data
            )
            if created:
                self.stdout.write(f'  ✓ Category: {cat.name}')

        # ── Create Universities ───────────────────────────────────────────
        for uni_data in UNIVERSITIES:
            uni, created = University.objects.get_or_create(
                abbreviation=uni_data['abbreviation'],
                defaults=uni_data
            )
            if created:
                self.stdout.write(f'  ✓ University: {uni.abbreviation}')

        # ── Ministry Goal ─────────────────────────────────────────────────
        goal, _ = MinistryGoal.objects.get_or_create(
            title='Campus Impact 2-Year Campaign',
            defaults={
                'description': '3,000 University Students Impact in 2 Years - Career, Faith, Teaching, Purpose',
                'target_students': 3000,
                'target_date': date.today() + timedelta(days=365 * 2),
                'start_date': date.today(),
            }
        )

        # ── Demo data ─────────────────────────────────────────────────────
        if options['demo']:
            self._create_demo_data()
            self.stdout.write(self.style.SUCCESS('  ✓ Demo data created!'))

        self.stdout.write(self.style.SUCCESS(
            '\n✅ Database seeded successfully!\n'
            '   → Run: python manage.py runserver\n'
            '   → Login at: http://127.0.0.1:8000/login/\n'
            '   → Username: admin  |  Password: campusimpact2024\n'
        ))

    def _create_demo_data(self):
        """Create sample students and events for demonstration"""
        categories = list(Category.objects.all())
        universities = list(University.objects.all())
        used_emails = set()

        students = []
        for i in range(45):
            fn = random.choice(SAMPLE_FIRST_NAMES)
            ln = random.choice(SAMPLE_LAST_NAMES)
            email_base = f"{fn.lower()}.{ln.lower()}{i}"
            email = f"{email_base}@student.ac.tz"
            if email in used_emails:
                continue
            used_emails.add(email)

            uni = random.choice(universities)
            num_cats = 1 if random.random() < 0.7 else 2
            assigned_cats = random.sample(categories, min(num_cats, len(categories)))
            days_ago = random.randint(0, 400)

            s = Student.objects.create(
                first_name=fn, last_name=ln, email=email,
                phone=f'+255 7{random.randint(10,99)} {random.randint(100,999)} {random.randint(100,999)}',
                university=uni,
                year_of_study=random.randint(1, 4),
                course_of_study=random.choice(COURSES),
                date_joined=date.today() - timedelta(days=days_ago),
                is_active=True,
            )
            s.categories.set(assigned_cats)
            uni.is_reached = True
            uni.save()
            students.append(s)

        # Create sample events
        event_titles = [
            ('Campus Fellowship — Changanyikeni', 'fellowship'),
            ('Career & Faith Seminar', 'seminar'),
            ('Worship Night — Power & Praise', 'worship'),
            ('Gospel Outreach — UDSM Campus', 'outreach'),
            ('Business & Kingdom Wealth Conference', 'conference'),
            ('Mentorship Session — Year 1 Students', 'mentorship'),
            ('Friday Fellowship Meeting', 'fellowship'),
            ('End of Semester Celebration', 'other'),
        ]

        past_events = []
        for i, (title, etype) in enumerate(event_titles):
            ev = Event.objects.create(
                title=title,
                event_type=etype,
                event_date=date.today() - timedelta(days=i * 20 + 5),
                location='TAG SCT Changanyikeni Church, Dar es Salaam',
                expected_attendance=random.randint(20, 60),
                is_completed=True,
                description=f'A powerful {etype} gathering for our campus students.',
            )
            # Create attendance records
            attending = random.sample(students, min(random.randint(15, 40), len(students)))
            for s in students:
                attended = s in attending
                Attendance.objects.create(
                    student=s, event=ev,
                    attended=attended,
                    participated=attended and random.random() > 0.4,
                )
            past_events.append(ev)

        # One upcoming event
        Event.objects.create(
            title='Campus Impact Grand Rally 2024',
            event_type='conference',
            event_date=date.today() + timedelta(days=14),
            location='TAG SCT Changanyikeni Church — Main Hall',
            expected_attendance=100,
            is_completed=False,
            description='Our flagship semester rally — all campus students invited!',
        )
