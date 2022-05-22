signup_sock = io('wss://patriot-point-manager.hpms-services.repl.co')

function submit() {
	email = document.getElementById('email').value
	username = document.getElementById('username').value
	password = document.getElementById('password').value
	if (email.trim() != '' && /^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$/.test(email) && username.trim() != '' && password.trim() != '') {
		signup_sock.emit('teacher_signup', {
			email: email,
			username: username,
			password: password
		})
	}
	else {
		alert('Fill out all the questions before attempting to submit the form.')
	}
}
	
signup_sock.on('signup_fail', function(d) {
	document.getElementById('info').innerHTML = d.message
})

signup_sock.on('signup_success', function() {
	window.location = '/teacher/login'
})

signup_sock.on('signup_awaiting_conf', function() {
	document.getElementById('info').innerHTML = 'to make sure that students don\'t give themselves Patriot Points and cheat, your email will be whitelisted. Please try again later.'
})