from django.contrib import admin
from .models import Task, Variant, Author
from .models import ChangeUserModel, Customer, SolvingVariant

admin.site.register(Task)
admin.site.register(Variant)
admin.site.register(Author)

admin.site.register(ChangeUserModel)
admin.site.register(Customer)
admin.site.register(SolvingVariant)
