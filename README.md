# Flask Python Environment Container Management

## Description

This project is a Flask-based framework for managing isolated Python environments using Docker containers. It includes the following features:

- Create independent, sandboxed Python containers accessible via webhooks.
- Install verified Python packages using `pip` within these containers.
- Monitor HTTP/HTTPS requests from each container, sanitize them, and log them for admin review.
- Admin interface for viewing container status, monitoring requests, and adjusting container limits.

## Features

1. **Container Management**:
   - Create, stop, and monitor Docker containers.
   - Each container is isolated from others and the main system.
   - Containers have limited network access, restricted to verified sources for `pip` installations.

2. **Monitored Webhooks**:
   - Sanitize and monitor outgoing HTTP/HTTPS requests.
   - View logs in JSON format or through a user-friendly admin HTML page.

3. **Resource Limits**:
   - Set memory and CPU limits for each container via the admin panel.

4. **Admin Panel**:
   - View and manage containers through a web UI.
   - View monitored requests via an HTML table or JSON API.

## Setup

1. **Clone the repository**:

   ```bash
   [git clone https://github.com/your-repo/flask-container-management.git](https://github.com/unaveragetech/flask-container-management.git)
   cd flask-container-management
