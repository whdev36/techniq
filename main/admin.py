from django.contrib import admin
from .models import Player
from .models import Course, Section, Lesson, Quiz

admin.site.register(Player)

admin.site.register(Course)
admin.site.register(Section)
admin.site.register(Lesson)
admin.site.register(Quiz)