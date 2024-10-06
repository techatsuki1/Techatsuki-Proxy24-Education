from django.contrib import admin
from .models import CustomUser

class CustomUserAdmin(admin.ModelAdmin):
    # Specify fields to be displayed in the list view
    list_display = (
        'username',
        'email',
        'status',
        
        
        'gender',
        
    )
    
    # Add filters for these fields
    list_filter = (
        'status',
        'gender',
        'designation',
        
    )
    
    # Add search functionality to these fields
    search_fields = (
        'username',
        'email',
        'phone_number',
        'address',
        'city_name',
        'district_name',
        'postcode',
    )
    
    # Optionally add ordering
    ordering = ('username',)

# Register the CustomUser model with the CustomUserAdmin class
admin.site.register(CustomUser, CustomUserAdmin)

