//@TODO this is mostly scaffolding

window.addEventListener('load', function() {
	// Add shortcut keys
	addShortcutKeys();

	// If on the performance page
	if(document.body.dataset.page == 'performance') {
		initPerformance();
	}
});

function addShortcutKeys() {
	document.addEventListener('keydown', function(e) {
		//@TODO hacky way to accomplish functionality

		// Ctrl + Enter
		if (e.ctrlKey && e.keyCode == 13) {
			// Click generate dialogue button
			document.getElementById('generate-dialogue').click();

			// Click the start button
			//document.getElementById('start-performance').click();
		}

		// Ctrl + M
		if (e.ctrlKey && e.keyCode == 77) {
			// Toggle microphone listening
			document.getElementById('toggle-microphone').click();
		}

		// Ctrl + Space
		if (e.ctrlKey && e.keyCode == 32) {
			// Interrupt audio
			document.getElementById('interrupt-audio').click();
		}
	});
}

function initPerformance() {
	// Websocket
	initPerformanceWebsocket();
}

function editScript() {
	let scriptTextEle = document.getElementById('performance-script-text');

	// Enable editing
	scriptTextEle.setAttribute('contenteditable', 'true');

	// Add editing class
	scriptTextEle.classList.add('editing');

	// Hide this button
	document.getElementById('edit-script').style.display = 'none';

	// Show save button
	document.getElementById('save-script').style.display = 'inline-block';

	//// Change button text
	//this.innerHTML = 'Save Script';
	//}
}

function saveScript() {
	let scriptTextEle = document.getElementById('performance-script-text');

	// Hide this button
	document.getElementById('save-script').style.display = 'none';

	// Show edit button
	document.getElementById('edit-script').style.display = 'inline-block';

	// Update the script text input
	document.getElementById('script-text-input').value = scriptTextEle.innerText;

	// Submit the form
	//@REVISIT this is a hacky way to submit the form
	htmx.trigger('#edit-script-form', 'submit');
}

function initPerformanceWebsocket() {
	// Get the performance id
	let performanceId = document.body.dataset.performanceId;

	// Websocket
	let url = `ws://${window.location.host}/ws/performances/`
		+ `${performanceId}`;

	let websocket = new WebSocket(url);

	websocket.onopen = function() {
		console.log('Websocket opened');
	};

	websocket.onmessage = function(e) {
		// Get updated script
		//@TODO probably scaffolding
		htmx.ajax(
			'GET',
			`/get_script/${performanceId}`,
			{
				target: '#performance-script-text',
				swap: 'outerHTML show:window:bottom'
			}
		);
	};

	websocket.onclose = function() {
	};
}
