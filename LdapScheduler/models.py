from django.db import models

# Create your models here.


class ComputingService(models.Model):
    service_id = models.CharField(max_length=200)


class GridResourceEndpoint (models.Model):
    endpoint_id = models.CharField(max_length=200, primary_key=True)
    computing_service_id = models.CharField(max_length=200, default="")
    endpoint_url = models.CharField(max_length=200)
    endpoint_interface_name = models.CharField(max_length=200)
    running_jobs_count = models.IntegerField(default=0)
    total_jobs_count = models.IntegerField(default=0)
    waiting_jobs_count = models.IntegerField(default=0)
    staging_jobs_count = models.IntegerField(default=0)
    suspended_jobs_count = models.IntegerField(default=0)
    quality_level = models.CharField(max_length=200)
    health_state = models.CharField(max_length=200)
    record_time = models.DateTimeField(null=True)

    def __str__(self):
        return 'id: %s time: %s endpointId: %s endpointUrl: %s interfaceName: %s runningJobsCount: %s totalJobsCount: %s waitingJobsCount: %s stagingJobsCount: %s suspendedJobsCount: %s qualityLevel: %s healthState: %s'% (self.id, self.record_time, self.endpoint_id, self.endpoint_url, self.endpoint_interface_name, self.running_jobs_count, self.total_jobs_count, self.waiting_jobs_count, self.staging_jobs_count, self.suspended_jobs_count, self.quality_level, self.health_state)


class ComputingManager(models.Model):
    manager_id = models.CharField(max_length=200, primary_key=True)
    computing_service_id = models.CharField(max_length=200, default="")
    total_slots_count = models.IntegerField(default=0)
    slots_used_by_local_jobs_count = models.IntegerField(default=0)
    slots_used_by_grid_jobs_count = models.IntegerField(default=0)


class ExecutionEnvironment(models.Model):
    resource_id = models.CharField(max_length=200, primary_key=True)
    computing_manager_id = models.CharField(max_length=200, default="")
    main_memory_size = models.IntegerField(default=0)
    os_family = models.CharField(max_length=200, default="")
    platform = models.CharField(max_length=200, default="")
    cpu_clock_speed = models.IntegerField(default=0)
    cpu_model = models.CharField(max_length=200, default="")
    logical_cpus_count = models.IntegerField(default=0)
    virtual_memory_size = models.IntegerField(default=0)
    entryUUID = models.CharField(max_length=200, default="")
    entity_name = models.CharField(max_length=200, default="")


class ComputingShareEndpoint(models.Model):
    computing_share_id = models.CharField(max_length=200, default="")
    computing_endpoint_id = models.CharField(max_length=200, default="")


class ComputingShareExecutionEnvironment(models.Model):
    share_id = models.CharField(max_length=200, default="")
    environment_id = models.CharField(max_length=200, default="")


class ComputingShare(models.Model):
    share_id = models.CharField(max_length=200, primary_key=True)
    max_cpu_time = models.IntegerField(default=0)
    max_running_jobs = models.IntegerField(default=0)
    max_total_jobs = models.IntegerField(default=0)
    max_virtual_memory = models.IntegerField(default=0)









