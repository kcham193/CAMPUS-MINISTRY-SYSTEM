from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.http import JsonResponse, HttpResponse
from datetime import timedelta, date
import json

from .models import Student, Event, University, Category, MinistryGoal
from .forms import StudentForm, EventForm, UniversityForm
from .permissions import admin_required


def get_dashboard_context():
    """Shared context for dashboard metrics"""
    total_students = Student.objects.filter(is_active=True).count()
    total_goal = 3000
    categories = Category.objects.all()
    universities_reached = University.objects.filter(is_reached=True).count()
    total_universities = University.objects.count()
    total_events = Event.objects.count()
    recent_events = Event.objects.order_by('-event_date')[:5]

    # Monthly growth (last 6 months)
    monthly_data = []
    monthly_labels = []
    for i in range(5, -1, -1):
        d = date.today().replace(day=1) - timedelta(days=i * 30)
        month_end = d.replace(day=28) + timedelta(days=4)
        month_end = month_end - timedelta(days=month_end.day)
        count = Student.objects.filter(
            is_active=True,
            date_joined__lte=month_end
        ).count()
        monthly_data.append(count)
        monthly_labels.append(d.strftime('%b %Y'))

    # Category data for chart
    category_data = []
    for cat in categories:
        category_data.append({
            'name': cat.name,
            'current': cat.current_count,
            'target': cat.target_count,
            'color': cat.color,
            'slug': cat.slug,
            'icon': cat.icon,
            'percent': cat.progress_percent,
        })

    return {
        'total_students': total_students,
        'total_goal': total_goal,
        'overall_progress': min(round((total_students / total_goal) * 100, 1), 100),
        'students_remaining': max(total_goal - total_students, 0),
        'categories': categories,
        'category_data_json': json.dumps(category_data),
        'universities_reached': universities_reached,
        'total_universities': total_universities,
        'total_events': total_events,
        'recent_events': recent_events,
        'monthly_labels': json.dumps(monthly_labels),
        'monthly_data': json.dumps(monthly_data),
    }


@login_required
def dashboard(request):
    ctx = get_dashboard_context()
    ctx['latest_students'] = Student.objects.filter(is_active=True).order_by('-date_joined')[:6]
    return render(request, 'ministry/dashboard.html', ctx)


# ─── STUDENTS ────────────────────────────────────────────────────────────────

@login_required
def student_list(request):
    q = request.GET.get('q', '')
    category_filter = request.GET.get('category', '')
    university_filter = request.GET.get('university', '')
    status_filter = request.GET.get('status', 'active')

    students = Student.objects.select_related('university').prefetch_related('categories').all()

    if q:
        students = students.filter(
            Q(first_name__icontains=q) | Q(last_name__icontains=q) |
            Q(email__icontains=q) | Q(course_of_study__icontains=q)
        )
    if category_filter:
        students = students.filter(categories__slug=category_filter).distinct()
    if university_filter:
        students = students.filter(university_id=university_filter)
    if status_filter == 'active':
        students = students.filter(is_active=True)
    elif status_filter == 'inactive':
        students = students.filter(is_active=False)

    return render(request, 'ministry/students/list.html', {
        'students': students,
        'categories': Category.objects.all(),
        'universities': University.objects.all(),
        'q': q,
        'category_filter': category_filter,
        'university_filter': university_filter,
        'status_filter': status_filter,
        'total_count': students.count(),
    })


@login_required
def student_detail(request, pk):
    student = get_object_or_404(Student, pk=pk)
    return render(request, 'ministry/students/detail.html', {
        'student': student,
    })


@admin_required
def student_create(request):
    if request.method == 'POST':
        form = StudentForm(request.POST, request.FILES)
        if form.is_valid():
            student = form.save()
            # Mark university as reached
            if student.university:
                student.university.is_reached = True
                student.university.save()
            messages.success(request, f'✓ {student.full_name} has been added successfully!')
            return redirect('student_list')
    else:
        form = StudentForm()
    return render(request, 'ministry/students/form.html', {'form': form, 'title': 'Add New Student'})


@admin_required
def student_edit(request, pk):
    student = get_object_or_404(Student, pk=pk)
    if request.method == 'POST':
        form = StudentForm(request.POST, request.FILES, instance=student)
        if form.is_valid():
            form.save()
            messages.success(request, f'✓ {student.full_name} updated successfully!')
            return redirect('student_detail', pk=pk)
    else:
        form = StudentForm(instance=student)
    return render(request, 'ministry/students/form.html', {
        'form': form, 'student': student,
        'title': f'Edit — {student.full_name}'
    })


