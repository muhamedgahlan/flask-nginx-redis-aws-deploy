# 🚀 3-Tier Dockerized Application with Automated GitLab CI/CD & AWS EC2

An end-to-end DevOps project that automates the deployment of a robust 3-Tier web application (Nginx, Flask, and Redis) onto an AWS EC2 instance using **GitLab CI/CD**, **Docker Hub**, and **Docker Compose**.

---

## 🏗️ Architecture Overview (The 3-Tier Design)

This application is decoupled into three isolated, containerized tiers to ensure scalability, security, and maintainability:

``` 
       [ User / Client ]
              │
              ▼ (Port 80)
┌───────────────────────────┐
│       Nginx Tier          │ ──► Reverse Proxy & Static Content Server
└─────────────┬─────────────┘
              │ (Internal Docker Network)
              ▼
┌───────────────────────────┐
│       Flask Tier          │ ──► Python Web Application / REST API
└─────────────┬─────────────┘
              │ (Internal Docker Network)
              ▼
┌───────────────────────────┐
│        Redis Tier         │ ──► In-Memory Data Store / Database
└───────────────────────────┘
```

Presentation Tier (Nginx): Acts as the reverse proxy, handling incoming HTTP traffic from clients and routing requests safely to the application tier.

Application Tier (Flask): The core business logic built with Python/Flask, processing requests and interacting with the data layer.

Data Tier (Redis): A high-performance, in-memory data store handling caching and persistence.

🎯 Why Did We Design It This Way? (Key Engineering Decisions)
Isolation & Microservices: Separating the web server, application logic, and database into distinct containers prevents single-point-of-failure issues and allows independent scaling.

Automated CI/CD Pipeline: Manual deployments are prone to human error. Utilizing GitLab CI/CD ensures that every code change undergoes a rigorous, automated lifecycle from code to production.

Build-Once, Deploy-Anywhere Strategy:

Utilizing docker:dind (Docker-in-Docker) in the pipeline to build images securely.

Tagging images with both $CI_PIPELINE_IID (for version tracking and rollback capabilities) and latest (to seamlessly satisfy production docker-compose pulls without manual file modifications on the server).

Secure Remote Deployment: Leveraging SSH-based deployment backed by GitLab File Variables (my_key) and strict host key verification to safely communicate with the AWS EC2 instance without exposing sensitive credentials.

🔄 CI/CD Pipeline Workflow
The pipeline is structured into 3 distinct stages inside .gitlab-ci.yml:

Build (build_images):

Builds the multi-tier application using docker compose build.

Tags and exports the images (nginx, flask) into .tar archive artifacts.

Push (push_images):

Authenticates with Docker Hub securely.

Loads the artifacts, tags them with both the pipeline ID and latest, and pushes them to Docker Hub.

Deploy (deploy_EC2):

Connects securely via SSH to the AWS EC2 instance (Amazon Linux 2023).

Pulls the updated container images and restarts the stack seamlessly using docker compose up -d.

🛠️ Tech Stack
Cloud Infrastructure: AWS EC2 (Amazon Linux 2023)

CI/CD Platform: GitLab CI/CD

Containerization: Docker, Docker Compose, Docker Hub

Web Server / Backend: Nginx, Python (Flask)

Database: Redis

Automation Tools: Git, Bash, OpenSSH

⚙️ How to Setup & Run Locally
Clone the repository:

Bash
git clone [https://github.com/your-username/your-repo-name.git](https://github.com/your-username/your-repo-name.git)
cd your-repo-name
Run the application locally using Docker Compose:

Bash
docker compose up --build -d
Access the application:
Open your browser and navigate to http://localhost.

🔐 Environment & GitLab Variables Configuration
To run this pipeline successfully on your own GitLab repository, configure the following variables under Settings > CI/CD > Variables:

DOCKER_USERNAME: Your Docker Hub username.

DOCKER_PASSWORD: Your Docker Hub password or Access Token.

IP: The Public IPv4 address of your AWS EC2 instance.

my_key: (File Variable) Containing your EC2 .pem private SSH key content.
