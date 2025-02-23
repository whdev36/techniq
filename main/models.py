from django.db import models
from django.contrib.auth.models import AbstractUser

class Player(AbstractUser):
    '''Player model that extends the Django AbstractUser.'''
    class Meta:
        verbose_name = 'Player'
        verbose_name_plural = 'Players'

    # Player information
    avatar = models.ImageField(upload_to='players/avatar', blank=True, null=True)
    bio = models.TextField(max_length=150, blank=True, null=True)
    location = models.CharField(max_length=200, blank=True, null=True)


    # Basic attributes

    level = models.PositiveIntegerField(default=0)  # Player level


    # Stats

    xp = models.IntegerField(default=0)  # experience point
    hp = models.IntegerField(default=100)  # health point
    mp = models.IntegerField(default=50)  # mana point


    # Additional stats

    gold = models.PositiveIntegerField(default=0)  # in-game  currency
    energy = models.PositiveIntegerField(default=100)  # action energy
    achievements = models.JSONField(default=dict, blank=True)  # store achievements

    def gain_xp(self, amount):
        '''Increase XP and level up if threshold is reached.'''
        pass

    def take_damage(self, amount):
        '''Reduce HP when the player takes damage.'''
        pass

    def use_mana(self, amount):
        '''Reduce MP when the player uses a skill or spell.'''
        pass

    def __str__(self):
        return f'{self.username} (Level {self.level})'
    
class Course(models.Model):

    title = models.CharField(max_length=255)  # name of course
    description = models.TextField()  # description of course
    image = models.ImageField(upload_to='courses/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    
class Section(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='sections')
    title = models.CharField(max_length=255)  # title of section
    order = models.PositiveIntegerField()  # order of section

    def __str__(self):
        return f'{self.course.title} - {self.title}'
    
class Lesson(models.Model):
    section = models.ForeignKey(Section, on_delete=models.CASCADE, related_name='lessons')
    title = models.CharField(max_length=255)  # title of lesson
    content = models.TextField()  # content of lesson
    order = models.PositiveIntegerField()  # order of lesson

    def __str__(self):
        return f'{self.section.course.title} - {self.section.title} - {self.title}'


class Quiz(models.Model):
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='quizzes')
    question = models.CharField(max_length=255)  # question
    option_1 = models.CharField(max_length=255)
    option_2 = models.CharField(max_length=255)
    option_3 = models.CharField(max_length=255)
    option_4 = models.CharField(max_length=255)
    correct_answer = models.CharField(max_length=255)  # correct answer

    def __str__(self):
        return f'Quiz: {self.question}'