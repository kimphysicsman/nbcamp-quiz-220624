from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import permissions, status
from .models import (
    JobPostSkillSet,
    JobType,
    JobPost,
    Company,
    SkillSet
)
from django.db.models.query_utils import Q
from .serializers import JobPostSerializer, CompanySerializer, JobTypeSerializer


class SkillView(APIView):

    permission_classes = [permissions.AllowAny]

    def get(self, request):
        skills = self.request.query_params.getlist('skills', '')
       
        query = Q()
        for skill in skills:
            skill_set = SkillSet.objects.get(name=skill)
            query |= Q(skill_set=skill_set)
        job_post_skill_sets = JobPostSkillSet.objects.filter(query)
        job_posts = [job_post_skill_set.job_post for job_post_skill_set in job_post_skill_sets]

        return Response(JobPostSerializer(job_posts, many=True).data, status=status.HTTP_200_OK)


class JobView(APIView):

    def post(self, request):
        job_type = int( request.data.get("job_type", None) )
        company_name = request.data.get("company_name", None)

        try:
            job_type = JobType.objects.get(id=job_type)
        except:
            return Response({'message': '해당 job_type 이 없습니다!'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            company = Company.objects.get(company_name=company_name)
        except:
            company = Company.objects.create(company_name=company_name)
            company.save()
        
        request.data['company'] = CompanySerializer(company).data
        request.data['job_type'] = JobTypeSerializer(job_type).data

        job_serializer = JobPostSerializer(data=request.data)
        if job_serializer.is_valid():
            job_serializer.save()
            return Response({'message': '저장 완료!'}, status=status.HTTP_200_OK)

        return Response(job_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

