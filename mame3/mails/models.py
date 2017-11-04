import datetime
#import json
from django.db import models
from django.utils import timezone

class Customer(models.Model):
    name = models.CharField(max_length=200)
    addr = models.CharField(max_length=45)
    soi = models.CharField(max_length=200, blank=True)
    road = models.CharField(max_length=200, blank=True)
    moo = models.CharField(max_length=10, blank=True)
    tumbon = models.CharField(max_length=200)
    amphur = models.CharField(max_length=200)
    province = models.CharField(max_length=200)
    postcode = models.CharField(max_length=10)
    tel = models.CharField(max_length=45, blank=True)
    remark = models.CharField(max_length=200, blank=True)
    create_date = models.DateTimeField('date created customer', default=timezone.now)

class Car(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    car_alphabet = models.CharField(max_length=10)
    car_number = models.CharField(max_length=10)
    car_province = models.CharField(max_length=10)
    car_type = models.CharField(max_length=10)
    is_tro = models.BooleanField(default=False)
    is_insure = models.BooleanField(default=False)
    is_paytax = models.BooleanField(default=False)
    is_special = models.BooleanField(default=False)
    is_sms = models.BooleanField(default=False)
    create_date = models.DateTimeField('date created car', default=timezone.now)
    expire_date = models.DateTimeField('date expire tax')
    update_date = models.DateTimeField('date update data', default=timezone.now)

class MailHistory(models.Model):
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    create_date = models.DateTimeField('date created mail', default=timezone.now)
