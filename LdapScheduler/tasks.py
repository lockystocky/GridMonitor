from datetime import timedelta
import datetime
from celery.task import periodic_task
import ldap
import os
from LdapScheduler.models import GridResourceEndpoint
from LdapScheduler.models import ExecutionEnvironment
from LdapScheduler.models import ComputingManager
from LdapScheduler.models import ComputingShare
from LdapScheduler.models import ComputingShareEndpoint
from LdapScheduler.models import ComputingShareExecutionEnvironment
import rrdtool
import base64

#os.environ.setdefault("DJANGO_SETTINGS_MODULE", "practice_work.settings")

'''
rrdtool.create(
    "database.rrd",
    "--start", "now",
    "--step", "60",
    "--no-overwrite",
    "DS:running_jobs:GAUGE:60:0:5000",
    "RRA:AVERAGE:0.5:1:500")
'''

print("created")

@periodic_task(run_every=timedelta(seconds=10))
def a():

    attributes = ["GLUE2EndpointID", "GLUE2EndpointURL", "GLUE2EndpointInterfaceName",
                  "GLUE2ComputingEndpointTotalJobs", "GLUE2ComputingEndpointRunningJobs",
                  "GLUE2ComputingEndpointWaitingJobs", "GLUE2ComputingEndpointStagingJobs",
                  "GLUE2ComputingEndpointSuspendedJobs", "GLUE2EndpointQualityLevel",
                  "GLUE2EndpointHealthState", "entryUUID"]

    connection = ldap.initialize("ldap://arc.univ.kiev.ua:2135")
    ldap_endpoints_list = connection.search_s("o=glue", ldap.SCOPE_SUBTREE, "(objectClass=GLUE2ComputingEndpoint)", attributes)

    for ldap_dn, ldap_ee in ldap_endpoints_list:
        if 'GLUE2EndpointURL' not in ldap_ee:
            continue
        print('---------------------------')
        for ce in ldap_ee['GLUE2EndpointID']:
            print(ce.decode('utf-8'))
        print('----------------------------')

        endpoint_id = (ldap_ee['GLUE2EndpointID'][0]).decode('utf-8')
        endpoint, created = GridResourceEndpoint.objects.get_or_create(endpoint_id=endpoint_id)
        endpoint.endpoint_url = ldap_ee['GLUE2EndpointURL'][0].decode('utf-8')
        endpoint.endpoint_interface_name = ldap_ee['GLUE2EndpointInterfaceName'][0].decode('utf-8')
        endpoint.entryUUID = ldap_ee['entryUUID'][0].decode('utf-8')
        end_id_base64 = base64.b64encode(endpoint.endpoint_id.encode('ascii')).decode('ascii')
        print('base64: ' + end_id_base64)
        endpoint.base64id = end_id_base64
        print('endpoint: ' + endpoint.endpoint_id)

        #if "GLUE2ComputingEndpointSuspendedJobs" in ldap_ee:
        #    endpoint.suspended_jobs_count = int(ldap_ee["GLUE2ComputingEndpointSuspendedJobs"][0].decode('utf-8'))

        if "GLUE2EndpointQualityLevel" in ldap_ee:
            endpoint.quality_level = ldap_ee["GLUE2EndpointQualityLevel"][0].decode('utf-8')

        if "GLUE2EndpointHealthState" in ldap_ee:
            endpoint.health_state = ldap_ee["GLUE2EndpointHealthState"][0].decode('utf-8')

        if 'GLUE2ComputingEndpointRunningJobs' in ldap_ee:
            running_jobs_count = int(
                (ldap_ee['GLUE2ComputingEndpointRunningJobs'][0]).decode('utf-8'))

            name = end_id_base64 + "_running_jobs_count.rrd"
            print(name)
            try:
                rrdtool.create(
                    name,
                    "--start", "now",
                    "--step", "60",
                    "--no-overwrite",
                    "DS:running_jobs:GAUGE:60:0:5000",
                    "RRA:AVERAGE:0.5:1:500")

            except:
                print('db exists')

            rrdtool.update(name, "N:" + str(running_jobs_count))
            print('running: ' + str(running_jobs_count))

        if "GLUE2ComputingEndpointTotalJobs" in ldap_ee:
            total_jobs_count = int(ldap_ee["GLUE2ComputingEndpointTotalJobs"][0].decode('utf-8'))
            name = end_id_base64 + "_total_jobs_count.rrd"

            try:
                rrdtool.create(
                    name,
                    "--start", "now",
                    "--step", "60",
                    "--no-overwrite",
                    "DS:total_jobs:GAUGE:60:0:5000",
                    "RRA:AVERAGE:0.5:1:500")

            except:
                print('db exists')

            rrdtool.update(name, "N:" + str(total_jobs_count))
            print('total: ' + str(total_jobs_count))

        if "GLUE2ComputingEndpointStagingJobs" in ldap_ee:
            staging_jobs_count = int(
                ldap_ee["GLUE2ComputingEndpointStagingJobs"][0].decode('utf-8'))
            name = end_id_base64 + "_staging_jobs_count.rrd"

            try:
                rrdtool.create(
                    name,
                    "--start", "now",
                    "--step", "60",
                    "--no-overwrite",
                    "DS:staging_jobs:GAUGE:60:0:5000",
                    "RRA:AVERAGE:0.5:1:500")

            except:
                print('db exists')

            rrdtool.update(name, "N:" + str(staging_jobs_count))
            print('staging: ' + str(staging_jobs_count))

        if "GLUE2ComputingEndpointWaitingJobs" in ldap_ee:
            waiting_jobs_count = int(
                ldap_ee["GLUE2ComputingEndpointWaitingJobs"][0].decode('utf-8'))
            name = end_id_base64 + "_waiting_jobs_count.rrd"

            try:
                rrdtool.create(
                    name,
                    "--start", "now",
                    "--step", "60",
                    "--no-overwrite",
                    "DS:waiting_jobs:GAUGE:60:0:5000",
                    "RRA:AVERAGE:0.5:1:500")

            except:
                print('db exists')

            rrdtool.update(name, "N:" + str(waiting_jobs_count))
            print('waiting: ' + str(waiting_jobs_count))

        if "GLUE2ComputingEndpointSuspendedJobs" in ldap_ee:
            suspended_jobs_count = int(ldap_ee["GLUE2ComputingEndpointSuspendedJobs"][0].decode('utf-8'))
            name = end_id_base64 + "_suspended_jobs_count.rrd"

            try:
                rrdtool.create(
                   name,
                   "--start", "now",
                   "--step", "60",
                   "--no-overwrite",
                   "DS:suspended_jobs:GAUGE:60:0:5000",
                   "RRA:AVERAGE:0.5:1:500")

            except:
                print('db exists')

            rrdtool.update(name, "N:" + str(suspended_jobs_count))
            print('suspended: ' + str(suspended_jobs_count))

        endpoint.save()

    print('running periodic task')




