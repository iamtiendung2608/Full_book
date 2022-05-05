function ModifyClass(){
    $("#target :input").addClass("form-control, col-xs-3");
}
function valid(){
    let confirmCode = document.getElementById("code").innerHTML;
    var input = window.prompt("Input valid code: ");
    if(input == confirmCode){
        let form = document.getElementById('form').submit();
        return false;
    }
    else{
        window.alert(confirmCode);        
    }
}
