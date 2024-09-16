import os
import subprocess

def install_docker():
    """
    Installs Docker and ensures that the system is properly configured for Docker.
    """
    print("Installing Docker...")

    # Update package info and install required dependencies
    subprocess.run(["sudo", "apt-get", "update"], check=True)
    subprocess.run(["sudo", "apt-get", "install", "-y", "apt-transport-https", "ca-certificates", "curl", "software-properties-common"], check=True)

    # Add Docker's official GPG key
    subprocess.run(["curl", "-fsSL", "https://download.docker.com/linux/ubuntu/gpg", "|", "sudo", "gpg", "--dearmor", "-o", "/usr/share/keyrings/docker-archive-keyring.gpg"], check=True)

    # Set up the stable repository for Docker
    subprocess.run(["sudo", "add-apt-repository", "deb", "[arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"], check=True)

    # Install Docker Engine
    subprocess.run(["sudo", "apt-get", "update"], check=True)
    subprocess.run(["sudo", "apt-get", "install", "-y", "docker-ce", "docker-ce-cli", "containerd.io"], check=True)

    # Verify Docker is installed correctly
    try:
        subprocess.run(["docker", "--version"], check=True)
        print("Docker installed successfully.")
    except subprocess.CalledProcessError:
        print("Error: Docker installation failed.")
        return False

    return True


def setup_docker_env():
    """
    Set Docker environment variables and write them to a Replit environment file.
    """
    print("Setting up Docker environment variables...")

    # Check if DOCKER_HOST, DOCKER_CERT_PATH, DOCKER_TLS_VERIFY are set
    docker_host = os.getenv("DOCKER_HOST", "unix:///var/run/docker.sock")
    docker_cert_path = os.getenv("DOCKER_CERT_PATH", "/etc/docker/certs")
    docker_tls_verify = os.getenv("DOCKER_TLS_VERIFY", "0")

    # Write environment variables to a file
    env_vars = {
        "DOCKER_HOST": docker_host,
        "DOCKER_CERT_PATH": docker_cert_path,
        "DOCKER_TLS_VERIFY": docker_tls_verify
    }

    # Specify the file where the environment variables will be written
    replit_env_file = ".replit_docker_env"

    with open(replit_env_file, "w") as env_file:
        for key, value in env_vars.items():
            env_file.write(f"{key}={value}\n")

    print(f"Docker environment variables have been written to {replit_env_file}")


def check_docker_status():
    """
    Check if Docker daemon is running.
    """
    try:
        subprocess.run(["sudo", "systemctl", "is-active", "--quiet", "docker"], check=True)
        print("Docker is running.")
    except subprocess.CalledProcessError:
        print("Docker is not running. Starting Docker...")
        subprocess.run(["sudo", "systemctl", "start", "docker"], check=True)
        print("Docker started.")


def main():
    # Install Docker if not already installed
    if install_docker():
        # Setup environment variables for Docker
        setup_docker_env()

        # Ensure Docker is running
        check_docker_status()


if __name__ == "__main__":
    main()
