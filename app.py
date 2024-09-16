import time
import docker
from flask import Flask, request, jsonify, render_template

app = Flask(__name__)
client = docker.from_env()

# In-memory log storage
monitored_requests = []

# List of verified pip packages
verified_packages = ["requests", "flask", "numpy", "pandas"]

# Function to check if a package is verified
def is_package_verified(package_name):
    return package_name in verified_packages

# Function to monitor and sanitize HTTP/HTTPS requests
def monitor_webhook(url, method="GET", headers=None, body=None):
    sanitized_url = url if url.startswith("https://") or url.startswith("http://") else None
    if not sanitized_url:
        return {"error": "Invalid URL"}
    
    # Create a log entry for the monitored request
    log_entry = {
        "method": method,
        "url": sanitized_url,
        "headers": headers,
        "body": body,
        "timestamp": time.time()
    }
    
    # Store the log entry in the monitored_requests list
    monitored_requests.append(log_entry)
    
    # Log request details
    print(f"Outgoing request monitored: {log_entry}")
    
    return {"status": "monitored", "details": log_entry}

# Function to create a container with restricted network access
def create_container_with_network(container_name):
    container = client.containers.run(
        "my-python-container",  # Custom image with pip pre-installed
        name=container_name,
        detach=True,
        mem_limit="512m",        # Memory constraint
        cpu_quota=50000,         # CPU constraint (0.5 of a core)
        network="restricted_network",  # Attach to restricted network
        tty=True                 # Keep the container alive
    )
    return container

# API route to create a new container
@app.route('/create_container', methods=['POST'])
def create_container():
    data = request.json
    container_name = data.get('name', 'python_container')
    
    container = create_container_with_network(container_name)
    return jsonify({
        "status": "success",
        "container_id": container.id,
        "container_name": container_name
    })

# API route to install a verified pip package
@app.route('/install_package', methods=['POST'])
def install_package():
    data = request.json
    container_id = data.get('container_id')
    package_name = data.get('package_name')
    
    # Check if the package is verified
    if not is_package_verified(package_name):
        return jsonify({"status": "error", "message": f"{package_name} is not verified."})
    
    # Get the container and install the package
    try:
        container = client.containers.get(container_id)
        exec_log = container.exec_run(f"pip install {package_name}")
        return jsonify({"status": "success", "message": exec_log.output.decode('utf-8')})
    except docker.errors.NotFound:
        return jsonify({"status": "error", "message": "Container not found"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

# API to check the status of a container
@app.route('/container/<container_id>/status', methods=['GET'])
def container_status(container_id):
    try:
        container = client.containers.get(container_id)
        uptime = time.time() - time.mktime(time.strptime(container.attrs['State']['StartedAt'], "%Y-%m-%dT%H:%M:%S.%fZ"))
        return jsonify({
            "id": container.id,
            "status": container.status,
            "uptime": uptime,
        })
    except docker.errors.NotFound:
        return jsonify({"error": "Container not found"}), 404

# Admin API to view monitored HTTP/HTTPS requests (JSON)
@app.route('/admin/monitoring', methods=['GET'])
def view_monitored_requests():
    return jsonify(monitored_requests)

# Admin page to view monitored requests in HTML
@app.route('/admin/monitoring/page', methods=['GET'])
def view_monitored_requests_page():
    return render_template("monitoring.html", logs=monitored_requests)

# Admin API to set limits for a container
@app.route('/admin/container/<container_id>/limits', methods=['POST'])
def update_container_limits(container_id):
    memory_limit = request.form.get('memory_limit', '512m')
    cpu_limit = float(request.form.get('cpu_limit', 0.5))
    container = client.containers.get(container_id)
    container.update(mem_limit=memory_limit, cpu_quota=int(cpu_limit * 100000))
    return f"Limits updated for container {container_id}"

# Flask app runner
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
