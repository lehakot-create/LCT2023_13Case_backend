from django.contrib import admin
from .models import (Status, Stack, Profile, TypeProject,
                     Public, Direction, Rate, Stage, Project,)

# Register your models here.
admin.site.register((Status, Stack, TypeProject, Public,
                     Direction, Rate, Stage, Project, ))


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('nick_name', 'id_status', 'first_name', 'last_name','description',
                    'img', 'telephone', 'email', 'get_stacks', )
#
# @admin.register(Project)
# class ProjectAdmin(admin.ModelAdmin):
#     list_display = ('id_project_type', 'name', 'id_type', 'members_limit', 'members',
#                     'direction', 'deadline', 'id_rate', 'id_stage', 'rating', )