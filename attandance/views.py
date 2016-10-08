from django.shortcuts import render
from datetime import datetime,timedelta
from collections import defaultdict

from django.views.decorators.csrf import csrf_exempt
from django.core.mail import send_mail
from django.contrib.auth.models import User,Group

from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.views import APIView

from attandance.serializers import UserSerialzer,GroupSersialzer,MemberSerializer
from attandance.models import Member,AttendanceHistory

# Create your views here.

def create(req):
    allMember = Member.objects.all()
    content = {"allMember":allMember}
    return render(req, 'attandance/create.html', content)


def detail(req,member_id):
    historys = AttendanceHistory.objects.filter(Member_ID = member_id)
    data = {"attandHistory":historys}
    return render(req,"attandance/detail",data)


def saveAll(req):
    allMember = Member.objects.all()

    for member in allMember:
        # memberID = req.POST.get(member.Member_ID,'')
        lordsTable = req.POST.get(str(member.Member_ID)+'LT', False)
        prayerMeeting = req.POST.get(str(member.Member_ID)+'PM', False)
        morningRevival = req.POST.get(str(member.Member_ID)+'LT', False)
        bibleReading = req.POST.get(str(member.Member_ID)+'BR', False)
        smallGroup = req.POST.get(str(member.Member_ID)+'SG', False)
        childrenNum = req.POST.get(str('childrenNum'), False)
        history = AttendanceHistory(Member_ID=member,
                                    Lords_Table=lordsTable,
                                    Prayer_Meeting=prayerMeeting,
                                    Morning_Revival=morningRevival,
                                    Bible_Reading=bibleReading,
                                    Small_Group=smallGroup)
        history.save()
    sendEmailToChurchOffice(childrenNum)

    return render(req,"attandance/create.html",{"status":"success"})


def getWeeklyInfor(childrenNum):
    today = datetime.today()
    start = today - timedelta(days=today.weekday())
    end = start + timedelta(days=6)
    weeklyHistory = AttendanceHistory.objects.filter(Create_Date__gt=start, Create_Date__lte=end)
    print(len(weeklyHistory))
    Summary = defaultdict(int)
    if weeklyHistory:
        for history in weeklyHistory:
            for attr in history.__dict__.keys():
                print(attr)
                if history.__dict__.get(attr):
                    Summary[attr] +=1
    Summary['Children'] = childrenNum
    return Summary


def sendEmailToChurchOffice(childrenNum):
    today = datetime.today()
    start = today-timedelta(days=today.weekday())
    end = start+timedelta(days=6)
    Summary =getWeeklyInfor(childrenNum)
    send_mail(
        'Weekly Statistic Report for CommonWealth {0} - {1}'\
            .format(start.date().strftime('%d/%m/%Y'),end.date().strftime('%d/%m/%Y')),
        """ Dear Church Office,
        Here is the Statistic for Commonwealth District:
        Lords Table:{0}
        Prayer Meeting:{1}
        Morning Revival:{2}
        Bible Reading:{3}
        Small Group:{4}
        children:{5}
        """.format(Summary['Lords_Table'],Summary['Prayer_Meeting'],
                   Summary['Morning_Revival'],Summary['Bible_Reading'],
                   Summary['Small_Group'],Summary['Children']),
        'htobenothingtest@gmail.com',
        ['htobenothingtest@gmail.com'],
        fail_silently=False
    )


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint allow users to be view and edited
    """
    queryset = User.objects.all()
    serializer_class = UserSerialzer


class GroupViewset(viewsets.ModelViewSet):
    """
    API endpoint allow groups to be view and edited
    """
    queryset = Group.objects.all()
    serializer_class = GroupSersialzer

# use @api_view of APIView to replace the JSONResponse
# class JSONResponse(HttpResponse):
#     """
#     An HttpResponse that renders content into Json
#     """
#     def __init__(self, data, **kwargs):
#         content = JSONRenderer().render(data)
#         kwargs['content_type'] = 'application/json'
#         super(JSONResponse,self).__init__(content, **kwargs)



# @api_view(['GET','POST'])
@csrf_exempt
class MemberList(APIView):
    """
    lsit out all members, or create new member
    :param request:
    :return:
    """
    def get(self, req, format=None):
        members = Member.objects.all()
        serializer = MemberSerializer(members,many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self,req, format=None):
        serializer = MemberSerializer(data=req.data)
        print(req.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

# @api_view(['GET','PUT'])
@csrf_exempt
class MemberDetail(APIView):
    """
    Retieve, update a member
    """
    def get_object(self,pk):
        try:
            member = Member.objects.get(pk=pk)
        except Member.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def get(self,req,pk,format=None):
        member = self.get_object(pk)
        serializer = MemberSerializer(member)
        return Response(serializer.data,status=status.HTTP_200_OK)

    def put(self,req,pk,format=None):
        member = self.get_object(pk)
        serializer = MemberSerializer(member,req.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

