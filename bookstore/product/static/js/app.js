function Unable(){
	$("#target :input"). prop("disabled", true)
	document.getElementById('btn_edit').disabled = false;
}

function Enable(){
	$("#target :input"). prop("disabled", false)
}
function getSelection(id){
	var k = document.getElementById(id);
	array =[]
	op="";
	for (let index = 0; index < array.length; index++) {
		// op += `<option value = ${value}>${value}<option>`
	}
	k.innerHTML = op;
}
