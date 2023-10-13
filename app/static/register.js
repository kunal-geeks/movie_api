    // Handle form submission
    document.getElementById('registration-form').addEventListener('submit', function(event) {
        event.preventDefault();
    
        fetch('/auth/register', {
            method: 'POST',
            body: new FormData(this),
        })
        .then(response => response.json())
        .then(data => {
            // Handle response here
            if (data.status === 'success') {
                $('#response-message').removeClass('alert-danger').addClass('alert-success').text(data.message).removeClass('d-none');
            } else {
                $('#response-message').removeClass('alert-success').addClass('alert-danger').text(data.message).removeClass('d-none');
            }
        })
        .catch(error => console.error('Error:', error));
    }); 