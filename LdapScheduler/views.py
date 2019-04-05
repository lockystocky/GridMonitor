# Create your views here.

from django.shortcuts import render
from django.views.generic.base import View
import rrdtool


class Home(View):
    def get(self, request, *args, **kwargs):
        rrdtool.graph('my.png',
                      '--imgformat', 'PNG',
                      '--width', '540',
                      '--height', '100',
                      '--start', "-14400",
                      '--end', "now",
                      '--vertical-label', 'Running jobs',
                      '--title', 'Running jobs',
                      '--lower-limit', '0',
                      'DEF:running_jobs=org.nordugrid.gridftpjob_running_jobs_count_my.rrd:running_jobs:AVERAGE',
                      'AREA:running_jobs#990033:Running jobs')
        return render(request, "index.html")
