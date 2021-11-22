function registerForm() {
	document.getElementById("formHeader").innerHTML = "Sign Up";
	$("#registerForm").hide();
	$("#loginSubmit").hide();
	$("#signupSubmit").show();
	$("#loginForm").show();
}

function loginForm() {
	document.getElementById("formHeader").innerHTML = "Log In";
	$("#registerForm").show();
	$("#loginSubmit").show();
	$("#signupSubmit").hide();
	$("#loginForm").hide();
}