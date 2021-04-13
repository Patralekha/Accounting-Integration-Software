from django.db import models
from django.contrib.postgres.fields import JSONField
from fuzzycount import FuzzyCountManager



class Accounts(models.Model):
    id=models.AutoField(primary_key=True)
    accountName=models.CharField(max_length=400)
    accountId=models.IntegerField()
    amount=models.DecimalField(max_digits=15, decimal_places=3)
    date=models.DateField()
    accountType=models.CharField(max_length=6)
    providerName=models.CharField(max_length=20)
    extraFields=JSONField(null=True,blank=True)

    objects = FuzzyCountManager()
    
    def __str__(self):
        return "{}-{}-{}-{}-{}-{}".format(self.id,self.accountId,self.accountName,self.accountType,self.amount,self.date)

