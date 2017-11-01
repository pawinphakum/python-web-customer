from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.urls import reverse
from django.core.urlresolvers import reverse_lazy
from django.views.generic.list import ListView
from django.views.generic.edit import FormView
from django.utils import timezone
#from datetime import date
import datetime
from django.core import serializers
import json
from .models import Customer, Car, MailHistory
from .forms import CustomerCarForm, SearchForm
import re

# Create your views here.
# def index(request):
#    return HttpResponse('Hello World')

def checkname(request):
    fullname = request.GET.get('fullname', None)
    remark = request.GET.get('remark', None)
    customer = Customer.objects.filter(name=fullname)
    response_data = {}
    if(customer):
        car_list = customer[0].car_set.all()
        response_data['customer'] = json.loads(serializers.serialize('json', customer))
        response_data['car_list'] = json.loads(serializers.serialize('json', car_list))
    return JsonResponse(response_data)

class CustomerCarView(FormView):
    template_name = 'mails/customercar.html'
    form_class = CustomerCarForm
    success_url = reverse_lazy('mails:index')
    #success_url = 'bad url'

    nowdate = timezone.now()

    def get_context_data(self, **kwargs):
        context = super(CustomerCarView, self).get_context_data(**kwargs)
        context['nowdate'] = self.nowdate
        context['car_list'] = Car.objects.filter(update_date__gt=self.nowdate.date()).select_related('customer')
        return context


    def form_valid(self, form):
        name = form.cleaned_data['name']
        addr = form.cleaned_data['addr']
        soi = form.cleaned_data['soi']
        road = form.cleaned_data['road']
        moo = form.cleaned_data['moo']
        tumbon = form.cleaned_data['tumbon']
        amphur = form.cleaned_data['amphur']
        province = form.cleaned_data['province']
        postcode = form.cleaned_data['postcode']
        tel = form.cleaned_data['tel']
        remark = form.cleaned_data['remark']
        car_alphabet = form.cleaned_data['car_alphabet']
        car_number = form.cleaned_data['car_number']
        car_province = form.cleaned_data['car_province']
        car_type = form.cleaned_data['car_type']
        is_tro = form.cleaned_data['is_tro']
        is_insure = form.cleaned_data['is_insure']
        is_paytax = form.cleaned_data['is_paytax']
        is_special = form.cleaned_data['is_special']
        is_sms = form.cleaned_data['is_sms']
        expire_date = form.cleaned_data['expire_date']

        def newCar(customer):
            car = Car()
            car.customer = customer
            car.car_alphabet = car_alphabet
            car.car_number = car_number
            car.car_province = car_province
            car.car_type = car_type
            car.is_tro = is_tro
            car.is_insure = is_insure
            car.is_paytax = is_paytax
            car.is_special = is_special
            car.is_sms = is_sms
            # html input '251161' > form class '2061-11-25' > db date -43 years
            car.expire_date = date(expire_date.year-43, expire_date.month, expire_date.day)
            car.save()
            mHistory = MailHistory()
            mHistory.car = car
            mHistory.save()

        def updateCar(car_alphabet, car_number, car_province, customer):
            car = Car.objects.filter(
                car_alphabet__exact=car_alphabet,
                car_number__exact=car_number,
                car_province__exact=car_province).first()
            if car:
                print('Exist Car')
                car.car_type = car_type
                car.is_tro = is_tro
                car.is_insure = is_insure
                car.is_paytax = is_paytax
                car.is_special = is_special
                car.is_sms = is_sms
                # html input '251161' > form class '2061-11-25' > db date -43 years
                car.expire_date = date(expire_date.year-43, expire_date.month, expire_date.day)
                car.update_date = self.nowdate
                car.customer = customer
                print('Update Car')
                car.save()
                mHistory = MailHistory()
                mHistory.car = car
                mHistory.save()
            else:
                print('New Car')
                newCar(customer)

        # customer = Customer.objects.get(name=name) # Single Object , try , catch
        # customer = Customer.objects.filter(name__exact=name) # List Objects , List , None
        customer = Customer.objects.filter(name=name).first() # Single Object , Single , None
        if customer:
            print('Exist Customer')
            isChange = False
            if customer.addr != addr:
                customer.addr = addr
                isChange = True
            if customer.soi != soi:
                customer.soi = soi
                isChange = True
            if customer.road != road:
                customer.road = road
                isChange = True
            if customer.moo != moo:
                customer.moo = moo
                isChange = True
            if customer.tumbon != tumbon:
                customer.tumbon = tumbon
                isChange = True
            if customer.amphur != amphur:
                customer.amphur = amphur
                isChange = True
            if customer.province != province:
                customer.province = province
                isChange = True
            if customer.postcode != postcode:
                customer.postcode = postcode
                isChange = True
            if customer.tel != tel:
                customer.tel = tel
                isChange = True
            if customer.remark != remark:
                customer.remark = remark
                isChange = True

            if isChange:
                print('Update Customer')
                customer.save()

            updateCar(car_alphabet, car_number, car_province, customer)

        else:
            print('New Customer')
            customer = Customer()
            customer.name = name
            customer.addr = addr
            customer.soi = soi
            customer.road = road
            customer.moo = moo
            customer.tumbon = tumbon
            customer.amphur = amphur
            customer.province = province
            customer.postcode = postcode
            customer.tel = tel
            customer.remark = remark
            customer.save()

            updateCar(car_alphabet, car_number, car_province, customer)

        return super(CustomerCarView, self).form_valid(form)

class SearchView(FormView):
    template_name = 'mails/search.html'
    form_class = SearchForm
    #success_url = reverse_lazy('mails:search')

    # initial context
    #def get_context_data(self, **kwargs):
    #    print('get_context_data')
    #    context = super(SearchView, self).get_context_data(**kwargs)
    #    context['myname'] = 'jesper'
    #    return context

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form, **kwargs)

    def form_valid(self, form, **kwargs):
        car_result = Car.objects.none()
        search = form.cleaned_data['search']
        search = search.strip()
        print('search:'+search+':')
        #regex
        byCarNumber = re.compile('^[0-9]{1,4}$')
        byName = re.compile('^\D+$')
        byUpdateDate = re.compile('^[0-9]{6}$')

        if(byCarNumber.match(search)):
            print('byCarNumber')
            car_result = Car.objects.filter(car_number=search).select_related('customer')
        elif(byName.match(search)):
            print('byName')
            car_result = Car.objects.filter(customer__name__contains=search).select_related('customer')
        elif(byUpdateDate.match(search)):
            print('byUpdateDate')
            year = 2017
            month = 10
            day = 28
            car_result = Car.objects.filter(update_date__date=datetime.date(year, month, day)).select_related('customer')
        else:
            print('no match')

        print(car_result.query)
        context = self.get_context_data(**kwargs)
        context['car_list'] = car_result
        return self.render_to_response(context)
