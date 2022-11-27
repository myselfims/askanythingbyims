from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Question(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    title = models.CharField(max_length = 200)
    likes = models.IntegerField(default=0, blank=True, null=True)
    status = models.BooleanField(default=True)
    allow_comment = models.BooleanField(default=True)
    date = models.DateField( auto_now_add=True, blank=True, null= True)

    def __str__(self):
        return self.title
    

class Answer(models.Model):
    title = models.ForeignKey(Question, on_delete = models.CASCADE)
    option = models.CharField(max_length = 200)
    votes = models.IntegerField()
    
    def __str__(self):
        return self.option
    
    
class Voter(models.Model):
    title = models.ForeignKey(Question, on_delete=models.CASCADE, null=True,blank=True)
    option = models.ForeignKey(Answer, on_delete=models.CASCADE)
    ip_address = models.CharField(max_length=30)
    like = models.BooleanField(default=False)
    
  
class Comment(models.Model):
    title = models.ForeignKey(Question, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    comment = models.CharField(max_length=300)


