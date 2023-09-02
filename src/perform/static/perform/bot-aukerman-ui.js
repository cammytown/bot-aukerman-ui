window.addEventListener('load', function() {
	// Add shortcut keys
	document.addEventListener('keydown', function(e) {
		// Ctrl + Enter
		if (e.ctrlKey && e.keyCode == 13) {
			// Click the start button
			document.getElementById('start-performance').click();
		}

		// Ctrl + Space
		if (e.ctrlKey && e.keyCode == 32) {
			// Toggle microphone listening
			document.getElementById('toggle-microphone').click();
		}
	});
});
