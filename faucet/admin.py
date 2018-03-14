from django.contrib import admin
from django.utils.safestring import mark_safe

from faucet.models import Account, Lecture


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    readonly_fields = ('ip', 'authorized_network', 'uid')
    list_display = ('name', 'authorized_network', 'uid', 'first_name', 'last_name', 'created')
    search_fields = ('name', 'uid', 'first_name', 'last_name')


@admin.register(Lecture)
class LectureAdmin(admin.ModelAdmin):
    list_display = ('topic_id', 'account_name', 'open_href')

    def open_href(self, instance):
        return mark_safe('<a href="%s" target="blank">открыть</a>' % (instance.topic_url))

    open_href.short_description = 'ссылка'
