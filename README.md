# Take It Or Sleeve It

Take It Or Sleeve It is a website where users compare album covers.
Pairs of covers are presented side by side, and you pick your favourite!
Your choices then go towards a ranking of album art.

Choose wisely!


# Requirements

- [Python3.5+](https://www.python.org/download/releases/3.0/)
- [Django 2.2](https://www.djangoproject.com/)
- [wptools](https://pypi.org/project/wptools/)


# Running it yourself

Download this repository...
```
git clone git@github.com:keziah55/TakeItOrSleeveIt.git
cd TakeItOrSleeveIt
```

Install the required Python packages with `pip` (or `pip3`)
```
pip install -r requirements.txt
```

Set up the database (make sure you have `albumratingsite/secret_settings.py`), where `python` is the python3 interpreter...
```
python manage.py migrate
```
...create the database...
```
python populateDatabase -cm
```
... then run it!
```
python manage.py runserver
```

Now, going to [http://127.0.0.1:8000/takeitorsleeveit/](http://127.0.0.1:8000/takeitorsleeveit/) will display the site.

You can fill the database with random test data with
```
python populateDatabase -t
```
See `python populateDatabase --help` for full list of args.
