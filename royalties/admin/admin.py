from django.conf import settings
from django.contrib import admin
from django.contrib.auth import admin as auth_admin


from royalties.models import (
    Artist,
    Artwork,
    Diffusion,
    Supplier,
    Royalty,
    Payment,
    Notification,
)

class ArtistAdmin(admin.ModelAdmin):
    pass


class ArtworkAdmin(admin.ModelAdmin):
    pass


class DiffusionAdmin(admin.ModelAdmin):
    pass


class SupplierAdmin(admin.ModelAdmin):
    pass


class RoyaltyAdmin(admin.ModelAdmin):
    pass


class PaymentAdmin(admin.ModelAdmin):
    pass


class NotificationAdmin(admin.ModelAdmin):
    pass


class AdminSite(admin.AdminSite):
    pass


admin_site = AdminSite()
admin_site.register(Notification, NotificationAdmin)
admin_site.register(Payment, PaymentAdmin)
admin_site.register(Royalty, RoyaltyAdmin)
admin_site.register(Supplier, SupplierAdmin)
admin_site.register(Diffusion, DiffusionAdmin)
admin_site.register(Artwork, ArtworkAdmin)
admin_site.register(Artist, ArtistAdmin)

# register dependencies in our admin too
admin_site.register(auth_admin.User, auth_admin.UserAdmin)
admin_site.register(auth_admin.Group, auth_admin.GroupAdmin)
