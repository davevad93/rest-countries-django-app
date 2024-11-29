# build_files.sh
pip install -r requirements.txt
python manage.py collectstatic --no-input --clear