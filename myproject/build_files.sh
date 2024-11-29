# build_files.sh
pip install -r requirements.txt
python3.x manage.py collectstatic --no-input --clear