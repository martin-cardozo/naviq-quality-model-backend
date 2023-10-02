from django.contrib import admin
from .models import User, Evaluation, Answer_Option, Application, Property, Criterion, Quality_Profile , Evaluation_Answer

admin.site.register(Answer_Option)
admin.site.register(Application)
admin.site.register(Property)
admin.site.register(Criterion)
admin.site.register(Quality_Profile)
admin.site.register(User)
admin.site.register(Evaluation_Answer)
admin.site.register(Evaluation)
