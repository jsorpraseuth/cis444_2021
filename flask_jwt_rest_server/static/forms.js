function registerForm() {
	document.getElementById("formSubmit").value = "Sign Up";
	document.getElementById("formHeader").innerHTML = "Sign Up";
	$("#registerForm").hide();
	$("#loginForm").show();
}

function loginForm() {
	document.getElementById("formSubmit").value = "Log In";
	document.getElementById("formHeader").innerHTML = "Log In";
	$("#registerForm").show();
	$("#loginForm").hide();
}