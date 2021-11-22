var jwt = null

function secure_get_with_token(endpoint, data_to_send, on_success_callback, on_fail_callback) {
	
	xhr = new XMLHttpRequest();
	
	function setHeader(xhr) {
		xhr.setRequestHeader('Authorization', 'Bearer:' + jwt);
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
	jwt = null;
	
	// hide store show login page
	$("#login").show();
	$("#store").hide();
	
	alert("Log Out successful.");

}

function login() {
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

function signup() {
	$.post("/open_api/signup", {"username" : $('#username').val(), "password" : $('#password').val()},
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
			data.books[i][0] + '" name="book_id" value="this.id" onclick="buyBook(this.id);">Buy</button></td>'
			+ '<td><strong class="bookTitle">' + data.books[i][1] 
			+ '</strong> by ' + data.books[i][2] + '</td>'
			+ '<td>' + data.books[i][3] + '</td>'
			+ '<td>$ ' + data.books[i][4] + '</td></tr>');
		}
	},
		function(err) { 
			console.log(err) 
		});
}

function buyBook(book_id) {
	secure_get_with_token("/secure_api/buy_book", {"book_id" : book_id} , function(data) {
		console.log("buy book"); 
		console.log(data);
		
		// empty books table
		pulledBooks.innerHTML = "";
		// refresh the book listing
		get_books();
		
		alert(data.message);
	},
		function(err) { 
			console.log(err) 
	});
}