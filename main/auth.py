# -*- coding: utf-8 -*-
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password


class CustomBackend(ModelBackend):
    """
    Аутентификация пользователя может происходить через email или номер телефона
    """
    def authenticate(self, request, username=None, password=None, **kwargs):

        User = get_user_model()
        if username is None:
            username = kwargs.get(User.USERNAME_FIELD)
        if username is None or password is None:
            return
        if not isinstance(username, str):
            return
        
        allow = False
        try:
            user = User.objects.get(aituUserId__exact=username)
        except User.DoesNotExist:
            return
        
        if self.user_can_authenticate(user):
            # once the user was logged in, we update all his information from NL
            return user

        return
