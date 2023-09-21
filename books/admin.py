from django.contrib import admin
from .models import Book, Section


class BookAdmin(admin.ModelAdmin):
    pass


class SectionAdmin(admin.ModelAdmin):
    pass


admin.site.register(Book, BookAdmin)
admin.site.register(Section, SectionAdmin)
