from django.contrib import admin
from .models import *


class BlockAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}


class BlockMessagesAdmin(admin.ModelAdmin):
    pass


class DutyAdmin(admin.ModelAdmin):
    fields = ('block', 'sending_user', 'responsible_person', 'date_added', 'duty_date', 'room')
    readonly_fields = ('date_added',)


class AdsAdmin(admin.ModelAdmin):
    fields = ('title', 'user', 'content', 'created_at', 'updated_at', 'views',)
    readonly_fields = ('views', 'created_at', 'updated_at')


class GeneralChatMessagesAdmin(admin.ModelAdmin):
    fields = ('user', 'text', 'date_added',)
    readonly_fields = ('date_added',)


class NewsAdmin(admin.ModelAdmin):
    fields = ('title', 'content', 'views', 'likes', 'dislikes', 'created_at', 'updated_at')
    readonly_fields = ('views', 'created_at', 'updated_at')


admin.site.register(Block, BlockAdmin)
admin.site.register(BlockMessages, BlockMessagesAdmin)
admin.site.register(Duty, DutyAdmin)
admin.site.register(Ads, AdsAdmin)
admin.site.register(GeneralChatMessages, GeneralChatMessagesAdmin)
admin.site.register(News, NewsAdmin)
