import json
from datetime import datetime
from django.utils import timezone
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework.exceptions import MethodNotAllowed
from api.models import Job, process_job


class JobSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    url = serializers.URLField()
    result = serializers.CharField(read_only=True)
    status = serializers.CharField(read_only=True)
    time_created = serializers.DateTimeField(read_only=True)
    time_updated = serializers.DateTimeField(read_only=True)

    def create(self, validated_data):
        latest_same_url_job = Job.objects.filter(url=validated_data['url']).order_by('-time_created').first()
        if latest_same_url_job:
            dur = (datetime.now(tz=timezone.utc) - latest_same_url_job.time_created).total_seconds()
            if dur / (60**2) < 1:
                raise serializers.ValidationError(detail=f'Request to {validated_data["url"]} has been submitted within the last hour')

        job = Job.objects.create(
            status=Job.STATUS.QUEUED,
            **validated_data
        )
        process_job(job.id)
        return job

    def update(self, instance, validated_data):
        pass


class JobViewSet(ModelViewSet):
    queryset = Job.objects.all()
    serializer_class = JobSerializer

    def create(self, request, *args, **kwargs):
        if isinstance(request.data, str):
            data = json.loads(request.data)
        else:
            data = request.data
        serializer = JobSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        obj = serializer.create(serializer.validated_data)
        output_serializer = JobSerializer(obj)
        return Response(output_serializer.data)

    def list(self, request, *args, **kwargs):
        url_filter = request.GET.get('url')
        latest = request.GET.get('latest')
        status = request.GET.getlist('status')

        filter_args = {}
        if url_filter:
            filter_args['url'] = url_filter
        if status:
            filter_args['status'] = status

        if latest:
            jobs = [Job.objects.filter(**filter_args).order_by('-time_created').first()]
        else:
            jobs = Job.objects.filter(**filter_args)

        serializer = JobSerializer(jobs, many=True)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        raise MethodNotAllowed

    def partial_update(self, request, *args, **kwargs):
        raise MethodNotAllowed
