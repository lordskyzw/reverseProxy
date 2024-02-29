from flask import Flask, request, redirect, session, flash, render_template, Response
import requests
from flask_sqlalchemy import SQLAlchemy
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///reverse.db'
app.secret_key = 'my_secret_key_nigga'
db = SQLAlchemy(app)
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)



servers = [
    "http://server-webapp1-1:80",
    "http://server-webapp2-1:80",
    "http://server-webapp3-1:80"
]
current_server = 0

@app.route('/<path:path>', methods=['GET'])
def handle_request(path):
    global current_server
    client_ip = request.remote_addr  # Get the client IP address
    logging.info("client ip is ================%s", client_ip)
    print(f"client ip is{client_ip}")

    # Assuming you have a function to check if IP is from university
    if is_university_network(client_ip):
        return forward_request_to_server(path)
    else:
        # Save the requested path in the session for later retrieval
        session['requested_resource'] = path
        return redirect('/sign-in')

@app.route('/sign-in', methods=['GET', 'POST'])
def sign_in():
    if request.method == 'POST':
        username = request.form['username']  # Changed from 'email' to 'username'
        password = request.form['password']
        if validate_credentials(username, password):
            # Credentials are valid, retrieve the saved path and forward the request
            path = session.pop('requested_resource', None)
            return forward_request_to_server(path) if path else "Resource not found", 404
        else:
            # Credentials are invalid, inform the user
            flash('Invalid credentials, please try again.')
            return render_template('sign_in.html'), 401
    return render_template('sign_in.html')

def forward_request_to_server(path):
    global current_server

    # Select the next server in a round-robin fashion
    server = servers[current_server]
    current_server = (current_server + 1) % len(servers)

    # Construct the full URL to forward the request to
    url = f"{server}/files/{path}"
    logging.info("sending path========================: %s", path)
    logging.info("FULL URL==============================: %s", url)

    # Forward the request to the selected server
    # Note: might need to include additional headers or data based on your specific requirements
    resp = requests.get(url)
    response = Response(resp.iter_content(), status=resp.status_code)
     # Copy relevant headers
    excluded_headers = ['content-encoding', 'content-length', 'transfer-encoding', 'connection']
    headers = [(name, value) for (name, value) in resp.raw.headers.items() if name.lower() not in excluded_headers]
    for header in headers:
        response.headers[header[0]] = header[1]

    return response

def validate_credentials(username, password):
    user = User.query.filter_by(username=username).first()
    if user and user.password == password:  # In a real app, use hashed passwords
        return True
    return False

def is_university_network(ip_address):
    # Example list of university IP ranges or specific IPs
    university_ips = ['192.168.1.1', '192.168.1.2']  # Replace with actual university IPs or ranges
    university_ip_ranges = [('192.168.1.100', '192.168.1.200')]  # Example IP range

    # Check if the IP is in the list of specific IPs
    if ip_address in university_ips:
        return True

    # Check if the IP is within any of the specified ranges
    for start, end in university_ip_ranges:
        if ip_address_to_int(start) <= ip_address_to_int(ip_address) <= ip_address_to_int(end):
            return True

    # IP does not belong to the university network
    return False

def ip_address_to_int(ip_address):
    """
    Convert an IP address from string format to a 32-bit integer to facilitate range comparison.
    This does not account for IPv6 addresses.
    """
    octets = [int(octet) for octet in ip_address.split('.')]
    return (octets[0] << 24) + (octets[1] << 16) + (octets[2] << 8) + octets[3]




if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
