from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
import markdown

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
    xp = models.IntegerField(default=0)  # Experience points
    hp = models.IntegerField(default=100)  # Health points
    mp = models.IntegerField(default=50)  # Mana points

    # Additional stats
    gold = models.PositiveIntegerField(default=0)  # In-game currency
    energy = models.PositiveIntegerField(default=100)  # Action energy
    achievements = models.JSONField(default=dict, blank=True)  # Store achievements

    def clean(self):
        '''Validate fields to ensure they are within acceptable ranges.'''
        if self.hp < 0:
            raise ValidationError({'hp': 'HP cannot be negative.'})
        if self.mp < 0:
            raise ValidationError({'mp': 'MP cannot be negative.'})
        if self.gold < 0:
            raise ValidationError({'gold': 'Gold cannot be negative.'})
        if self.energy < 0:
            raise ValidationError({'energy': 'Energy cannot be negative.'})

    def gain_xp(self, amount):
        '''Increase XP and level up if threshold is reached.'''
        if amount < 0:
            raise ValueError('XP amount must be positive.')
        self.xp += amount
        # Example leveling logic: Level up every 100 XP
        while self.xp >= 100:
            self.level += 1
            self.xp -= 100
            self.hp = 100  # Reset HP on level up
            self.mp = 50   # Reset MP on level up
        self.save()

    def take_damage(self, amount):
        '''Reduce HP when the player takes damage.'''
        if amount < 0:
            raise ValueError('Damage amount must be positive.')
        self.hp = max(self.hp - amount, 0)  # Ensure HP does not go below 0
        self.save()

    def use_mana(self, amount):
        '''Reduce MP when the player uses a skill or spell.'''
        if amount < 0:
            raise ValueError('Mana amount must be positive.')
        self.mp = max(self.mp - amount, 0)  # Ensure MP does not go below 0
        self.save()

    def __str__(self):
        return f'{self.username} (Level {self.level})'


class Course(models.Model):
    title = models.CharField(max_length=255)  # Name of course
    description = models.TextField()  # Description of course
    image = models.ImageField(upload_to='courses/', blank=True, null=True, default='courses/default.png')  # Default image
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['title']  # Order courses by title by default


class Section(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='sections')
    title = models.CharField(max_length=255)  # Title of section
    order = models.PositiveIntegerField()  # Order of section

    def __str__(self):
        return f'{self.course.title} - {self.title}'

    def clean(self):
        # Ensure order is unique within the course
        if Section.objects.filter(course=self.course, order=self.order).exclude(pk=self.pk).exists():
            raise ValidationError({'order': 'A section with this order already exists in the course.'})

    class Meta:
        ordering = ['order']  # Order sections by order by default
        unique_together = ['course', 'order']  # Ensure order is unique within a course


class Lesson(models.Model):
    section = models.ForeignKey(Section, on_delete=models.CASCADE, related_name='lessons')
    title = models.CharField(max_length=255)  # Title of lesson
    content = models.TextField()  # Content of lesson
    order = models.PositiveIntegerField()  # Order of lesson

    def __str__(self):
        return f'{self.section.course.title} - {self.section.title} - {self.title}'
    
    def get_markdown_content(self):
        return markdown.markdown(self.content)

    def clean(self):
        # Ensure order is unique within the section
        if Lesson.objects.filter(section=self.section, order=self.order).exclude(pk=self.pk).exists():
            raise ValidationError({'order': 'A lesson with this order already exists in the section.'})

    class Meta:
        ordering = ['order']  # Order lessons by order by default
        unique_together = ['section', 'order']  # Ensure order is unique within a section


class Quiz(models.Model):
    '''Represents a quiz associated with a lesson.'''
    lesson = models.ForeignKey('Lesson', on_delete=models.CASCADE, related_name='quizzes')
    title = models.CharField(max_length=255)  # Quiz title
    description = models.TextField(blank=True, null=True)  # Quiz description

    def __str__(self):
        return f'Quiz: {self.title}'

    class Meta:
        verbose_name_plural = 'Quizzes'


class Question(models.Model):
    '''Represents a question within a quiz.'''
    quiz = models.ForeignKey('Quiz', on_delete=models.CASCADE, related_name='questions')
    text = models.CharField(max_length=255)  # Question text

    def __str__(self):
        return f'Question: {self.text}'


class Option(models.Model):
    '''Represents an option for a question.'''
    question = models.ForeignKey('Question', on_delete=models.CASCADE, related_name='options')
    text = models.CharField(max_length=255)  # Option text
    is_correct = models.BooleanField(default=False)  # Indicates if this option is correct

    def __str__(self):
        return f'Option: {self.text} (Correct: {self.is_correct})'

    def clean(self):
        '''Ensure only one correct option per question.'''
        if self.is_correct:
            existing_correct_option = Option.objects.filter(question=self.question, is_correct=True).exclude(pk=self.pk).exists()
            if existing_correct_option:
                raise ValidationError('Only one correct option is allowed per question.')