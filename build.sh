#!/usr/bin/env bash
set -o errexit

pip install -r requirements.txt

python manage.py collectstatic --no-input
python manage.py migrate

# Re-create the 5 default portfolio projects if they don't already exist
# (safe to run every deploy — it never duplicates or overwrites existing data).
python manage.py seed_site
