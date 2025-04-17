from django.contrib import admin
from .models import Ad, ExchangeProposal

@admin.register(Ad)
class AdAdmin(admin.ModelAdmin):
    list_display = ['title', 'user', 'category', 'condition', 'created_at']
    list_filter = ['category', 'condition']
    search_fields = ['title', 'description']

@admin.register(ExchangeProposal)
class ProposalAdmin(admin.ModelAdmin):
    list_display = ['ad_sender', 'ad_receiver', 'status', 'created_at']
    list_filter = ['status']