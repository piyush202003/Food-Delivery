from attr import field
from django.contrib import admin
from matplotlib.pyplot import cla

from accounts.models import Address, User

# Register your models here.
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display =('username', 'first_name', 'last_name', 'email', 'password', 'avatar', 'is_admin', 'is_staff', 'is_delivery_partner', 'last_login', 'date_joined', )
    readonly_fields = ('date_joined', 'last_login', )
    search_fields = ('username', 'email', 'first_name', 'last_name', )
    list_filter = ('is_admin', 'is_staff', 'is_delivery_partner', )
    fieldsets = (
        ('User Info',{
            'fields': ( 'username', 'first_name', 'last_name', 'avatar', 'email', 'password', )
        }),
        ('Authorities', {
            'fields' : ( "is_admin", 'is_staff', 'is_delivery_partner', )
        }),
        ('Time Stamp',{
            'fields': ( 'last_login', 'date_joined', )
        }),
    )

@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ('user', 'label', 'address', 'city', 'state', 'zip', 'is_default', 'lat', 'lng', 'created_at', 'updated_at', )
    search_fields = ('address', 'city', 'state', )
    readonly_fields = ('created_at', 'updated_at', )
    list_filter = ( 'label', )
    