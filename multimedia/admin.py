from django.contrib import admin
from .models import BooksLibrary, Gallery, UserManual, PraiseGlory, TestimonyOfSalvation, ArchiveLink

admin.site.register(BooksLibrary)
admin.site.register(Gallery)
admin.site.register(UserManual)
admin.site.register(PraiseGlory)
admin.site.register(TestimonyOfSalvation)
admin.site.register(ArchiveLink)