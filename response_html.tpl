<html>
<meta name="viewport" content="width=device-width, initial-scale=1">
<link rel="stylesheet" href="http://domainpath/survey.css">
</head>
<script>
<script src="http//static.domainpath/survey.js" type="text/javascript">
</script>
<body>
<p>{{q}}</p>
<div class='formresponse'>
<form id='response' name='response' method='post'>
<div class="slidecontainer">
  <input type="range" min="1" max="6" class="slider" id="myRange" name='w'>
  <p><span id="demo" class='prompt'></span></p>
</div>
<input type='hidden' name='q' value='{{n}}'><br>
<input type='hidden' name='s'><br>
<input type='submit' id='submit' value='Next' style='visibility:hidden'>
</div>
</form>
<script>
var slider = document.getElementById("myRange");
var output = document.getElementById("demo");
output.innerHTML = 'Move the slider...';

slider.oninput = function() {
	if (this.value == '1') {stringval = 'I strongly disagree'}
	if (this.value == '2') {stringval = 'I disagree'}
	if (this.value == '3') {stringval = 'I sort of disagree'}
	if (this.value == '4') {stringval = 'I sort of agree'}
	if (this.value == '5') {stringval = 'I agree'}
	if (this.value == '6') {stringval = 'I strongly agree'}
  document.getElementById("submit").style.visibility='visible';
  output.innerHTML = stringval;
}
</script>
</body>
