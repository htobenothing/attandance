from django.shortcuts import render
from datetime import datetime, timedelta
from collections import defaultdict

from django.views.decorators.csrf import csrf_exempt
from django.core.mail import send_mail
from django.contrib.auth.models import User, Group

from rest_framework import viewsets,status
from rest_framework import generics
from rest_framework import permissions
from rest_framework.decorators import api_view, detail_route, list_route
from rest_framework.response import Response
from rest_framework.reverse import reverse

from attandance.serializers import UserSerialzer, GroupSerializer, MemberSerializer, AttandanceHistorySerializer
from attandance.serializers import AccountSerializer
from attandance.models import Member, AttendanceHistory,Account
from attandance.permissions import IsOwnerOrReadOnly

# Create your views here.


def create(req):
    allMember = Member.objects.all()
    content = {"allMember": allMember}
    return render(req, 'attandance/create.html', content)


def detail(req, member_id):
    historys = AttendanceHistory.objects.filter(Member_ID=member_id)
    data = {"attandHistory": historys}
    return render(req, "attandance/detail", data)


def saveAll(req):
    allMember = Member.objects.all()

    for member in allMember:
        # memberID = req.POST.get(member.Member_ID,'')
        lordsTable = req.POST.get(str(member.Member_ID) + 'LT', False)
        prayerMeeting = req.POST.get(str(member.Member_ID) + 'PM', False)
        morningRevival = req.POST.get(str(member.Member_ID) + 'LT', False)
        bibleReading = req.POST.get(str(member.Member_ID) + 'BR', False)
        smallGroup = req.POST.get(str(member.Member_ID) + 'SG', False)
        childrenNum = req.POST.get(str('childrenNum'), False)
        history = AttendanceHistory(Member_ID=member,
                                    Lords_Table=lordsTable,
                                    Prayer_Meeting=prayerMeeting,
                                    Morning_Revival=morningRevival,
                                    Bible_Reading=bibleReading,
                                    Small_Group=smallGroup)
        history.save()
    # sendEmailToChurchOffice(childrenNum)

    return render(req, "attandance/success.html", {"status": "success"})


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
                    Summary[attr] += 1
    Summary['Children'] = childrenNum
    return Summary


def sendEmailToChurchOffice(req):
    today = datetime.today()
    start = today - timedelta(days=today.weekday())
    end = start + timedelta(days=6)
    Summary = getWeeklyInfor(req.POST.get('childrenNum',' '))
    send_mail(
        'Weekly Statistic Report for CommonWealth {0} - {1}' \
            .format(start.date().strftime('%d/%m/%Y'), end.date().strftime('%d/%m/%Y')),
        """ Dear Church Office,
        Here is the Statistic for Commonwealth District:
        Lords Table:{0}
        Prayer Meeting:{1}
        Morning Revival:{2}
        Bible Reading:{3}
        Small Group:{4}
        children:{5}
        """.format(Summary['Lords_Table'], Summary['Prayer_Meeting'],
                   Summary['Morning_Revival'], Summary['Bible_Reading'],
                   Summary['Small_Group'], Summary['Children']),
        'htobenothingtest@gmail.com',
        ['htobenothingtest@gmail.com'],
        fail_silently=False
    )
    return Response(template_name="attandance/success.html",status=200)


# class UserViewSet(viewsets.ModelViewSet):
#     """
#     API endpoint allow users to be view and edited
#     """
#     queryset = User.objects.all()
#     serializer_class = UserSerialzer


class GroupViewset(viewsets.ModelViewSet):
    """
    API endpoint allow groups to be view and edited
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


# use @api_view of APIView to replace the JSONResponse
# class JSONResponse(HttpResponse):
#     """
#     An HttpResponse that renders content into Json
#     """
#     def __init__(self, data, **kwargs):
#         content = JSONRenderer().render(data)
#         kwargs['content_type'] = 'application/json'
#         super(JSONResponse,self).__init__(content, **kwargs)

class MemberViewSet(viewsets.ModelViewSet):
    serializer_class = MemberSerializer
    queryset = Member.objects.all()


class AttandanceHistory(viewsets.ModelViewSet):
    serializer_class = AttandanceHistorySerializer
    queryset = AttendanceHistory.objects.all()


class MemberList(generics.ListCreateAPIView):
    """
    lsit out all members, or create new member
    """
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    queryset = Member.objects.all()
    serializer_class = MemberSerializer


class MemberDetail(generics.RetrieveUpdateAPIView):
    """
    Retieve, update a member
    """
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    queryset = Member.objects.all()
    serializer_class = MemberSerializer


class AttandanceHistoryList(generics.ListCreateAPIView):
    """
    list out all history, or create new history
    """
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    queryset = AttendanceHistory.objects.all()
    serializer_class = AttandanceHistorySerializer


class AttandanceHistoryDetail(generics.RetrieveUpdateAPIView):
    """
    Retrieve and update the specific attandance History
    """
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    queryset = AttendanceHistory.objects.all()
    serializer_class = AttandanceHistorySerializer


class AccountViewSet(viewsets.ModelViewSet):
    # lookup_field, use the specific field to find the 'Account' instance
    lookup_field = 'name'
    queryset = Account.objects.all()
    serializer_class = AccountSerializer

    def get_permissions(self):
        if self.request.method in permissions.SAFE_METHODS:
            return (permissions.AllowAny(),)

        if self.request.method == 'POST':
            return (permissions.AllowAny())

    # overwrite the create function, so that use create_user function to create Account
    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data = request.data)

        if serializer.is_valid():
            Account.objects.create_user(**serializer.validated_data)

            return Response(serializer.validated_data,status=status.HTTP_201_CREATED)

        return Response({
            'status':'Bad Request',
            'message':'Have some invalidate data, please check'
        },status=status.HTTP_400_BAD_REQUEST)

from django.views.generic.base import TemplateView


class IndexView(TemplateView):
    template_name = 'attandance/index.html'


class LoginView(TemplateView):
    template_name = 'attandance/login.html'


class LogoutView(TemplateView):
    template_name = 'attandance/login.html'