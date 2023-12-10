from django.contrib import admin

from .models import User, Wallet


# Create an admin class for the User model with an inlineForm for the Wallet model


class WalletInline(admin.TabularInline):
    model = Wallet
    extra = 1


class UserAdmin(admin.ModelAdmin):
    inlines = [WalletInline]
    exclude = ('wallet',)


admin.site.register(User, UserAdmin)
