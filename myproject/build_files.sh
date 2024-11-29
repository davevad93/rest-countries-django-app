# build_files.sh
python -m pip install -r requirements.txt
python manage.py collectstatic --noinput