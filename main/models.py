from django.db import models
from django.contrib.auth.models import AbstractUser

class Player(AbstractUser):
    '''Player model that extends the Django AbstractUser.'''
    class Meta:
        verbose_name = 'Player'
        verbose_name_plural = 'Players'


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