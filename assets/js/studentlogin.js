login_sock = io('wss://patriot-point-manager.hpms-services.repl.co')

function login() {
	username = document.getElementById('username').value
	password = document.getElementById('password').value
	if (username.trim() != '' && password.trim() != '') {
		login_sock.emit('student_login', {
			username: username,
			password: password
		})
	}
	else {
		alert('Please fill the form properly')
	}
}

login_sock.on('login_success', function() {
	window.location = '/student/portal'
})

login_sock.on('login_fail', function(d) {
	document.getElementById('info').innerHTML = d.message
})