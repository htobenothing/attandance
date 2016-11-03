/**
 * Created by nothing on 10/27/16.
 */

function confirmOwnAtten(id) {
    var memberID = id.split("_")[0];
    console.log(memberID);

    var lordsTable = $("#" + memberID + "LT").prop('checked');
    var prayerMeeting = $("#" + memberID + "PM").prop('checked');
    var morningRevival = $("#" + memberID + "MR").prop('checked');
    var bibleReading = $("#" + memberID + "BR").prop('checked');
    var smallGroup = $("#" + memberID + "SG").prop('checked');
    var attandanceHistoryID = $("#"+memberID +"atten");


    var attandacne = {
        "Member_ID": memberID,
        "Lords_Table": lordsTable,
        "Prayer_Meeting": prayerMeeting,
        "Morning_Revival": morningRevival,
        "Bible_Reading": bibleReading,
        "Small_Group": smallGroup
    };

    createAttendance(attandacne);

    $("." + memberID).prop("disabled", true);

}

var attandances = [];

var csrftoken = Cookies.get('csrftoken');

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

function createAttendance(attandance) {
    $.ajaxSetup({
        beforeSend: function (xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });

    $.ajax({
        url: "/api/v1/attandancehistory/",
        type: "POST",
        data: attandance
    }).done(function (data) {
        console.log(data.History_ID)
        var span =document.createElement("span");
        span.prop('hidden',true);
        span.prop('atten',data.Member_ID);
        
        attandances.push(data)
    })
}

function editAtten(id) {
    var memberID = id.split("_")[0];
    $("." + memberID).prop("disabled", false);

    var lordsTable = $("#" + memberID + "LT").prop('checked');
    var prayerMeeting = $("#" + memberID + "PM").prop('checked');
    var morningRevival = $("#" + memberID + "MR").prop('checked');
    var bibleReading = $("#" + memberID + "BR").prop('checked');
    var smallGroup = $("#" + memberID + "SG").prop('checked');

    var HistoryID = findAttandance(memberID);
    var attandacne = {
        "History_ID":HistoryID,
        "Member_ID": memberID,
        "Lords_Table": lordsTable,
        "Prayer_Meeting": prayerMeeting,
        "Morning_Revival": morningRevival,
        "Bible_Reading": bibleReading,
        "Small_Group": smallGroup
    };
}

function updateAttandance() {

    $.ajaxSetup({
        beforeSend: function (xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });

    $.ajax({
        url: "/api/v1/attandancehistory/",
        type: "PUT",
        data: attandance
    })
}

function findAttandance(memberID) {
    for(i =0; i < attandances.length; i++){
        if(attandances[i].Member_ID == memberID){
            return attandances[i].History_ID;
        }
    }
}

