# Docker Storage Mechanisms

## Introduction to Docker Storage
By default, all files created inside a Docker container are stored on a writable container layer. This data is tightly coupled with the container lifecycle: it does not persist when the container is deleted, and it is difficult to share data with other containers or the host machine. To resolve these challenges, Docker provides three robust mechanisms to persist data and share files between the host system and containers: **Bind Mounts**, **Volumes**, and **tmpfs Mounts**.

---

## 1. Bind Mounts
Bind mounts allow you to map a specific directory or file on your host machine directly into a container. Any modifications made to the files—whether from inside the container or on the host—are instantly reflected on both sides. This mechanism is primarily utilized during development for sharing source code, configuration files, or local logs into a container for real-time testing.

---

## 2. Volumes
Volumes are completely managed by Docker and stored within a dedicated directory on the host system (typically under `/var/lib/docker/volumes/` on Linux systems). Unlike bind mounts, users do not interact directly with the file path on the host; instead, Docker safely controls the storage. Volumes are the gold standard for data persistence, making them ideal for storing databases and persistent application state that must survive container recreation.

---

## 3. tmpfs Mounts
A tmpfs mount does not write data to the host machine's persistent disk storage at all. Instead, it stores data entirely within the host system's memory (RAM). When the container stops, the tmpfs mount is removed, and all files written within it are permanently discarded. This approach is specifically designed for high-performance temporary storage of sensitive information, tokens, or credentials that must never be written to non-volatile disk media.

---

## Comparison of Docker Storage Methods

| Feature | Bind Mounts | Volumes | tmpfs Mounts |
| :--- | :--- | :--- | :--- |
| **Management & Control** | Directly managed by the User/Host | Fully managed by Docker Engine | Host System Memory (RAM) |
| **Storage Location** | Any custom path on the Host system | Docker-managed dedicated directory (Disk) | System RAM (No disk storage) |
| **Data Persistence** | Persists on host when container is deleted | Persists safely across container lifecycles | Erased immediately when container stops |
| **Primary Use Case** | Sharing source code & configuration files | Persistent databases & application state | Sensitive, ephemeral data & caching |

---


# Understanding Docker Images, Pull, and Containers


Instead of manually downloading and configuring application code and dependencies from scratch, Docker utilizes pre-packaged, ready-to-run environments. This approach ensures consistency across different environments, from development to production.

---

### 1. Docker Image
* **Definition:** A Docker image is a read-only template or blueprint that contains everything needed to run an application—including the code, runtime, system tools, libraries, and settings.
* **Analogy:** Think of a Docker image as a class definition in programming or a software installation ISO file; it is the static blueprint from which containers are created.

---

### 2. Docker Pull
* **Definition:** `docker pull` is the command used to download a Docker image from a centralized registry (such as Docker Hub) onto your local machine.
* **Process:** When you want an application (like OWASP Juice Shop), Docker checks your local cache; if the image is missing, it fetches the required layers from the remote registry over the internet.

---

### 3. Container Creation & Docker Run
* **Definition:** A container is a runnable, isolated instance of a Docker image. When you execute `docker run`, Docker takes the static read-only image and adds a thin writable layer on top of it, turning it into a living, breathing process.
* **Key Components during Run:**
  * **Port Mapping (`-p`):** Exposing container ports to the host machine so users or other services can access the application.
  * **Volume Mounting (`-v`):** Linking persistent storage directories so data survives container deletion.
  * **Detached Mode (`-d`):** Running the container in the background without locking your terminal session.

---

### Summary of Workflow

1. **Docker Hub (Registry):** Where developers store and share Docker images.
2. **Docker Pull:** Downloads the image to your local computer.
3. **Docker Run:** Instantiates the image into an active, running **Docker Container**.


---
# Docker Commands

### How to Stop the Docker Background Engine
sudo systemctl status docker
sudo systemctl stop docker
sudo systemctl disable docker

### Verify that the installation is successful by running the hello-world image:
sudo docker run hello-world  

### List ALL running containers
sudo docker ps

### List ALL containers (even stopped ones):
sudo docker ps -a

### Stop a running container:
sudo docker stop <container_id_or_name>

### Delete a container:
sudo docker rm <container_id_or_name>

### Start an EXISTING (Stopped) container
sudo docker start <CONTAINER_ID_or_NAME>



### Openvas installation on docker:

mkdir ~/openvas-docker
cd ~/openvas-docker

###  Download the OpenVAS Blueprint (compose.yaml)
curl -f -L https://greenbone.github.io/docs/latest/_static/compose.yaml -o compose.yaml

### Start the openvas container:
sudo docker compose -f compose.yaml -p greenbone-community-edition up -d

### : Verify they are running!
sudo docker ps




-----------------------------------------------------------------------
### How to Actually Make OpenVAS Use Less Memory in Docker

### Step 1: Open your configuration file
cd ~/openvas-docker
nano compose.yaml

### Step 2: Add memory limits
deploy:
      resources:
        limits:
          memory: 1500M


### Step 3: Restart the containers
sudo docker compose -f compose.yaml -p greenbone-community-edition up -d
-------------------------------------------------------------------------


### Stop the OpenVAS Containers
cd ~/openvas-docker
sudo docker compose -f compose.yaml -p greenbone-community-edition down
### Start the OpenVAS Containers
sudo docker compose -f compose.yaml -p greenbone-community-edition up -d

sudo docker ps

http://localhost:9392


- OpenVAS needs to load its massive vulnerability database (scap-data, cert-bund-data, etc.) into the main engine memory. This happens automatically in the background right now.

To check if it is ready for your first test scan, run this log command:
sudo docker compose -f compose.yaml -p greenbone-community-edition logs -f gvmd

==============================================================================
### apt openvas

sudo systemctl edit gvmd

sudo systemctl stop gvmd


sudo gvm-check-setup
 1286  sudo gvm-start


sudo systemctl stop gvmd gsad ospd-openvas
sudo systemctl disable gvmd gsad ospd-openvas
