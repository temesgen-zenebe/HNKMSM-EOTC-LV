
from django.contrib import admin
from .models import MembersUpdateInformation, Child, Relative

class ChildInline(admin.TabularInline):
    model = Child
    extra = 1

class RelativeInline(admin.TabularInline):
    model = Relative
    extra = 1

class MembersUpdateInformationAdmin(admin.ModelAdmin):
    inlines = [ChildInline, RelativeInline]
    list_display = ('member_id','user', 'full_name', 'baptismal_name', 'godfather', 'city', 'state', 'email', 'marital_status','how_mony_children','how_mony_relatives', 'slug', 'created', 'updated')
    prepopulated_fields = {"slug": ("full_name",)}

admin.site.register(MembersUpdateInformation, MembersUpdateInformationAdmin)
admin.site.register(Child)
admin.site.register(Relative)