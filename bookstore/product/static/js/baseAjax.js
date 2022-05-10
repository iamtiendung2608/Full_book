function callAjax(eventID, link){

    $.ajax({
        type : "GET",
        url : link,
        data : {

        },
        success: function(){


        }, 
        errors: function(){

        }
    })
}