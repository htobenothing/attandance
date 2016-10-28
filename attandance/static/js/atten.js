/**
 * Created by nothing on 10/27/16.
 */

function confirmOwnAtten(id) {
    var memberID = id.split("_")[0];
    var record = document.getElementsByClassName(memberID);
    $("."+memberID).prop("disabled",true);

}

function editAtten(id) {
    var memberID = id.split("_")[0];
    var record = document.getElementsByClassName(memberID);
    $("."+memberID).prop("disabled",false);
}