function ModifyClass(){
    $("#target :input").addClass("form-control, col-xs-3");
}
function valid(){
    var province = $("#id_Province");
    var city = $("#id_City");
    var details = $("#id_Details");
    var delivery = $("#id_date_delivery");
    if(province.length==0||city.length==0||details.length==0||delivery.length==0){
        document.getElementById("warning").innerHTML="<strong style='color:red'>Some Field is Null</strong>";
        return false;
    }
    document.getElementById("warning").innerHTML="";
    return true;
}