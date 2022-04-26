from django.db import models


class Game(models.TextChoices):
    PUBG = "PUBG", "Player’s Unknown Battle Ground"
    FORT = "FORT", "Fortnite Battle Royale"
    APEX = "APEX", "Apex Legends"
    LOL = "LOL", "League of Legends"
    CSGO = "CSGO", "Counter Strike: Global Offensive"
    HEART = "HEART", "Heartstone"
    MINE = "MINE", "Minecraft"
    DOTA = "DOTA", "DOTA  2"
    DIV = "DIV", "The Division 2"
    SPLAT = "SPLAT", "The Splatoon 2"


class Player(models.Model):
    is_active = models.BooleanField(default=False)
    chat_id = models.IntegerField(default=9999999)
    username = models.CharField(max_length=150)
    steam = models.CharField(max_length=255)
    bio = models.TextField()
    game = models.TextField(choices=Game.choices)
