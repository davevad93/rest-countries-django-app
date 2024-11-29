# build_files.sh
pip install -r requirements.txt
py manage.py collectstatic --no-input --clear