from django.contrib import admin
from .models import Person, PollQuestion,Choice
# Register your models here.

class ChoiceAdmin(admin.ModelAdmin):
    list_display = ('id','choice_text','votes',)

admin.site.register(Choice, ChoiceAdmin)

class PollQueAdmin(admin.ModelAdmin):
    list_display = ('id','que_text','created_by','poll_name','created_at','updated_at')

admin.site.register(PollQuestion, PollQueAdmin)

class PersonAdmin(admin.ModelAdmin):
    list_display = ('username','email',)

admin.site.register(Person, PersonAdmin)
