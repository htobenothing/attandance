from rest_framework import serializers
from attandance.models import AttendanceHistory, Member,MemberType,Account
from django.contrib.auth.models import User, Group
from django.contrib.auth import update_session_auth_hash



class MemberSerializer(serializers.ModelSerializer):

    # ModelSerializer is the shortcut of making fields serializer by ourself
    # logic about the serializer/deserializer:
    # 1. serialize the model instance, then JsonRender to translate into python native datatype:json.
    # 2. convert json to instance, use BytesIO,JsonParser and serialzer to convert to a object instance
    AttandanceHistorys = serializers.PrimaryKeyRelatedField(
        many=True, queryset=AttendanceHistory.objects.all()
    )

    class Meta:
        model = Member
        fields = ('Member_ID', 'Name', 'Member_Type','District_ID','Email', 'Phone', 'Status', 'AttandanceHistorys')

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


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ('url','name')


class AttandanceHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = AttendanceHistory
        field = ('History_ID','Member_ID','Create_Date',
                 'Lords_Table','Prayer_Meeting','Morning_Revival'
                 'Bible_Reading','Small_Group')

    def create(self, validatedData):
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

        instance.History_ID = validated_data.get('History_ID',instance.History_ID)
        instance.Member_ID = validated_data.get('Member_ID',instance.Member_ID)
        instance.Lords_Table = validated_data.get('Lords_Table',instance.Lords_Table)
        instance.Prayer_Meeting = validated_data.get('Prayer_Meeting',instance.Prayer_Meeting)
        instance.Morning_Revival = validated_data.get('Morning_Revival',instance.Morning_Revival)
        instance.Bible_Reading = validated_data.get('Bible_Reading', instance.Bible_Reading)
        instance.Small_Group = validated_data.get('Small_Group', instance.Small_Group)
        instance.save()
        return instance


class AccountSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True,required=False)
    confirm_password = serializers.CharField(write_only=True,required=False)

    class Meta:
        model = Account
        fields=('id', 'email', 'username', 'created_at', 'updated_at',
                  'first_name', 'last_name', 'tagline', 'password',
                  'confirm_password',)
        read_only_fields = ('create_at','update_at')

        def create(self,validate_data):
            return Account.objects.create(**validate_data)

        def update(self,instance,validate_data):
            instance.username = validate_data.get('username',instance.username)
            instance.tagline = validate_data.get('tagline',instance.tagline)

            instance.save()

            password = validate_data.get('password', None)
            confirm_password = validate_data.get('confirm_password', None)

            if password and confirm_password and password == confirm_password:
                # set_password help to store password security
                instance.set_password(password)
                instance.save()
            update_session_auth_hash(self.context.get('request'),instance)