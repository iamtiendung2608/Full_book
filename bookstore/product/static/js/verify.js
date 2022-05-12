    function OTPInput() {
        const inputs = document.querySelectorAll('#otp > *[id]');
        for (let i = 0; i < inputs.length; i++) {
            inputs[i].addEventListener('keydown', function (event) { 
                if (event.key === "Backspace") {
                    inputs[i].value = ''; 
                }
                else {
                    if (i === inputs.length - 1 && inputs[i].value !== ''){
                        return true;
                    }
                    else if (event.keyCode > 47 && event.keyCode < 58) {
                        inputs[i].value = event.key;
                        if (i !== inputs.length - 1)
                            inputs[i + 1].focus(); event.preventDefault(); 
                    } 
                    else if (event.keyCode > 64 && event.keyCode < 91) { 
                        inputs[i].value = String.fromCharCode(event.keyCode); 
                        if (i !== inputs.length - 1) 
                            inputs[i + 1].focus();event.preventDefault(); 
                    } 
                } 
            });
        }
    }
    
function Open() {
    callCode();
    document.getElementById('verify').classList.remove("pop-up-off");
    OTPInput();
}

function callCode(){
    $.ajax({
        type: "GET",
        url: "/bill/confirm",
        data: {
        },
        success: function(response){
            $('#code').text(response.code);
        },
        error: function () {
            console.log("error");
        }
    });
}

function validate(){
    var value = '';
    const inputs = document.querySelectorAll('#otp > *[id]');
    for (let i = 0; i < inputs.length; i++){
        value += inputs[i].value;
    }
    var code = $('#code').text();
    if(code != value){
        window.alert("Invalid code! ");
    }
    else{
        jQuery(document.body).append("<div class='push-notification' id='notification'>Confirm Success!</div>");
        jQuery('#notification').show().fadeOut(2000, function () {
            jQuery('#notification').remove();
        });
        document.getElementById('verify').classList.add("pop-up-off");
        $('#btn-submit').prop('disabled',false);
    }
}