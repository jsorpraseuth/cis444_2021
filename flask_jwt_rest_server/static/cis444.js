var jwt = null

function secure_get_with_token(endpoint, data_to_send, on_success_callback, on_fail_callback) {
	
	xhr = new XMLHttpRequest();
	
	function setHeader(xhr) {
		xhr.setRequestHeader('Authorization', 'Bearer: ' + jwt);
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

var pulledBooks;

function logout() {
	// empty books table
	pulledBooks.innerHTML = "";
	
	// delete session token
	fetch("/logout");
	jwt = undefined;
	
	// hide store show login page
	$("#login").show();
	$("#store").hide();
}

function verify() {
	$.post("/open_api/login", {"username" : $('#username').val(), "password" : $('#password').val()},
		function(data, textStatus) {
			if(data.authenticated == false) {
				alert(data.message);
				return false;
			}
			//this gets called when browser receives response from server
			console.log(data.token);
			// store jwt
			jwt = data.token
			$("#login").hide();
			//make secure call with the jwt
			get_books();
		}, "json").fail(function(response) {
			//this gets called if the server throws an error
			console.log("error");
			console.log(response);
		});

	return false;
}

function get_books() {	
	secure_get_with_token("/secure_api/get_books", {} , function(data) {
		console.log("got books"); 
		console.log(data);
		
		$('#store').show();
		
		// display books
		for(i = 0; i < data.books.length; i++) {
		// <button id="book_id" onclick="buyBook(this.id);">Buy</button>
			pulledBooks = document.getElementById("books");
			pulledBooks.insertAdjacentHTML('beforeend', '<tr><td><button id="' + 
			response.data.books[i].book_id + '" onclick="buyBook(this.id);">Buy</button></td>'
			+ '<td><strong class="bookTitle">' + response.data.books[i].book_name 
			+ '</strong> by ' + response.data.books[i].book_author + '</td>'
			+ '<td>' + response.data.books[i].book_genre + '</td>'
			+ '<td>$ ' + response.data.books[i].book_price + '</td></tr>');
		}
	},
		function(err){ console.log(err) });
}

async function buyBook(id) {
	const response = await $.post("/buyBook", { "jwt": token.jwt, "book_id": id }, "json");
	alert(response.message);
}