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