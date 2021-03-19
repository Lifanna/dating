# -*- coding: utf-8 -*-
import os

GENDER = [
    ('f', 'Женщина'),
    ('m', 'Мужчина'),
]

GENDER_AND_EMPTY = [('', '', 'Выберите пол*')] + GENDER

# Moodle
MOODLE_HOST = os.environ.get("MOODLE_HOST")
MOODLE_WEB_TOKEN = os.environ.get("MOODLE_WEB_TOKEN")
MOODLE_MOB_TOKEN = os.environ.get("MOODLE_MOB_TOKEN")
