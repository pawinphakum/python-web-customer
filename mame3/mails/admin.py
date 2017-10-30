from django.contrib import admin

from .models import Customer, Car, MailHistory

# Register your models here.

class CarInline(admin.TabularInline):
    model = Car
    extra = 1

class CustomerAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ['name']
    list_filter = ['create_date']
    inlines = [CarInline]

admin.site.register(Customer, CustomerAdmin)

#

class MailHistoryInline(admin.TabularInline):
    model = MailHistory
    extra = 1

class CarAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': [
            'car_alphabet',
            'car_number',
            'car_province',
            'car_type',
            'expire_date',
            ]}),
        ('Date information', {'fields': ['create_date'], 'classes': ['collapse']}),
    ]
    list_display = ('car_alphabet','car_number','car_province','car_type','customerName')
    search_fields = ['car_number']
    list_filter = ['create_date','expire_date']
    inlines = [MailHistoryInline]
    def customerName(self, obj):
        return obj.customer.name

admin.site.register(Car, CarAdmin)
