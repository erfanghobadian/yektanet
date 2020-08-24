from rest_framework import serializers
from .models import Work, WorkSubmit
from User.serializers import CompanySerializer, PersonSerializer


class WorkSerializer(serializers.ModelSerializer):
    company = serializers.SerializerMethodField()

    class Meta:
        model = Work
        fields = ('id', 'title', 'image', 'expire_date', 'salary', 'hours', 'fields', 'company')

    def create(self, validated_data):
        work, created = Work.objects.update_or_create(company=self.context['request'].user.companyprofile,
                                                      title=validated_data.get('title'),
                                                      image=validated_data.get('image'),
                                                      expire_date=validated_data.get('expire_date'),
                                                      salary=validated_data.get('salary'),
                                                      hours=validated_data.get('hours'),
                                                      fields=validated_data.get('fields'))
        return work

    def get_company(self, obj):
        comp = CompanySerializer(obj.company).data
        comp.pop('user')
        return comp


class WorkSubmitSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkSubmit
        fields = ('work',)


class ApplicationSerializer(serializers.ModelSerializer):
    work = serializers.SerializerMethodField(read_only=True)
    person = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = WorkSubmit
        fields = ('work', 'person')

    def get_person(self, obj):
        person = PersonSerializer(obj.person).data
        person.pop('user')
        return person

    def get_work(self, obj):
        work = WorkSerializer(obj.work).data
        work.pop('company')
        return work
