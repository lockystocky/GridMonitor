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
    total_jobs_name = endpoint.base64id + '_total_jobs_count.rrd'
    total_jobs_path = endpoint.base64id + '_total_jobs_count' + str(datetime.datetime.now().date()) + '.png'

    try:
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
    except:
        total_jobs_path = ""


    running_jobs_name = endpoint.base64id + '_running_jobs_count.rrd'
    running_jobs_path = endpoint.base64id + '_running_jobs_count' + str(
        datetime.datetime.now().date()) + '.png'

    try:
        rrdtool.graph('practice_work/files/static/' + running_jobs_path,
                      '--imgformat', 'PNG',
                      '--width', '540',
                      '--height', '100',
                      '--start', "-14400",
                      '--end', "now",
                      '--vertical-label', 'Running jobs',
                      '--title', 'Running jobs',
                      '--lower-limit', '0',
                      'DEF:running_jobs=' + running_jobs_name + ':running_jobs:AVERAGE',
                      'AREA:running_jobs#990033:Running jobs')
    except:
        running_jobs_path = ""

    waiting_jobs_name = endpoint.base64id + '_waiting_jobs_count.rrd'
    waiting_jobs_path = endpoint.base64id + '_waiting_jobs_count' + str(
        datetime.datetime.now().date()) + '.png'

    try:
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
    except:
        waiting_jobs_path = ""

    staging_jobs_name = endpoint.base64id + '_staging_jobs_count.rrd'
    staging_jobs_path = endpoint.base64id + '_staging_jobs_count' + str(
        datetime.datetime.now().date()) + '.png'
    try:
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
    except:
        staging_jobs_path = ""

    suspended_jobs_name = endpoint.base64id + '_suspended_jobs_count.rrd'
    suspended_jobs_path = endpoint.base64id + '_suspended_jobs_count' + str(
        datetime.datetime.now().date()) + '.png'
    try:
        rrdtool.graph('practice_work/files/static/' + suspended_jobs_path,
                      '--imgformat', 'PNG',
                      '--width', '540',
                      '--height', '100',
                      '--start', "-14400",
                      '--end', "now",
                      '--vertical-label', 'Suspended jobs',
                      '--title', 'Suspended jobs',
                      '--lower-limit', '0',
                      'DEF:suspended_jobs=' + suspended_jobs_name + ':suspended_jobs:AVERAGE',
                      'AREA:suspended_jobs#990033:Suspended jobs')
    except:
        suspended_jobs_path = ""

    return render(request, "interface.html", {'total_jobs_path': total_jobs_path, 'running_jobs_path': running_jobs_path,
                                              'waiting_jobs_path': waiting_jobs_path, 'staging_jobs_path': staging_jobs_path,
                                              'suspended_jobs_path': suspended_jobs_path})


def interfaceinfo(request, name=None):
    endpoint = GridResourceEndpoint.objects.get(base64id=name)
    shares = ComputingShareEndpoint.objects.filter(computing_endpoint_id=endpoint.endpoint_id)
    total_jobs_name = endpoint.base64id + '_total_jobs_count.rrd'
    total_jobs_path = endpoint.base64id + '_total_jobs_count' + str(datetime.datetime.now().date()) + '.png'

    try:
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
    except:
        total_jobs_path = ""

    running_jobs_name = endpoint.base64id + '_running_jobs_count.rrd'
    running_jobs_path = endpoint.base64id + '_running_jobs_count' + str(
        datetime.datetime.now().date()) + '.png'

    try:
        rrdtool.graph('practice_work/files/static/' + running_jobs_path,
                      '--imgformat', 'PNG',
                      '--width', '540',
                      '--height', '100',
                      '--start', "-14400",
                      '--end', "now",
                      '--vertical-label', 'Running jobs',
                      '--title', 'Running jobs',
                      '--lower-limit', '0',
                      'DEF:running_jobs=' + running_jobs_name + ':running_jobs:AVERAGE',
                      'AREA:running_jobs#990033:Running jobs')
    except:
        running_jobs_path = ""

    waiting_jobs_name = endpoint.base64id + '_waiting_jobs_count.rrd'
    waiting_jobs_path = endpoint.base64id + '_waiting_jobs_count' + str(
        datetime.datetime.now().date()) + '.png'

    try:
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
    except:
        waiting_jobs_path = ""

    staging_jobs_name = endpoint.base64id + '_staging_jobs_count.rrd'
    staging_jobs_path = endpoint.base64id + '_staging_jobs_count' + str(
        datetime.datetime.now().date()) + '.png'
    try:
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
    except:
        staging_jobs_path = ""

    suspended_jobs_name = endpoint.base64id + '_suspended_jobs_count.rrd'
    suspended_jobs_path = endpoint.base64id + '_suspended_jobs_count' + str(
        datetime.datetime.now().date()) + '.png'
    try:
        rrdtool.graph('practice_work/files/static/' + suspended_jobs_path,
                      '--imgformat', 'PNG',
                      '--width', '540',
                      '--height', '100',
                      '--start', "-14400",
                      '--end', "now",
                      '--vertical-label', 'Suspended jobs',
                      '--title', 'Suspended jobs',
                      '--lower-limit', '0',
                      'DEF:suspended_jobs=' + suspended_jobs_name + ':suspended_jobs:AVERAGE',
                      'AREA:suspended_jobs#990033:Suspended jobs')
    except:
        suspended_jobs_path = ""

    return render(request, "interfaceinfo.html",
                  {'total_jobs_path': total_jobs_path, 'running_jobs_path': running_jobs_path,
                   'waiting_jobs_path': waiting_jobs_path, 'staging_jobs_path': staging_jobs_path,
                   'suspended_jobs_path': suspended_jobs_path, 'endpoint': endpoint, 'shares': shares})


