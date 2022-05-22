signup_sock = io('wss://patriot-point-manager.hpms-services.repl.co')

function submit() {
	username = document.getElementById('username').value
	password = document.getElementById('password').value
	if (username.trim() != '' && password.trim() != '') {
		signup_sock.emit('student_signup', {
			username: username,
			password: password
		})
	}
	else {
		alert('Please fill out all the boxes before attempting to submit the form.')
	}
}

signup_sock.on('signup_success', function() {
	window.location = '/student/login'
})

signup_sock.on('signup_fail', function(d) {
	document.getElementById('info').innerHTML = d.message
})