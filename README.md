# 🎓 Campus Impact — Ministry Management System
### TAG SCT Changanyikeni · Dar es Salaam

> **3,000 University Students Impact in 2 Years**
> Career · Faith · Teaching · Purpose

---

## 🚀 Quick Setup (5 Minutes)

### 1. Prerequisites
Make sure you have **Python 3.10+** installed.

```bash
python --version   # Should be 3.10 or higher
```

### 2. Create Virtual Environment & Install
```bash
# Navigate to project folder
cd campus_impact_project

# Create virtual environment
python -m venv venv

# Activate it
# On Windows:
venv\Scripts\activate
# On Mac/Linux:
source venv/bin/activate

# Install all dependencies
pip install -r requirements.txt
```

### 3. Setup Database & Initial Data
```bash
# Create database tables
python manage.py migrate

# Seed initial data (categories + 16 Dar es Salaam universities)
python manage.py seed_data

# Optional: Add demo students and events to see the system in action
python manage.py seed_data --demo
```

### 4. Run the Server
```bash
python manage.py runserver
```

### 5. Open in Browser
```
http://127.0.0.1:8000/
```

**Login credentials:**
- Username: `admin`
- Password: `campusimpact2024`

---

## 📋 System Features

### 👥 Student Management
- Full CRUD (Add, View, Edit, Delete students)
- Track name, email, phone, university, category, year of study, course
- Search and filter by category, university, or status
- Attendance rate per student automatically calculated

### 📅 Event Management
- Create events: Fellowship, Seminar, Outreach, Worship Night, Conference, Mentorship
- Mark attendance for all students with one form
- Track attended vs participated separately
- Event completion status

### 🗺️ University Coverage Map
- Interactive dark Leaflet.js map of Dar es Salaam
- 16 pre-loaded universities and colleges
- Green markers = reached, Red markers = not yet reached
- Click any marker for institution details and student count
- Coverage percentage tracking

### 📊 Dashboard
- Live progress ring showing overall 3,000 goal progress
- 6-month student growth trend chart
- Category vs target bar chart
- Recent events feed
- Top active students by attendance
- Animated counters and progress bars

### 📁 Reports (PDF Download)
- Professional PDF with ministry letterhead
- Executive summary with all key metrics
- Visual progress bars per category
- Full student registry table
- Events summary table
- Generated with ReportLab — no external services needed

---

## 🎯 Ministry Categories & Targets

| Category | Target | Description |
|----------|--------|-------------|
| 🙏 Minister's Calling for Gospel | 50 | Future gospel ministers and church leaders |
| 🏛️ Political & Government Leaders | 100 | Faithful leaders in government and politics |
| 🎵 Worship & Praises | 300 | Worship team and music ministry members |
| 💼 Business and Investors | 200 | Entrepreneurs and Kingdom investors |
| 👷 Careers and Faithful Workers | 350 | Professionals excelling in their fields |

---

## 🏫 Pre-Loaded Universities (Dar es Salaam)

1. University of Dar es Salaam (UDSM)
2. Ardhi University (ARU)
3. Muhimbili University (MUHAS)
4. Institute of Finance Management (IFM)
5. College of Business Education (CBE)
6. DUCE - Dar es Salaam University College of Education
7. Dar es Salaam Institute of Technology (DIT)
8. Tanzania Institute of Accountancy (TIA)
9. Open University of Tanzania (OUT)
10. Mzumbe University DSM Campus
11. St. Augustine University DSM Campus
12. Hubert Kairuki Memorial University (HKMU)
13. International Medical & Technological University (IMTU)
14. St. Joseph University in Tanzania (SJUT)
15. UDSM Business School (UDBS)
16. Dar es Salaam Maritime Institute (DMI)

---

## 🛠️ Tech Stack

| Component | Technology |
|-----------|-----------|
| Backend | Django 4.2 |
| Database | SQLite3 (built-in) |
| PDF Reports | ReportLab |
| Maps | Leaflet.js + OpenStreetMap (free) |
| Charts | Chart.js |
| Icons | Bootstrap Icons |
| Fonts | Syne + DM Sans (Google Fonts) |

---

## 📂 Project Structure

```
campus_impact_project/
├── campus_impact/          # Django project settings
├── ministry/               # Main application
│   ├── models.py           # Database models
│   ├── views.py            # All views
│   ├── urls.py             # URL routing
│   ├── forms.py            # Form definitions
│   ├── pdf_report.py       # PDF generation
│   ├── management/
│   │   └── commands/
│   │       └── seed_data.py  # Initial data seeder
│   └── templates/          # All HTML templates
├── static/                 # Static files
├── manage.py
└── requirements.txt
```

---

## 🔒 Security Note

This system is configured for local/internal church use.
Before deploying to a public server:
1. Change `SECRET_KEY` in `settings.py`
2. Set `DEBUG = False`
3. Configure `ALLOWED_HOSTS` with your domain
4. Use a production database (PostgreSQL recommended)

---

*Built with ❤️ for TAG SCT Changanyikeni Campus Ministry*
