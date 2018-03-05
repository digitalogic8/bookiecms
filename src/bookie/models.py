from django.db import models



class Profile(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    def __str__(self):
        return self.question_text



class Bet(models.Model):
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE)
    #contest = models.ForeignKey(Contest, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
    def __str__(self):
        return self.choice_text