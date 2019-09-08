# Take It Or Sleeve It

Take It Or Sleeve It is a website where users compare album covers.
Pairs of covers are presented side by side, and you pick your favourite!
Your choices then go towards a ranking of album art.

Choose wisely!



# Requirements

- Python3.5+
- Django 2.2
- [wptools](https://pypi.org/project/wptools/)





# Running it yourself

```
git clone git@github.com:keziah55/TakeItOrSleeveIt.git
cd TakeItOrSleeveIt
pip install -r requirements.txt
python manage.py migrate
python populateDatabase -cm
python manage.py runserver
```

Then, going to [http://127.0.0.1:8000/takeitorsleeveit/](http://127.0.0.1:8000/takeitorsleeveit/) will display the site.

