# Create your views here.

from django.shortcuts import render
from django.views.generic.base import View
import rrdtool
from LdapScheduler.models import GridResourceEndpoint
from LdapScheduler.models import ComputingShareEndpoint
from LdapScheduler.models import ComputingShare
from LdapScheduler.models import ComputingShareExecutionEnvironment
from LdapScheduler.models import ExecutionEnvironment
import tempfile
import datetime
import urllib.parse


def interface(request, name=None):
    endpoint = GridResourceEndpoint.objects.get(endpoint_interface_name=name)
    total_jobs_name = endpoint.endpoint_interface_name + '_total_jobs_count_my.rrd'
    total_jobs_path = endpoint.endpoint_interface_name + '_total_jobs_count' + str(datetime.datetime.now().date()) + '.png'

    rrdtool.graph('practice_work/files/static/' + total_jobs_path,
                  '--imgformat', 'PNG',
                  '--width', '540',
                  '--height', '100',
                  '--start', "-14400",
                  '--end', "now",
                  '--vertical-label', 'Total jobs',
                  '--title', 'Total jobs',
                  '--lower-limit', '0',
                  'DEF:total_jobs=' + total_jobs_name + ':total_jobs:AVERAGE',
                  'AREA:total_jobs#990033:Total jobs')

    running_jobs_name = endpoint.endpoint_interface_name + '_running_jobs_count_my.rrd'
    running_jobs_path = endpoint.endpoint_interface_name + '_running_jobs_count' + str(
        datetime.datetime.now().date()) + '.png'

    rrdtool.graph('practice_work/files/static/' + running_jobs_path,
                  '--imgformat', 'PNG',
                  '--width', '540',
                  '--height', '100',
                  '--start', "-14400",
                  '--end', "now",
                  '--vertical-label', 'Runningjobs',
                  '--title', 'Running jobs',
                  '--lower-limit', '0',
                  'DEF:running_jobs=' + running_jobs_name + ':running_jobs:AVERAGE',
                  'AREA:running_jobs#990033:Running jobs')

    waiting_jobs_name = endpoint.endpoint_interface_name + '_waiting_jobs_count_my.rrd'
    waiting_jobs_path = endpoint.endpoint_interface_name + '_waiting_jobs_count' + str(
        datetime.datetime.now().date()) + '.png'

    rrdtool.graph('practice_work/files/static/' + waiting_jobs_path,
                  '--imgformat', 'PNG',
                  '--width', '540',
                  '--height', '100',
                  '--start', "-14400",
                  '--end', "now",
                  '--vertical-label', 'Waiting jobs',
                  '--title', 'Waiting jobs',
                  '--lower-limit', '0',
                  'DEF:waiting_jobs=' + waiting_jobs_name + ':waiting_jobs:AVERAGE',
                  'AREA:waiting_jobs#990033:Waiting jobs')

    staging_jobs_name = endpoint.endpoint_interface_name + '_staging_jobs_count_my.rrd'
    staging_jobs_path = endpoint.endpoint_interface_name + '_staging_jobs_count' + str(
        datetime.datetime.now().date()) + '.png'

    rrdtool.graph('practice_work/files/static/' + staging_jobs_path,
                  '--imgformat', 'PNG',
                  '--width', '540',
                  '--height', '100',
                  '--start', "-14400",
                  '--end', "now",
                  '--vertical-label', 'Staging jobs',
                  '--title', 'Staging jobs',
                  '--lower-limit', '0',
                  'DEF:staging_jobs=' + staging_jobs_name + ':staging_jobs:AVERAGE',
                  'AREA:staging_jobs#990033:Staging jobs')

    return render(request, "interface.html", {'total_jobs_path': total_jobs_path, 'running_jobs_path': running_jobs_path,
                                              'waiting_jobs_path': waiting_jobs_path, 'staging_jobs_path': staging_jobs_path})


def interfaceinfo(request, name=None):
    endpoint = GridResourceEndpoint.objects.get(endpoint_interface_name=name)
    shares = ComputingShareEndpoint.objects.filter(computing_endpoint_id=endpoint.endpoint_id)
    return render(request, "interfaceinfo.html", {'interface': endpoint, 'shares': shares})


def computingshare(request, name=None):
    share = ComputingShare.objects.get(share_id=name)
    environments = ComputingShareExecutionEnvironment.objects.filter(share_id=name)
    return render(request, "computingshare.html", {'share': share, 'environments': environments})


def environment(request, name=None):
    print(name)
    environment = ExecutionEnvironment.objects.get(resource_id=name)
    return render(request, "environment.html", {'environment': environment})


class Home(View):
    def get(self, request, *args, **kwargs):
        endpoints = GridResourceEndpoint.objects.all()
        '''
        rrdtool.graph('my.png',
                      '--imgformat', 'PNG',
                      '--width', '540',
                      '--height', '100',
                      '--start', "-14400",
                      '--end', "now",
                      '--vertical-label', 'Running jobs',
                      '--title', 'Running jobs',
                      '--lower-limit', '0',
                      'DEF:total_jobs=org.nordugrid.gridftpjob_total_jobs_count_my.rrd:total_jobs:AVERAGE',
                      'AREA:total_jobs#990033:Running jobs')
                      '''
        return render(request, "index.html", {'endpoints': endpoints})


class Interface(View):
    def get(self, request, name):
        endpoint = GridResourceEndpoint.objects.get(interface_name=name)
        name = endpoint.endpoint_interface_name + '_total_jobs_count_my.rrd'
        fd, path = tempfile.mkstemp('.png')
        rrdtool.graph(path,
                      '--imgformat', 'PNG',
                      '--width', '540',
                      '--height', '100',
                      '--start', "-14400",
                      '--end', "now",
                      '--vertical-label', 'Total jobs',
                      '--title', 'Total jobs',
                      '--lower-limit', '0',
                      'DEF:total_jobs=' + name + ':total_jobs:AVERAGE',
                      'AREA:total_jobs#990033:Running jobs')


        return render(request, "interface.html", {'path': path})

