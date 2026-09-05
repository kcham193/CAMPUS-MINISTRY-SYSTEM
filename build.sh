#!/usr/bin/env bash
set -o errexit

pip install -r requirements.txt

python manage.py collectstatic --no-input
python manage.py migrate --no-input

# One-time superuser bootstrap. Remove after first successful deploy.
if [[ -n "$DJANGO_SUPERUSER_PASSWORD" ]]; then
  python manage.py shell -c "
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'kasim@kunonu.org', '$DJANGO_SUPERUSER_PASSWORD')
    print('Superuser created.')
else:
    print('Superuser already exists, skipping.')
"
fi

# One-time student import. Remove after first successful run.
if [[ "$RUN_IMPORT" == "1" ]]; then
  python manage.py import_students
fi
