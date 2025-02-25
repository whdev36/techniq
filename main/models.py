from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError

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