@periodic_task(run_every=timedelta(days=1))
def b():
    print('task B start')
    attributes = ["GLUE2ExecutionEnvironmentMainMemorySize", "GLUE2ExecutionEnvironmentOSFamily",
                  "GLUE2ExecutionEnvironmentPlatform", "GLUE2ExecutionEnvironmentCPUClockSpeed",
                  "GLUE2ExecutionEnvironmentCPUModel", "GLUE2ExecutionEnvironmentLogicalCPUs",
                  "GLUE2ExecutionEnvironmentVirtualMemorySize", "GLUE2ResourceID",
                  "GLUE2ExecutionEnvironmentComputingManagerForeignKey"]

    connection = ldap.initialize("ldap://arc.univ.kiev.ua:2135")
    ldap_endpoints_list = connection.search_s("o=glue", ldap.SCOPE_SUBTREE, "(objectClass=GLUE2ExecutionEnvironment)",
                                              attributes)

    for ldap_dn, ldap_ee in ldap_endpoints_list:

        resource_id = (ldap_ee['GLUE2ResourceID'][0]).decode('utf-8')
        exec_env, created = ExecutionEnvironment.objects.get_or_create(resource_id=resource_id)

        if 'GLUE2ExecutionEnvironmentMainMemorySize' in ldap_ee:
            exec_env.main_memory_size = int((ldap_ee['GLUE2ExecutionEnvironmentMainMemorySize'][0]).decode('utf-8'))

        if 'GLUE2ExecutionEnvironmentComputingManagerForeignKey' in ldap_ee:
            exec_env.computing_manager_id = (ldap_ee['GLUE2ExecutionEnvironmentComputingManagerForeignKey'][0]).decode(
                'utf-8')

        if 'GLUE2ExecutionEnvironmentOSFamily' in ldap_ee:
            exec_env.os_family = (ldap_ee['GLUE2ExecutionEnvironmentOSFamily'][0]).decode('utf-8')

        if 'GLUE2ExecutionEnvironmentPlatform' in ldap_ee:
            exec_env.platform = (ldap_ee['GLUE2ExecutionEnvironmentPlatform'][0]).decode('utf-8')

        if 'GLUE2ExecutionEnvironmentCPUClockSpeed' in ldap_ee:
            exec_env.cpu_clock_speed = int((ldap_ee['GLUE2ExecutionEnvironmentCPUClockSpeed'][0]).decode('utf-8'))

        if 'GLUE2ExecutionEnvironmentCPUModel' in ldap_ee:
            exec_env.cpu_model = (ldap_ee['GLUE2ExecutionEnvironmentCPUModel'][0]).decode('utf-8')

        if 'GLUE2ExecutionEnvironmentLogicalCPUs' in ldap_ee:
            exec_env.logical_cpus_count = int((ldap_ee['GLUE2ExecutionEnvironmentLogicalCPUs'][0]).decode('utf-8'))

        if 'GLUE2ExecutionEnvironmentVirtualMemorySize' in ldap_ee:
            exec_env.virtual_memory_size = int(
                (ldap_ee['GLUE2ExecutionEnvironmentVirtualMemorySize'][0]).decode('utf-8'))

        exec_env.save()

    attributes = ["GLUE2ManagerID", "GLUE2ManagerServiceForeignKey",
                  "GLUE2ComputingManagerSlotsUsedByLocalJobs", "GLUE2ComputingManagerSlotsUsedByGridJobs",
                  "GLUE2ComputingManagerTotalSlots"]

    connection = ldap.initialize("ldap://arc.univ.kiev.ua:2135")
    ldap_endpoints_list = connection.search_s("o=glue", ldap.SCOPE_SUBTREE, "(objectClass=GLUE2ComputingManager)",
                                              attributes)

    for ldap_dn, ldap_ee in ldap_endpoints_list:

        manager_id = (ldap_ee['GLUE2ManagerID'][0]).decode('utf-8')
        manager, created = ComputingManager.objects.get_or_create(manager_id=manager_id)

        if 'GLUE2ComputingManagerTotalSlots' in ldap_ee:
            manager.total_slots_count = int((ldap_ee['GLUE2ComputingManagerTotalSlots'][0]).decode('utf-8'))

        if 'GLUE2ComputingManagerSlotsUsedByLocalJobs' in ldap_ee:
            manager.slots_used_by_local_jobs_count = int(
                (ldap_ee['GLUE2ComputingManagerSlotsUsedByLocalJobs'][0]).decode(
                    'utf-8'))

        if 'GLUE2ComputingManagerSlotsUsedByGridJobs' in ldap_ee:
            manager.slots_used_by_grid_jobs_count = (ldap_ee['GLUE2ComputingManagerSlotsUsedByGridJobs'][0]).decode(
                'utf-8')

        if 'GLUE2ManagerServiceForeignKey' in ldap_ee:
            manager.computing_service_id = (ldap_ee['GLUE2ManagerServiceForeignKey'][0]).decode('utf-8')

        exec_env.save()

    attributes = ["GLUE2ShareID", "GLUE2ComputingShareComputingEndpointForeignKey",
                  "GLUE2ComputingShareMaxCPUTime", "GLUE2ComputingShareMaxRunningJobs",
                  "GLUE2ComputingShareMaxTotalJobs", "GLUE2ComputingShareMaxVirtualMemory",
                  "GLUE2ComputingShareExecutionEnvironmentForeignKey"]

    connection = ldap.initialize("ldap://arc.univ.kiev.ua:2135")
    ldap_endpoints_list = connection.search_s("o=glue", ldap.SCOPE_SUBTREE, "(objectClass=GLUE2ComputingShare)",
                                              attributes)

    for ldap_dn, ldap_ee in ldap_endpoints_list:

        share_id = (ldap_ee['GLUE2ShareID'][0]).decode('utf-8')
        share, created = ComputingShare.objects.get_or_create(share_id=share_id)

        if "GLUE2ComputingShareComputingEndpointForeignKey" in ldap_ee:
            for endpoint in ldap_ee["GLUE2ComputingShareComputingEndpointForeignKey"]:
                endpoint_id = endpoint.decode('utf-8')
                cse, created = ComputingShareEndpoint.objects.get_or_create(computing_share_id=share_id,
                                                                            computing_endpoint_id=endpoint_id)
                cse.computing_share_id = share_id
                cse.computing_endpoint_id = endpoint_id
                cse.save()

        if "GLUE2ComputingShareExecutionEnvironmentForeignKey" in ldap_ee:
            for env in ldap_ee["GLUE2ComputingShareExecutionEnvironmentForeignKey"]:
                environment_id = env.decode('utf-8')
                cse, created = ComputingShareExecutionEnvironment.objects.get_or_create(share_id=share_id,
                                                                                        environment_id=environment_id)
                cse.share_id = share_id
                cse.environment_id = environment_id
                cse.save()

        if "GLUE2ComputingShareMaxCPUTime" in ldap_ee:
            share.max_cpu_time = int((ldap_ee['GLUE2ComputingShareMaxCPUTime'][0]).decode('utf-8'))

        if "GLUE2ComputingShareMaxRunningJobs" in ldap_ee:
            share.max_running_jobs = int((ldap_ee['GLUE2ComputingShareMaxRunningJobs'][0]).decode('utf-8'))

        if "GLUE2ComputingShareMaxTotalJobs" in ldap_ee:
            share.max_total_jobs = int((ldap_ee['GLUE2ComputingShareMaxTotalJobs'][0]).decode('utf-8'))

        if "GLUE2ComputingShareMaxVirtualMemory" in ldap_ee:
            share.max_virtual_memory = int((ldap_ee['GLUE2ComputingShareMaxVirtualMemory'][0]).decode('utf-8'))

        share.save()

    print('task B stop')



