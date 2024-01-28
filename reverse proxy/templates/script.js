document.getElementById('signInForm').addEventListener('submit', function(event) {
    event.preventDefault();
    var email = document.getElementById('email').value;
    var password = document.getElementById('password').value;
    
    // Here you would handle the sign in, for example sending it to a server
    console.log('Email:', email, 'Password:', password);
    
    // For demonstration purposes, just show an alert
    alert('Sign In Successful (not really, just a placeholder)');
});
