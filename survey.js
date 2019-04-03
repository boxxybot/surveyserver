var arrivalDate = new Date().getTime();
var x = setInterval(function() {
	var now = new Date().getTime();
	var distance = now - arrivalDate;
	var seconds = Math.floor(distance / 1000);
	document.getElementById("blarg").value = seconds;
}, 1000);
