$(document).ready(function() {
	$(document).on("keydown", checkKey)
	
	
	
});
function checkKey(evt) {
	var key = evt.keyCode;
	console.log(key);
	if (key === 39) {
		moveleftorright(1)
		
		
	}
	else if (key === 37) {
		moveleftorright(-1)
		
		
		
		
	}
	else if (key === 38) {
		moveup(3)
		
	}
	
	
}
function moveleftorright(number) {
	 var value = document.getElementById("character").style.left;
            value = value.replace("%", "");
			value = parseInt(value);
            value = value + number;
            value = value + "%";
            document.getElementById("character").style.left = value;
	
	
}
function moveup(number) {
var value = document.getElementById("character").style.bottom;
 value = value.replace("%", "");
			value = parseInt(value);
            value = value + number;
            value = value + "%";
            document.getElementById("character").style.bottom = value;
			
			value = value.replace("%", "");
			value = parseInt(value);
            value = value - number;
            value = value + "%";
            document.getElementById("character").style.bottom = value;
			

	
}

/* carne y papas son muy sobrosos y bueno para salud*/

