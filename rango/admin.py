from django.contrib import admin
from rango.models import Category, Page, UserProfile,RecommendedDish
# Register your models here.
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('name',)}
class PageAdmin(admin.ModelAdmin):
    list_display = ('title','category', 'url')
class DishAdmin(admin.ModelAdmin):
    list_display = ('page','user', 'dish_name')    
admin.site.register(RecommendedDish,DishAdmin)
admin.site.register(Category,CategoryAdmin)
admin.site.register(Page,PageAdmin)
admin.site.register(UserProfile)
