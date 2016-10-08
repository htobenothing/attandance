from rest_framework import serializers
from attandance.models import AttendanceHistory, Member,MemberType
from django.contrib.auth.models import User, Group

class MemberSerializer(serializers.ModelSerializer):


    # # define the field need to be serialize
    # Member_ID = serializers.IntegerField(read_only=True)
    # Name = serializers.CharField(required=True,max_length=50)
    # Member_Type = serializers.ChoiceField(choices=MemberType,default='5')
    # Contact = serializers.CharField(max_length=50)
    # Create_Date = serializers.DateTimeField(read_only=True)
    # Status = serializers.BooleanField(default=True)

    # ModelSerializer is the shortcut of making fields serializer by ourself
    # logic about the serializer/deserializer:
    # 1. serialize the model instance, then JsonRender to translate into python native datatype:json.
    # 2. convert json to instance, use BytesIO,JsonParser and serialzer to convert to a object instance

    class Meta:
        model = Member
        fields = ('Member_ID', 'Name', 'Member_Type', 'Contact', 'Status')


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

        instance.Member_ID = validated_data.get('Member_ID',instance.Member_ID)
        instance.Name = validated_data.get('Name',instance.Name)
        instance.Member_Type = validated_data.get('Member_Type',instance.Member_Type)
        instance.Contact = validated_data.get('Contact',instance.Contact)
        instance.Status = validated_data.get('Status',instance.Status)
        instance.save()
        return instance

class UserSerialzer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        field = ('url','username','email','groups')

class GroupSersialzer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ('url','name')