from django.contrib import admin
from .models import UserProfile
# Register your models here.
admin.site.register(UserProfile)
class DonationAdmin(admin.ModelAdmin):
    list_display = ('amount', 'currency', 'transaction_id', 'created_at')
    search_fields = ('transaction_id')