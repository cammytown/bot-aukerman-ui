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

	//document.body.addEventListener('htmx:beforeRequest', function(evt) {
	//    // Get trigger element
	//    let triggerEle = evt.detail.elt;

	//    // If trigger element is save script button
	//    if (triggerEle.id == 'save-script') {
	//        // Get script text element
	//        let scriptTextEle = document.getElementById('performance-script-text');

	//        // Update hidden input
	//        let hiddenInput = document.getElementById('script-text-input')
	//        hiddenInput.value = scriptTextEle.innerText;
	//    }
	//});

	// Buttons
	// Edit script
	document.getElementById('edit-script').addEventListener('click', function() {
		let scriptTextEle = document.getElementById('performance-script-text');

		// Check if the script is already being edited
		//@TODO probably improve architecture
		//if(scriptTextEle.getAttribute('contenteditable') == 'true') {
		//    // Disable editing
		//    scriptTextEle.setAttribute('contenteditable', 'false');

		//    // Remove editing class
		//    scriptTextEle.classList.remove('editing');

		//    // Change button text
		//    this.innerHTML = 'Edit Script';

		//    // Save script
		//    document.getElementById('save-script').click();

		//} else {
			// Enable editing
			scriptTextEle.setAttribute('contenteditable', 'true');

			// Add editing class
			scriptTextEle.classList.add('editing');

			// Hide this button
			this.style.display = 'none';

			// Show save button
			document.getElementById('save-script').style.display = 'inline-block';

			//// Change button text
			//this.innerHTML = 'Save Script';
		//}
	});

	document.getElementById('save-script').addEventListener('click', function() {
		let scriptTextEle = document.getElementById('performance-script-text');

		// Hide this button
		this.style.display = 'none';

		// Show edit button
		document.getElementById('edit-script').style.display = 'inline-block';

		// Update the script text input
		document.getElementById('script-text-input').value = scriptTextEle.innerText;

		// Submit the form
		//@REVISIT this is a hacky way to submit the form
		htmx.trigger('#edit-script-form', 'submit');
	});

	//document.getElementById('performance-script-text')
	//    .addEventListener('keydown', function() {
	//        console.log('input');

	//        // Update the script text input
	//        document.getElementById('script-text-input').value = this.innerText;
	//    });
});
