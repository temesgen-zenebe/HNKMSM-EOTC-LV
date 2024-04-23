from django.contrib import admin
from .models import SermonCategory, SermonSeries, Sermon, SermonMedia, Comment

@admin.register(SermonSeries)
class SermonSeriesAdmin(admin.ModelAdmin):
    list_display = ('title', 'description')
    search_fields = ('title',)
    
@admin.register(SermonCategory)
class SermonCategoryAdmin(admin.ModelAdmin):
    list_display = ('category', 'subcategory')
    search_fields = ('category',)

@admin.register(Sermon)
class SermonAdmin(admin.ModelAdmin):
    list_display = ('title', 'preacher', 'date_preached', 'series')
    list_filter = ('date_preached', 'series', 'category')
    search_fields = ('title', 'preacher')
    date_hierarchy = 'date_preached'
    # prepopulated_fields = {'slug': ('title',)}  # Remove this line
    readonly_fields = ('created_at', 'updated',)
    # Additional customization as needed


@admin.register(SermonMedia)
class SermonMediaAdmin(admin.ModelAdmin):
    list_display = ('sermon', 'media_type', 'media_url')

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('sermon', 'user', 'created_at')
    search_fields = ('sermon__title', 'user__username')
    readonly_fields = ('created_at', 'respond_at',)

