from django.contrib import admin
from .models import Person, PollQuestion,Choice,Response
# Register your models here.

class ChoiceInLine(admin.TabularInline):
    model = Choice
    extra = 1

class ChoiceAdmin(admin.ModelAdmin):
    list_display = ('id','choice_text','votes',)

admin.site.register(Choice, ChoiceAdmin)

class PollQueAdmin(admin.ModelAdmin):
    list_display = ('id','que_text','created_by','poll_name','created_at','updated_at')
    inlines = [ChoiceInLine]
admin.site.register(PollQuestion, PollQueAdmin)

class PersonAdmin(admin.ModelAdmin):
    list_display = ('username','email',)

admin.site.register(Person, PersonAdmin)

class ResponseAdmin(admin.ModelAdmin):
    list_display = ('id',)

admin.site.register(Response, ResponseAdmin)

