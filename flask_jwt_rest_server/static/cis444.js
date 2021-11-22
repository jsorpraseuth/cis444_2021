var jwt = null

function secure_get_with_token(endpoint, data_to_send, on_success_callback, on_fail_callback) {
	
	console.log("Secure Call: " + method);
	
	xhr = new XMLHttpRequest();
	
	function setHeader(xhr) {
		xhr.setRequestHeader('Authorization', 'Bearer:'+jwt);
	}
	
	function get_and_set_new_jwt(data){
		console.log(data);
		jwt = data.token
		on_success_callback(data)
	}
	
	$.ajax({
		url: endpoint,
		data : data_to_send,
		type: 'GET',
		datatype: 'json',
		success: on_success_callback,
		error: on_fail_callback,
		beforeSend: setHeader
	});
}

var token;
var pulledBooks;

function logout() {
	// empty books table
	pulledBooks.innerHTML = "";
	
	// delete session token
	fetch("/logout");
	token = undefined;
	
	// hide store show login page
	$("#login").show();
	$("#store").hide();
}

async function verify() {
	var text = document.getElementById("formHeader").innerHTML.toLowerCase();
	var action = (text == "log in") ? "login" : "signup";
	
	const response = await $.post("/" + action,
		{ "username": document.getElementById("username").value, "password": document.getElementById("password").value }, "json");
	if (action == "login" && response.status == 200) {
		token = await response.data
		loadBooks();
		$("#login").hide();
		$("#store").show();
	}
	else {
		alert(response.data.message);
	}
	
	document.getElementById("username").value = "";
	document.getElementById("password").value = "";
	return true;
}

async function loadBooks() {
	const response = await $.post("/loadBooks", { "jwt": token.jwt }, "json");
	for(i = 0; i < response.data.books.length; i++) {
		// <button id="book_id" onclick="buyBook(this.id);">Buy</button>
		pulledBooks = document.getElementById("books");
		pulledBooks.insertAdjacentHTML('beforeend', '<tr><td><button id="' + 
		response.data.books[i].book_id + '" onclick="buyBook(this.id);">Buy</button></td>'
		+ '<td><strong class="bookTitle">' + response.data.books[i].book_name 
		+ '</strong> by ' + response.data.books[i].book_author + '</td>'
		+ '<td>' + response.data.books[i].book_genre + '</td>'
		+ '<td>$ ' + response.data.books[i].book_price + '</td></tr>');
	}
}

async function buyBook(id) {
	const response = await $.post("/buyBook", { "jwt": token.jwt, "book_id": id }, "json");
	alert(response.data.message);
}