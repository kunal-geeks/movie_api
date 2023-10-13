document.getElementById('loginForm').addEventListener('submit', function(event) {
    event.preventDefault(); // Prevent the default form submission

    var formData = new FormData(event.target);

    fetch('auth/login', {
        method: 'POST',
        body: formData,
        headers: {
            'Accept': 'application/json'
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'success') {
            window.location.href = data.redirect || '/dashboard';
        } else {
            alert(data.message); // Show an alert for login failure
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });
});