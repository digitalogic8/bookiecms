from django.db import models



class Bets(models.Model):
    contest = models.CharField(max_length=200)
    whichTeam = models.CharField(max_length=200)
    def __str__(self):
        return self.whichTeam


