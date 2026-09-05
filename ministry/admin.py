from django.contrib import admin
from .models import Student, Event, University, Category, MinistryGoal


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['slug', 'target_count', 'current_count', 'progress_percent']
    readonly_fields = ['current_count', 'progress_percent']

    def current_count(self, obj): return obj.current_count
    def progress_percent(self, obj): return f"{obj.progress_percent}%"


@admin.register(University)
class UniversityAdmin(admin.ModelAdmin):
    list_display = ['name', 'abbreviation', 'type', 'is_reached', 'student_count']
    list_filter = ['type', 'is_reached']
    search_fields = ['name', 'abbreviation']


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'email', 'university', 'category_list', 'year_of_study', 'is_active', 'date_joined']
    list_filter = ['is_active', 'categories', 'university', 'year_of_study']
    search_fields = ['first_name', 'last_name', 'email']
    date_hierarchy = 'date_joined'
    filter_horizontal = ['categories']

    def category_list(self, obj):
        return ', '.join(c.name for c in obj.categories.all()) or '—'
    category_list.short_description = 'Categories'


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ['title', 'event_type', 'event_date', 'location', 'attended_students', 'is_completed']
    list_filter = ['event_type', 'is_completed']
    date_hierarchy = 'event_date'


@admin.register(MinistryGoal)
class MinistryGoalAdmin(admin.ModelAdmin):
    list_display = ['title', 'target_students', 'target_date', 'is_active']
