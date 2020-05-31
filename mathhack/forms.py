from django import forms
from .models import SolvingVariant, ChangeUserModel
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from django.core.exceptions import ValidationError


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class ChangeUserForm(forms.ModelForm):
    class Meta:
        model = ChangeUserModel
        fields = ['change_username', 'change_grade', 'change_user_image']

    def clean_image(self):
        image = self.cleaned_data.get('change_user_image', False)
        if image:
            if image.size > 4*1024*1024:
                # raise ValidationError("Изображение больше чем 4МБ!")
                return 1
            return 0
        else:
            # raise ValidationError("Не получается прочитать изображение!")
            return 2


class SolvingVariantForm(forms.ModelForm):
    class Meta:
        model = SolvingVariant
        fields = ['task1', 'task2', 'task3', 'task4', 'task5',
                  'task6', 'task7', 'task8', 'task9', 'task10',
                  'task11', 'task12', 'task13', 'task14', 'task15',
                  'task16', 'task17', 'task18', 'task19', ]
