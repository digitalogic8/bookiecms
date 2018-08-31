from django.db import models
from django.contrib.auth.models import User



class BookieProfile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    siteName = models.CharField(max_length=200) 
    email = models.EmailField(default="anywhere@anyhow.com")
    
class BookieInvitation(models.Model):
    bookie = models.ForeignKey(BookieProfile, on_delete=models.CASCADE)
    invitedEmail = models.EmailField()
    filled = models.BooleanField()



