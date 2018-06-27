from django.db import models


class Team(models.Model):
     NCAAF = "NCAAF"
     NCAABB = "NCAABB"
     NCAAM = "NCAAM"
     NCAAW = "NCAAW"
     MLB = "MLB"
     SPORTS = (
         (NCAAF, 'NCAA Football'),
         (NCAABB, 'NCAA Baseball'),
         (NCAAM, 'NCAA Mens Basketball'),
         (NCAAW, 'NCAA Womens Basketball'),
        (MLB, "Major League Baseball")
     )  
     teamName = models.CharField(max_length=200)
     teamAbbreviation = models.CharField(max_length=10, default="XXX")
     sport = models.CharField(
        max_length=100,
        choices=SPORTS,
        default=MLB,
     )
     teamLogo = models.CharField(max_length=200, default="XXX")
     def __str__(self):
        return self.teamName

class Contest(models.Model):
    PHASES = (
        ("upcoming", 'This game is in the future'),
        ("ongoing", "This game is currently being played"),
        ("final", "this game is over")
        
    )
    homeTeam = models.ForeignKey(Team, related_name='homeTeam', on_delete=models.CASCADE)
    awayTeam = models.ForeignKey(Team, related_name='awayTeam', on_delete=models.CASCADE)
    contest_date = models.DateTimeField('Date Of Contest')
    homeScore = models.IntegerField('Home Score', default=0)
    awayScore = models.IntegerField('Away Score', default=0)
    gamePhase = models.CharField(
        max_length=100,
        choices=PHASES,
        default="upcoming",
    )
    def __str__(self):
        return str(self.homeTeam) + " vs " + str(self.awayTeam)
class AvailableBets(models.Model):
    BETTYPES = (
        ("spread", 'Bet on the line'),
        ("moneyline", "moneyline bet"),
        ("total", "runline bet")
        
    )
    OUnder = (
        ("under", 'total score will score over this many points'),
        ("over", "total score will be under this many points"),
        ("na", "na")
        
    )
    contest = models.ForeignKey(Contest, related_name='availableBet', on_delete=models.CASCADE)
    odds = models.FloatField(default=0.0)
    spread = models.FloatField(default=0.0)
    overorunder = models.CharField(
        max_length=10,
        choices=OUnder,
        default="na",
    )
    team = models.ForeignKey(Team, related_name='team', on_delete=models.CASCADE, null=True)
    bettype = models.CharField(
        max_length=100,
        choices=BETTYPES,
        default="spread",
    )
class Bet(models.Model):
    timestamp = models.DateTimeField('Date Of Contest')
    numberOfBet =  models.ForeignKey(AvailableBets, related_name='betnumber', on_delete=models.CASCADE)
    userMakingBet = models.CharField(max_length=200) 
    line = models.FloatField()
    amountOfBet = models.FloatField()
    approved = models.BooleanField()
    outcome = models.CharField(max_length=1)  
    


    
    