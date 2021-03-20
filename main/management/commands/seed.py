from django.core.management.base import BaseCommand
from django.core.files import File
from django.utils.timezone import now
from main import models
from random import choice
import datetime
import urllib
import os
import pandas as pd
import os, random
from pathlib import Path


class Command(BaseCommand):
    def handle(self, *args, **options):
        # assert(os.getenv('DJANGO_ENVIRONMENT') == "DEVELOPMENT")
        # self.clear_db()
        self.populate_db()

    def clear_db(self):
        models.Like.objects.all().delete()
        models.Comment.objects.all().delete()
        models.User.objects.all().delete()
        models.Language.objects.all().delete()
        models.City.objects.all().delete()

    # генерация дат рождения
    def get_random_birthday(self):
        start_date = datetime.date(1980, 1, 1)
        end_date = datetime.date(2002, 1, 1)

        time_between_dates = end_date - start_date
        days_between_dates = time_between_dates.days
        random_number_of_days = random.randrange(days_between_dates)

        random_date = start_date + datetime.timedelta(days=random_number_of_days)

        return random_date

    def populate_db(self):
        # admin
        # city_names = []
        # with open('main/management/commands/cities.txt', 'r', encoding='utf8') as file:
        #     city_names = file.readlines()
        
        # for city_name in city_names:
        #     city = models.City(name=city_name.strip())
        #     city.save()

        # для парсинга хобби
        with open('main/management/commands/interests.txt', 'r', encoding='utf8') as file:
            interests = file.readline().split(';')
            print(random.choice(interests))

        # для парсинга координат городов
        coordinates = {}
        with open('main/management/commands/coordinates.txt', 'r', encoding='utf8') as file:
            for line in file.readlines():
                cityID = line.split(':')[0]
                cityCoordinate = line.split(':')[1]
                coordinates[int(cityID)] = cityCoordinate

        # admin = models.User(email='admin@example.com', first_name="Админ", last_name="Админович", is_staff=True, is_superuser=True)
        # admin.set_password("")
        # admin.save()

        # df_names = pd.read_csv('main/management/commands/data.csv')

        # BASE_DIR = Path(__file__).resolve().parent

        name_surname = []
        for i in range(0, 500):
            first_name = df_names['name'][i]
            external_id = df_names['name'][i] + str(df_names['count'][i]) + str(df_names['rowid'][i])

            image = "static/" + random.choice(os.listdir(str(BASE_DIR) + "/images"))

            i += 1
            last_name = df_names['name'][i]
            name_surname.append(first_name + "//" + last_name)

            user = models.User(
                first_name=first_name, 
                last_name=last_name,
                external_id=str(external_id),
            )

            user.set_password("admin12345")
            user.save()

            city_id = random.randint(1, 10)
            user_profile = models.UserProfile(
                external_id="", 
                gender="f", 
                city=models.City.objects.filter(id=city_id).first(), 
                latitude=coordinates.get(city_id).split(',')[9], 
                longitude=coordinates.get(city_id).split(',')[1], 
                breefly=random.choice(interests), 
                birth_date=self.get_random_birthday()
            )

            # user_profile.save()
