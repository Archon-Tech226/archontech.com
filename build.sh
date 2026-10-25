#!/usr/bin/env bash
set -o errexit

pip install -r requirements.txt

python manage.py collectstatic --no-input
python manage.py migrate

# Re-create the 5 default portfolio projects if they don't already exist
# (safe to run every deploy — it never duplicates or overwrites existing data).
python manage.py seed_site

# Create the admin account once, from environment variables (skipped if no password is set
# or if the user already exists).
if [ -n "$DJANGO_SUPERUSER_PASSWORD" ]; then
  python manage.py createsuperuser --noinput || echo "Admin step skipped: the user already exists, or DJANGO_SUPERUSER_EMAIL is not a valid address."
fi
