from django.contrib import admin
from .models import (
    BooksLibrary, Gallery, UserManual, 
    PraiseGlory, TestimonyOfSalvation, 
    ArchiveLink,SpiritualPoemSong 
)

admin.site.register(BooksLibrary)
admin.site.register(Gallery)
admin.site.register(UserManual)
admin.site.register(PraiseGlory)
admin.site.register(TestimonyOfSalvation)
admin.site.register(ArchiveLink)

@admin.register(SpiritualPoemSong)
class SpiritualPoemSongAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'type', 'language', 'published_date', 'created_by')
    search_fields = ('title', 'author', 'content')
    list_filter = ('type', 'language', 'published_date')
    prepopulated_fields = {'slug': ('title',)}
