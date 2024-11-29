# build_files.sh
pip install -r requirements.txt
python3.10 manage.py collectstatic --no-input --clear