def computingshare(request, name=None):
    print('NAME: ' + name)
    share = ComputingShare.objects.get(share_id=name)
    print('SHARE_ID: ' + share.share_id)
    print('SHARE_BASE64_ID: ' + share.base64id)
    environments = ComputingShareExecutionEnvironment.objects.filter(share_id=name)

    total_jobs_name = share.base64id + '_total_jobs.rrd'
    total_jobs_path = share.base64id + '_total_jobs' + str(datetime.datetime.now().date()) + '.png'
    print('total_jobs_name: ' + total_jobs_name)

    rrdtool.graph('practice_work/files/static/' + total_jobs_path,
                  '--imgformat', 'PNG',
                  '--width', '540',
                  '--height', '100',
                  '--start', "-14400",
                  '--end', "now",
                  '--vertical-label', 'Total jobs',
                  '--title', 'Total jobs',
                  '--lower-limit', '0',
                  'DEF:tot_jobs=' + total_jobs_name + ':tot_jobs:AVERAGE',
                  'AREA:tot_jobs#990033:Total jobs')

    waiting_jobs_name = share.base64id + '_waiting_jobs.rrd'
    waiting_jobs_path = share.base64id + '_waiting_jobs' + str(datetime.datetime.now().date()) + '.png'

    try:
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
    except:
        waiting_jobs_path = ""

    running_jobs_name = share.base64id + '_running_jobs.rrd'
    running_jobs_path = share.base64id + '_running_jobs' + str(datetime.datetime.now().date()) + '.png'

    try:
        rrdtool.graph('practice_work/files/static/' + running_jobs_path,
                      '--imgformat', 'PNG',
                      '--width', '540',
                      '--height', '100',
                      '--start', "-14400",
                      '--end', "now",
                      '--vertical-label', 'Running jobs',
                      '--title', 'Running jobs',
                      '--lower-limit', '0',
                      'DEF:running_jobs=' + running_jobs_name + ':running_jobs:AVERAGE',
                      'AREA:running_jobs#990033:Total jobs')
    except:
        running_jobs_path = ""

    return render(request, "computingshare.html",
                  {'share': share, 'environments': environments,
                   'total_jobs_path': total_jobs_path,
                   'running_jobs_path': running_jobs_path,
                   'waiting_jobs_path': waiting_jobs_path})


def environment(request, name=None):
    print(name)
    environment = ExecutionEnvironment.objects.get(resource_id=name)

    used_instances_name = environment.base64id + '_used_instances.rrd'
    used_instances_path = environment.base64id + '_used_instances' + str(datetime.datetime.now().date()) + '.png'

    try:
        rrdtool.graph('practice_work/files/static/' + used_instances_path,
                      '--imgformat', 'PNG',
                      '--width', '540',
                      '--height', '100',
                      '--start', "-14400",
                      '--end', "now",
                      '--vertical-label', 'Used instances',
                      '--title', 'Used instances',
                      '--lower-limit', '0',
                      'DEF:used_instances=' + used_instances_name + ':used_instances:AVERAGE',
                      'AREA:used_instances#990033:Total jobs')
    except:
        used_instances_path = ""

    unavail_instances_name = environment.base64id + '_unavailable_instances.rrd'
    unavail_instances_path = environment.base64id + '_unavailable_instances' + str(datetime.datetime.now().date()) + '.png'

    try:
        rrdtool.graph('practice_work/files/static/' + unavail_instances_path,
                      '--imgformat', 'PNG',
                      '--width', '540',
                      '--height', '100',
                      '--start', "-14400",
                      '--end', "now",
                      '--vertical-label', 'Unavailable instances',
                      '--title', 'Unavailable instances',
                      '--lower-limit', '0',
                      'DEF:unavail_inst=' + unavail_instances_name + ':unavail_inst:AVERAGE',
                      'AREA:unavail_inst#990033:Unavailable instances')
    except:
        unavail_instances_path = ""

    total_instances_name = environment.base64id + '_total_instances.rrd'
    total_instances_path = environment.base64id + '_total_instances' + str(
        datetime.datetime.now().date()) + '.png'

    try:
        rrdtool.graph('practice_work/files/static/' + total_instances_path,
                      '--imgformat', 'PNG',
                      '--width', '540',
                      '--height', '100',
                      '--start', "-14400",
                      '--end', "now",
                      '--vertical-label', 'Total instances',
                      '--title', 'Total instances',
                      '--lower-limit', '0',
                      'DEF:total_instances=' + total_instances_name + ':total_instances:AVERAGE',
                      'AREA:total_instances#990033:Total instances')
    except:
        total_instances_path = ""

    return render(request, "environment.html",
                  {'environment': environment,
                   'total_instances_path': total_instances_path,
                   'unavail_instances_path': unavail_instances_path,
                   'used_instances_path': used_instances_path})


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

