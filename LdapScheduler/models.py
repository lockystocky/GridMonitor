from django.db import models

# Create your models here.


class GridResourceEndpoint (models.Model):
    endpoint_id = models.CharField(max_length=200)
    endpoint_url = models.CharField(max_length=200)
    endpoint_interface_name = models.CharField(max_length=200)
    running_jobs_count = models.IntegerField(default=0)
    total_jobs_count = models.IntegerField(default=0)
    waiting_jobs_count = models.IntegerField(default=0)
    staging_jobs_count = models.IntegerField(default=0)
    suspended_jobs_count = models.IntegerField(default=0)
    quality_level = models.CharField(max_length=200)
    health_state = models.CharField(max_length=200)
    record_time = models.DateTimeField()

    def __str__(self):
        return 'id: %s time: %s endpointId: %s endpointUrl: %s interfaceName: %s runningJobsCount: %s totalJobsCount: %s waitingJobsCount: %s stagingJobsCount: %s suspendedJobsCount: %s qualityLevel: %s healthState: %s'% (self.id, self.record_time, self.endpoint_id, self.endpoint_url, self.endpoint_interface_name, self.running_jobs_count, self.total_jobs_count, self.waiting_jobs_count, self.staging_jobs_count, self.suspended_jobs_count, self.quality_level, self.health_state)


