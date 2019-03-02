from datetime import timedelta
import datetime
from celery.task import periodic_task
import ldap
from LdapScheduler.models import GridResourceEndpoint

@periodic_task(run_every=timedelta(seconds=10))
def a():

    attributes = ["GLUE2EndpointID", "GLUE2EndpointURL", "GLUE2EndpointInterfaceName",
                  "GLUE2ComputingEndpointTotalJobs", "GLUE2ComputingEndpointRunningJobs",
                  "GLUE2ComputingEndpointWaitingJobs", "GLUE2ComputingEndpointStagingJobs",
                  "GLUE2ComputingEndpointSuspendedJobs", "GLUE2EndpointQualityLevel",
                  "GLUE2EndpointHealthState"]

    connection = ldap.initialize("ldap://arc.univ.kiev.ua:2135")
    ldap_endpoints_list = connection.search_s("o=glue", ldap.SCOPE_SUBTREE, "(objectClass=GLUE2ComputingEndpoint)", attributes)

    for ldap_dn, ldap_ee in ldap_endpoints_list:
        if 'GLUE2EndpointURL' not in ldap_ee:
            continue
        # get endpoint data

        grid_resource_endpoint = GridResourceEndpoint()

        grid_resource_endpoint.record_time = datetime.datetime.now()

        grid_resource_endpoint.endpoint_id = ldap_ee['GLUE2EndpointID'][0].decode('utf-8')

        grid_resource_endpoint.endpoint_url = ldap_ee['GLUE2EndpointURL'][0].decode('utf-8')

        grid_resource_endpoint.endpoint_interface_name = ldap_ee['GLUE2EndpointInterfaceName'][0].decode('utf-8')

        if 'GLUE2ComputingEndpointRunningJobs' in ldap_ee:
            grid_resource_endpoint.running_jobs_count = int((ldap_ee['GLUE2ComputingEndpointRunningJobs'][0]).decode('utf-8'))

        if "GLUE2ComputingEndpointTotalJobs" in ldap_ee:
            grid_resource_endpoint.total_jobs_count = int(ldap_ee["GLUE2ComputingEndpointTotalJobs"][0].decode('utf-8'))

        if "GLUE2ComputingEndpointStagingJobs" in ldap_ee:
            grid_resource_endpoint.staging_jobs_count = int(ldap_ee["GLUE2ComputingEndpointStagingJobs"][0].decode('utf-8'))

        if "GLUE2ComputingEndpointWaitingJobs" in ldap_ee:
            grid_resource_endpoint.waiting_jobs_count = int(ldap_ee["GLUE2ComputingEndpointWaitingJobs"][0].decode('utf-8'))

        if "GLUE2ComputingEndpointSuspendedJobs" in ldap_ee:
            grid_resource_endpoint.suspended_jobs_count = int(ldap_ee["GLUE2ComputingEndpointSuspendedJobs"][0].decode('utf-8'))

        if "GLUE2EndpointQualityLevel" in ldap_ee:
            grid_resource_endpoint.quality_level = ldap_ee["GLUE2EndpointQualityLevel"][0].decode('utf-8')

        if "GLUE2EndpointHealthState" in ldap_ee:
            grid_resource_endpoint.health_state = ldap_ee["GLUE2EndpointHealthState"][0].decode('utf-8')


        grid_resource_endpoint.save()

    print('running periodic task')
