**Installing Git:**

1. **Ubuntu:**
   Open a terminal and run the following commands:
   ```shell
   sudo apt update
   sudo apt install git
   ```

2. **macOS:**
   - Using Homebrew:
     Open a terminal and run the following command:
     ```shell
     brew install git
     ```
   - Downloading the Git installer:
     Visit the official Git website ([https://git-scm.com/download/mac](https://git-scm.com/download/mac)) and download the macOS installer. Once downloaded, run the installer and follow the installation instructions.

3. **Windows:**
   - Download the Git installer for Windows from the official Git website ([https://git-scm.com/download/win](https://git-scm.com/download/win)).
   - Run the installer and follow the installation instructions.

**Cloning the Repository:**

1. Open a terminal or command prompt.
2. Change to the directory where you want to clone the repository (e.g., `cd ~/Documents`).
3. Run the following command to clone the repository:
   ```shell
   git clone https://gitlab.com/zotac_server/lectures.git
   ```

**Installing Docker:**

1. **Ubuntu:**
   - Open a terminal.
   - Update the apt package index:
     ```shell
     sudo apt update
     ```
   - Install Docker dependencies:
     ```shell
     sudo apt install apt-transport-https ca-certificates curl software-properties-common
     ```
   - Add the Docker GPG key:
     ```shell
     curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg
     ```
   - Add the Docker repository:
     ```shell
     echo "deb [arch=amd64 signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
     ```
   - Update the apt package index again:
     ```shell
     sudo apt update
     ```
   - Install Docker:
     ```shell
     sudo apt install docker-ce docker-ce-cli containerd.io
     ```

2. **macOS:**
   - Download the Docker Desktop installer for macOS from the Docker website ([https://www.docker.com/products/docker-desktop](https://www.docker.com/products/docker-desktop)).
   - Run the installer and follow the installation instructions.

3. **Windows:**
   - Download the Docker Desktop installer for Windows from the Docker website ([https://www.docker.com/products/docker-desktop](https://www.docker.com/products/docker-desktop)).
   - Run the installer and follow the installation instructions.

**Building and running the Docker Image:**

1. Open a terminal or command prompt.
2. Change to the cloned repository directory:
   ```shell
   cd lectures
   ```
3. Build the Docker image using the provided Dockerfile:
   ```shell
   docker build -t lectures-image .
   ```
4. Run a container from the built Docker image:
   ```shell
   docker run -p8080:8080 -d lectures-image
   ```

**Accessing to the Project:**
   - To access the application after running the Docker image, you need to open your web browser and enter the following URL: http://localhost:8080, and start working.



