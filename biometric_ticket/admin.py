from django.contrib import admin
from .models import Customer, Fingerprint_device, Wallet, LED_bulb, Mappingstation ,Transaction
# Register your models here.

class CustomerAdmin(admin.ModelAdmin):
    list_display = ('name', 'uuid', 'contact', 'address', 'finger_print', 'status')
    

     

admin.site.register(Customer,CustomerAdmin)


class Fingerprint_deviceAdmin(admin.ModelAdmin):
    list_display = ('fid','location')  

admin.site.register(Fingerprint_device,Fingerprint_deviceAdmin)

class WalletAdmin(admin.ModelAdmin):
    list_display = ('uuid','money')  

admin.site.register(Wallet,WalletAdmin)
    

admin.site.register(LED_bulb)

class MappingstationAdmin(admin.ModelAdmin):
    list_display = ('all_station_name','ghatkopar')

admin.site.register(Mappingstation,MappingstationAdmin)

class TransactionAdmin(admin.ModelAdmin):
    list_display = ('uuid','source','destination','fare','time','status')

admin.site.register(Transaction,TransactionAdmin)

    