function Unable(){
	$("#target :input"). prop("disabled", true)
	document.getElementById('btn_edit').disabled = false;
}

function Enable(){
	$("#target :input"). prop("disabled", false)
}

