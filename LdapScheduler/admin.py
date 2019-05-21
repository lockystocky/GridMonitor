from django.contrib import admin
from LdapScheduler.models import GridResourceEndpoint
from LdapScheduler.models import ComputingShareEndpoint
from LdapScheduler.models import ComputingShare
from LdapScheduler.models import ComputingShareExecutionEnvironment
from LdapScheduler.models import ExecutionEnvironment

# Register your models here.

admin.site.register(GridResourceEndpoint)
admin.site.register(ComputingShareEndpoint)
admin.site.register(ComputingShare)
admin.site.register(ComputingShareExecutionEnvironment)
admin.site.register(ExecutionEnvironment)
