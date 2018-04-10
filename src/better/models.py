from django.db import models


class Team(models.Model):
    NCAAF = "NCAAF"
    NCAABB = "NCAABB"
    NCAAM = "NCAAM"
    NCAAW = "NCAAW"
    SPORTS = (
        (NCAAF, 'NCAA Football'),
        (NCAABB, 'NCAA Baseball'),
        (NCAAM, 'NCAA Mens Basketball'),
        (NCAAW, 'NCAA Womens Basketball'),
    )
    teamName = models.CharField(max_length=200)
    sport = models.CharField(
        max_length=100,
        choices=SPORTS,
        default=NCAAF,
    )
    teamPhoto = models.URLField()
    def __str__(self):
        return self.teamName
class Contest(models.Model):
    homeTeam = models.ForeignKey(Team, related_name='homeTeam', on_delete=models.CASCADE)
    awayTeam = models.ForeignKey(Team, related_name='awayTeam', on_delete=models.CASCADE)
    overUnder = models.FloatField()
    line = models.FloatField()
    contestPhoto = models.URLField()
    contest_date = models.DateTimeField('Date Of Contest')
    def __str__(self):
        return str(self.homeTeam) + " vs " + str(self.awayTeam)
class AvailableBets(models.Model):
    contest = models.ForeignKey(Contest, related_name='bet', on_delete=models.CASCADE)
    BETTYPES = (
        ("O/U", 'Over Under'),
        ("line", 'Bet on the line'),
        ("moneyline", "moneyline bet")
        
    )
    teamName = models.CharField(max_length=200)
    sport = models.CharField(
        max_length=100,
        choices=BETTYPES,
        default="straight",
    )
class Bet(models.Model):
    timestamp = models.DateTimeField('Date Of Contest')
    numberOfBet =  models.ForeignKey(AvailableBets, related_name='betnumber', on_delete=models.CASCADE)
    userMakingBet = models.CharField(max_length=200) 
    line = models.FloatField()
    amountOfBet = models.FloatField()
    approved = models.BooleanField()
    outcome = models.CharField(max_length=1)  

    
    