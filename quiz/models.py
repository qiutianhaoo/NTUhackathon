from django.db import models

# Create your models here.
'''
class Question(models.Model):

    questions = models.IntegerField(default = 5)
    #choices = (('0','UK IPA'), ('1','US IPA'), ('2','Klattese'), ('3','SAMPA'), ('4','ARPABET'))
    #option = models.CharField(max_length = 2, choices = choices)
'''

class Question(models.Model):
    number = models.IntegerField(default = 1)
    qn = models.TextField(default = "")
    option1 = models.TextField(default = "")
    option2 = models.TextField(default = "")
    option3 = models.TextField(default = "")
    option4 = models.TextField(default = "")
    option5 = models.TextField(default = "")
    ans = models.CharField(max_length = 1, default = "")

    def __str__(self):
        return self.qn
