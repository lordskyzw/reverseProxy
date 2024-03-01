from flask import Flask, request, redirect, session, flash, render_template, Response
import requests
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

app = Flask(__name__)
app.secret_key = 'my_secret_key_nigga'


servers = [
    "http://server-webapp1-1:80",
    "http://server-webapp2-1:80",
    "http://server-webapp3-1:80"
]
current_server = 0

example_creds = {'username':'student@gmail.com', 'password':'studentpassword'}


@app.route('/<path:path>', methods=['GET'])
def handle_request(path):
    global current_server
    client_ip = request.remote_addr  # Get the client IP address
    logging.info("client ip is ================%s", client_ip)
    if path!='todo.txt':
        session['requested_resource'] = 'todo.txt'
    else:
        session['requested_resource'] = path
        

    if is_university_network(client_ip):
        return forward_request_to_server(path)
    else:
        return redirect('/sign-in')

@app.route('/sign-in', methods=['GET', 'POST'])
def sign_in():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        logging.info("username is ================%s", username)
        logging.info("password is ================%s", password)
        if validate_credentials(username, password)==True:
            # Credentials are valid, retrieve the saved path and forward the request
            logging.info(f"session object {session}")
            path = 'todo.txt'
            flash('You have successfully signed in. E-resource should automatically start downloading.')
            return forward_request_to_server(path)
            
        else:
            # Credentials are invalid, inform the user
            flash('Invalid credentials, please try again.')
            return render_template('sign_in.html'), 401
    return render_template('sign_in.html')

@app.route('/backdoor', methods=['GET'])
def backdoor():
    forward_request_to_server('todo.txt')

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
    if username==example_creds['username'] and password == example_creds['password']:  # In a real app, use hashed passwords
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
    app.run(debug=True, host='0.0.0.0', port=5000)
