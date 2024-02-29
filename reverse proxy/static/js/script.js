document.getElementById('signInForm').addEventListener('submit', function(event) {
    event.preventDefault();
    
    var email = document.getElementById('email').value;
    var password = document.getElementById('password').value;
    
    // Construct form data
    var formData = new FormData();
    formData.append('username', email);
    formData.append('password', password);
    
    // Send the form data to the Flask sign-in route using fetch
    fetch('/sign-in', {
        method: 'POST',
        body: formData
    })
    .then(response => {
        if (response.ok) {
            return response.text();
        } else {
            throw new Error('Sign in failed');
        }
    })
    .then(text => {
        console.log(text); // Handle the response text
        alert('Sign In Successful');
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Sign In Failed');
    });
});

