from django.contrib import admin
from . models import Post, User, Follow, Like

# Register your models here.


#class Follow_Admin(admin.ModelAdmin):
#    filter_horizontal = ("follows",)

admin.site.register(Post)
admin.site.register(User)
admin.site.register(Follow)
admin.site.register(Like)
