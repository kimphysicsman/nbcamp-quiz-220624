from rest_framework import serializers
from .models import Company, BusinessArea, JobPost, JobType, SkillSet, JobPostSkillSet


class BusinessAreaSerializer(serializers.ModelSerializer):
    class Meta:
        model = BusinessArea
        fields = ['area']


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ['company_name']

class JobTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobType
        fields = ['job_type']

class JobPostSerializer(serializers.ModelSerializer):
    job_type = JobTypeSerializer()
    company = CompanySerializer()
    skillsets = serializers.SerializerMethodField()

    def get_skillsets(self, obj):
        skillsets = obj.skillset_set.all()
        name_list = [skillset.name for skillset in skillsets]
        return name_list

    class Meta:
        model = JobPost
        fields = ['id', 'job_type', 'company', 'job_description', 'salary', 'skillsets']

    def create(self, validated_data):
        company = validated_data.pop('company')
        company = Company.objects.get(company_name=company['company_name'])

        job_type = validated_data.pop('job_type')
        job_type = JobType.objects.get(job_type=job_type['job_type'])

        job_post = JobPost.objects.create(company=company, job_type=job_type, **validated_data)
        job_post.save()

        return job_post


class SkillSetSerializer(serializers.ModelSerializer):
    job_posts = JobPostSerializer(many=True)
    class Meta:
        model = SkillSet
        fields = ['name' ,'job_posts']

class JobPostSkillSetSerializer(serializers.ModelSerializer):
    job_posts = JobPostSerializer()
    skill_set = SkillSetSerializer()
    class Meta:
        model = SkillSet
        fields = ['skill_set' ,'job_posts']
