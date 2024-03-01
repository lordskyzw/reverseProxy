document.getElementById('signInForm').addEventListener('submit', function(event) {
    event.preventDefault();
    
    var email = document.getElementById('email').value;
    var password = document.getElementById('password').value;
    
    var formData = new FormData();
    formData.append('username', email);
    formData.append('password', password);
    
    fetch('/sign-in', {
        method: 'POST',
        body: formData
    })
    .then(response => {
        if (response.ok) {
            // Redirect to a route that triggers the file download
            window.location.href = '/backdoor'; // Adjust the path as needed
        } else {
            throw new Error('Sign in failed');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Sign In Failed');
    });
});