@admin_required
def student_delete(request, pk):
    student = get_object_or_404(Student, pk=pk)
    if request.method == 'POST':
        name = student.full_name
        student.delete()
        messages.success(request, f'Student {name} has been removed.')
        return redirect('student_list')
    return render(request, 'ministry/students/confirm_delete.html', {'student': student})


# ─── EVENTS ──────────────────────────────────────────────────────────────────

@login_required
def event_list(request):
    events = Event.objects.all()
    type_filter = request.GET.get('type', '')
    if type_filter:
        events = events.filter(event_type=type_filter)
    return render(request, 'ministry/events/list.html', {
        'events': events,
        'type_choices': Event.TYPE_CHOICES,
        'type_filter': type_filter,
    })


@login_required
def event_detail(request, pk):
    event = get_object_or_404(Event, pk=pk)
    return render(request, 'ministry/events/detail.html', {
        'event': event,
    })


@admin_required
def event_create(request):
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            event = form.save()
            messages.success(request, f'✓ Event "{event.title}" created!')
            return redirect('event_detail', pk=event.pk)
    else:
        form = EventForm()
    return render(request, 'ministry/events/form.html', {'form': form, 'title': 'Create Event'})


@admin_required
def event_edit(request, pk):
    event = get_object_or_404(Event, pk=pk)
    if request.method == 'POST':
        form = EventForm(request.POST, instance=event)
        if form.is_valid():
            form.save()
            messages.success(request, f'✓ Event updated!')
            return redirect('event_detail', pk=pk)
    else:
        form = EventForm(instance=event)
    return render(request, 'ministry/events/form.html', {
        'form': form, 'event': event, 'title': f'Edit — {event.title}'
    })


@admin_required
def event_delete(request, pk):
    event = get_object_or_404(Event, pk=pk)
    if request.method == 'POST':
        event.delete()
        messages.success(request, 'Event deleted.')
        return redirect('event_list')
    return render(request, 'ministry/events/confirm_delete.html', {'event': event})


# ─── UNIVERSITIES ────────────────────────────────────────────────────────────

@login_required
def university_map(request):
    universities = University.objects.all()
    uni_data = []
    for u in universities:
        uni_data.append({
            'id': u.id,
            'name': u.name,
            'abbreviation': u.abbreviation,
            'type': u.get_type_display(),
            'lat': u.latitude,
            'lng': u.longitude,
            'is_reached': u.is_reached,
            'student_count': u.student_count,
            'address': u.address,
        })
    return render(request, 'ministry/universities/map.html', {
        'universities': universities,
        'uni_data_json': json.dumps(uni_data),
        'reached_count': universities.filter(is_reached=True).count(),
        'total_count': universities.count(),
        'not_reached_count': universities.count() - universities.filter(is_reached=True).count(),
    })


@admin_required
def university_create(request):
    if request.method == 'POST':
        form = UniversityForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, '✓ University added!')
            return redirect('university_map')
    else:
        form = UniversityForm()
    return render(request, 'ministry/universities/form.html', {'form': form, 'title': 'Add University'})


@admin_required
def university_edit(request, pk):
    uni = get_object_or_404(University, pk=pk)
    if request.method == 'POST':
        form = UniversityForm(request.POST, instance=uni)
        if form.is_valid():
            form.save()
            messages.success(request, '✓ University updated!')
            return redirect('university_map')
    else:
        form = UniversityForm(instance=uni)
    return render(request, 'ministry/universities/form.html', {
        'form': form, 'university': uni, 'title': f'Edit — {uni.name}'
    })


@admin_required
def university_delete(request, pk):
    uni = get_object_or_404(University, pk=pk)
    if request.method == 'POST':
        uni.delete()
        messages.success(request, 'University removed.')
        return redirect('university_map')
    return render(request, 'ministry/universities/confirm_delete.html', {'university': uni})


# ─── REPORTS ─────────────────────────────────────────────────────────────────

@login_required
def reports_index(request):
    ctx = get_dashboard_context()
    ctx['universities'] = University.objects.all()
    ctx['total_events'] = Event.objects.count()
    ctx['completed_events'] = Event.objects.filter(is_completed=True).count()
    return render(request, 'ministry/reports/index.html', ctx)


@login_required
def report_pdf(request):
    from .pdf_report import generate_pdf_report
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="CampusImpact_Report_{date.today()}.pdf"'
    generate_pdf_report(response)
    return response


# ─── API / JSON ───────────────────────────────────────────────────────────────

@login_required
def api_dashboard_stats(request):
    """JSON endpoint for live dashboard stats"""
    categories = Category.objects.all()
    data = {
        'total_students': Student.objects.filter(is_active=True).count(),
        'categories': [
            {
                'name': c.name, 'current': c.current_count,
                'target': c.target_count, 'color': c.color
            } for c in categories
        ]
    }
    return JsonResponse(data)
