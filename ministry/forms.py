from django import forms
from .models import Student, Event, Attendance, University, Category


class StudentForm(forms.ModelForm):
    MAX_CATEGORIES = 2

    class Meta:
        model = Student
        fields = [
            'first_name', 'last_name', 'email', 'phone',
            'university', 'categories', 'year_of_study', 'course_of_study',
            'date_joined', 'is_active', 'photo', 'notes'
        ]
        widgets = {
            'date_joined': forms.DateInput(attrs={'type': 'date'}),
            'notes': forms.Textarea(attrs={'rows': 3}),
            'first_name': forms.TextInput(attrs={'placeholder': 'First name'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Last name'}),
            'email': forms.EmailInput(attrs={'placeholder': 'student@university.ac.tz'}),
            'phone': forms.TextInput(attrs={'placeholder': '+255 7XX XXX XXX'}),
            'course_of_study': forms.TextInput(attrs={'placeholder': 'e.g. Bachelor of Commerce'}),
            'categories': forms.CheckboxSelectMultiple(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field_name == 'categories':
                continue
            existing = field.widget.attrs.get('class', '')
            field.widget.attrs['class'] = f'{existing} form-control ci-input'.strip()
        self.fields['is_active'].widget.attrs['class'] = 'form-check-input'
        self.fields['photo'].widget.attrs['class'] = 'form-control ci-input'
        self.fields['categories'].help_text = f'Select up to {self.MAX_CATEGORIES} categories.'

    def clean_categories(self):
        categories = self.cleaned_data.get('categories')
        if categories and len(categories) > self.MAX_CATEGORIES:
            raise forms.ValidationError(
                f'A student can belong to a maximum of {self.MAX_CATEGORIES} categories.'
            )
        return categories


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = [
            'title', 'description', 'event_type', 'event_date',
            'event_time', 'location', 'expected_attendance', 'is_completed'
        ]
        widgets = {
            'event_date': forms.DateInput(attrs={'type': 'date'}),
            'event_time': forms.TimeInput(attrs={'type': 'time'}),
            'description': forms.Textarea(attrs={'rows': 3}),
            'title': forms.TextInput(attrs={'placeholder': 'Event title'}),
            'location': forms.TextInput(attrs={'placeholder': 'Venue / Location'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            existing = field.widget.attrs.get('class', '')
            field.widget.attrs['class'] = f'{existing} form-control ci-input'.strip()
        self.fields['is_completed'].widget.attrs['class'] = 'form-check-input'


class UniversityForm(forms.ModelForm):
    class Meta:
        model = University
        fields = ['name', 'abbreviation', 'type', 'latitude', 'longitude', 'address', 'is_reached', 'notes']
        widgets = {
            'notes': forms.Textarea(attrs={'rows': 2}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            existing = field.widget.attrs.get('class', '')
            field.widget.attrs['class'] = f'{existing} form-control ci-input'.strip()
        self.fields['is_reached'].widget.attrs['class'] = 'form-check-input'


class AttendanceBulkForm(forms.Form):
    """Used to mark attendance for all students at once for an event"""

    def __init__(self, *args, students=None, **kwargs):
        super().__init__(*args, **kwargs)
        if students:
            for student in students:
                self.fields[f'attended_{student.id}'] = forms.BooleanField(
                    required=False,
                    label=student.full_name,
                    widget=forms.CheckboxInput(attrs={'class': 'form-check-input attended-check'})
                )
                self.fields[f'participated_{student.id}'] = forms.BooleanField(
                    required=False,
                    label='Participated',
                    widget=forms.CheckboxInput(attrs={'class': 'form-check-input participated-check'})
                )
                self.fields[f'notes_{student.id}'] = forms.CharField(
                    required=False,
                    widget=forms.TextInput(attrs={
                        'class': 'form-control ci-input form-control-sm',
                        'placeholder': 'Notes...'
                    })
                )
