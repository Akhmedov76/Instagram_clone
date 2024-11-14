from django.contrib import admin

from app_accounts.models import UserModel, VerificationModel

admin.site.register(UserModel)
admin.site.register(VerificationModel)
