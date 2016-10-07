from rest_framework import serializers
from attandance.models import AttendanceHistory, Member,MemberType


class MemberSerializer(serializers.Serializer):
    Member_ID = serializers.IntegerField(primary_key=True)
    Name = serializers.CharField(required=True,max_length=50)
    Member_Type = serializers.CharField(max_length=1, choices=MemberType)
    Contact = serializers.CharField(max_length=50)
    Password = serializers.CharField(max_length=255)
    Create_Date = serializers.DateTimeField(auto_now_add=True)
    Status = serializers.BooleanField(default=True)

    def create(self,validatedData):
        """
        Create and return a new Member instance, given the validated data
        :param validatedData:
        :return:'attandance.Member'
        """
        return Member.objects.create(**validatedData)

    def update(self, instance, validated_data):
        """
        update and return an existing 'Member' instance, given the validated data
        :param instance:
        :param validated_data:
        :return:
        """

        instance.Member_ID = validated_data.get('member_id',instance.Member_ID)
        instance.Name = validated_data.get('name',instance.Name)
