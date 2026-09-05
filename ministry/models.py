
from django.db import models
from django.utils import timezone


class Category(models.Model):
    CATEGORY_CHOICES = [
        ('gospel', "Minister's Calling for Gospel"),
        ('political', 'Political & Government Faithful Leaders'),
        ('worship', 'Worship & Praises'),
        ('business', 'Business and Investors'),
        ('career', 'Careers and Faithful Workers'),
    ]
    COLOR_MAP = {
        'gospel': '#c49a1a',
        'political': '#8b1a1a',
        'worship': '#2d6e2d',
        'business': '#1a3a8f',
        'career': '#6b2d8b',
    }
    ICON_MAP = {
        'gospel': 'bi-book-fill',
        'political': 'bi-building-fill',
        'worship': 'bi-music-note-beamed',
        'business': 'bi-briefcase-fill',
        'career': 'bi-person-workspace',
    }

    slug = models.CharField(max_length=20, choices=CATEGORY_CHOICES, unique=True)
    target_count = models.IntegerField(default=0)
    description = models.TextField(blank=True)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.get_slug_display()

    @property
    def name(self):
        return self.get_slug_display()

    @property
    def color(self):
        return self.COLOR_MAP.get(self.slug, '#888888')

    @property
    def icon(self):
        return self.ICON_MAP.get(self.slug, 'bi-person')

    @property
    def current_count(self):
        return self.students.filter(is_active=True).count()

    @property
    def progress_percent(self):
        if self.target_count == 0:
            return 0
        return min(round((self.current_count / self.target_count) * 100, 1), 100)


class University(models.Model):
    TYPE_CHOICES = [
        ('university', 'University'),
        ('college', 'College'),
        ('institute', 'Institute'),
        ('polytechnic', 'Polytechnic'),
    ]

    name = models.CharField(max_length=200)
    abbreviation = models.CharField(max_length=30, blank=True)
    type = models.CharField(max_length=20, choices=TYPE_CHOICES, default='university')
    latitude = models.FloatField()
    longitude = models.FloatField()
    address = models.CharField(max_length=300, blank=True)
    is_reached = models.BooleanField(default=False)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Universities'
        ordering = ['name']

    def __str__(self):
        return self.abbreviation if self.abbreviation else self.name

    @property
    def student_count(self):
        return self.student_set.filter(is_active=True).count()


class Student(models.Model):
    YEAR_CHOICES = [(i, f'Year {i}') for i in range(1, 7)] + [(0, 'Graduate/Alumni')]

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, blank=True)
    university = models.ForeignKey(University, on_delete=models.SET_NULL, null=True, blank=True)
    categories = models.ManyToManyField(Category, blank=True, related_name='students')
    year_of_study = models.IntegerField(choices=YEAR_CHOICES, default=1)
    course_of_study = models.CharField(max_length=200, blank=True)
    date_joined = models.DateField(default=timezone.now)
    is_active = models.BooleanField(default=True)
    photo = models.ImageField(upload_to='students/', blank=True, null=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-date_joined', 'last_name']

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    @property
    def initials(self):
        return f"{self.first_name[0]}{self.last_name[0]}".upper()

    @property
    def primary_category(self):
        return self.categories.first()


class Event(models.Model):
    TYPE_CHOICES = [
        ('fellowship', 'Fellowship Meeting'),
        ('seminar', 'Seminar / Training'),
        ('outreach', 'Outreach / Evangelism'),
        ('worship', 'Worship Night'),
        ('conference', 'Conference'),
        ('sports', 'Sports & Recreation'),
        ('mentorship', 'Mentorship Session'),
        ('other', 'Other'),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    event_type = models.CharField(max_length=20, choices=TYPE_CHOICES, default='fellowship')
    event_date = models.DateField()
    event_time = models.TimeField(null=True, blank=True)
    location = models.CharField(max_length=300)
    attended_students = models.IntegerField(default=0)
    is_completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-event_date']

    def __str__(self):
        return f"{self.title} ({self.event_date})"


class MinistryGoal(models.Model):
    """Tracks the overall campaign goal milestones"""
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    target_students = models.IntegerField(default=3000)
    target_date = models.DateField()
    start_date = models.DateField(default=timezone.now)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title

    @property
    def current_students(self):
        return Student.objects.filter(is_active=True).count()

    @property
    def progress_percent(self):
        return min(round((self.current_students / self.target_students) * 100, 1), 100)

    @property
    def days_remaining(self):
        from datetime import date
        remaining = self.target_date - date.today()
        return remaining.days
