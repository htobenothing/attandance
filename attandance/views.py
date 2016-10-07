from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.views import generic
from datetime import datetime,timedelta
# Create your views here.
from .models import Member,AttendanceHistory
from django.core.mail import send_mail
from django.conf import settings
from collections import defaultdict


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
        lordsTable = req.POST.get(str(member.Member_ID)+'LT', '')
        prayerMeeting = req.POST.get(str(member.Member_ID)+'PM', '')
        morningRevival = req.POST.get(str(member.Member_ID)+'LT', '')
        bibleReading = req.POST.get(str(member.Member_ID)+'BR', '')
        smallGroup = req.POST.get(str(member.Member_ID)+'SG', '')
        childrenNum = req.POST.get(str('childrenNum'), '')
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
        ['htobenothing@gmail.com'],
        fail_silently=False
    )