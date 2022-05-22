login_sock = io('wss://patriot-point-manager.hpms-services.repl.co')

login_sock.on('connect', function () {
	console.log('connected')
})

function login() {
	uname = document.getElementById('username').value
	pwd = document.getElementById('password').value
	login_sock.emit('teacher_login', {
		username: uname,
		password: pwd
	})
}

login_sock.on('login_successful', function() {
	console.log('login success')
	window.location = '/teacher/portal'
})

login_sock.on('login_failed', function(data) {
	console.log(data.message)
	document.getElementById('info').innerHTML = data.message
})