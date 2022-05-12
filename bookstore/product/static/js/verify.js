let current = '';


    function OTPInput() {
        callCode();
        const inputs = document.querySelectorAll('#otp > *[id]');
        for (let i = 0; i < inputs.length; i++) {
            inputs[i].addEventListener('keydown', function (event) { 
                if (event.key === "Backspace") { 
                    inputs[i].value = ''; 
                    if (i !== 0) 
                        inputs[i - 1].focus(); 
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
            console.log(response.code);
        },
        error: function () {
            console.log("error");
        }
    });
}