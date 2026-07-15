# How to Stop the Docker Background Engine
sudo systemctl status docker
sudo systemctl stop docker
sudo systemctl disable docker

# Verify that the installation is successful by running the hello-world image:
sudo docker run hello-world

# List ALL running containers
sudo docker ps

# List ALL containers (even stopped ones):
sudo docker ps -a

# Stop a running container:
sudo docker stop <container_id_or_name>

# Delete a container:
sudo docker rm <container_id_or_name>

# Start an EXISTING (Stopped) container
sudo docker start <CONTAINER_ID_or_NAME>



# Openvas installation on docker:

mkdir ~/openvas-docker
cd ~/openvas-docker

#  Download the OpenVAS Blueprint (compose.yaml)
curl -f -L https://greenbone.github.io/docs/latest/_static/compose.yaml -o compose.yaml

# Start the openvas container:
sudo docker compose -f compose.yaml -p greenbone-community-edition up -d

# : Verify they are running!
sudo docker ps




-----------------------------------------------------------------------
# How to Actually Make OpenVAS Use Less Memory in Docker

# Step 1: Open your configuration file
cd ~/openvas-docker
nano compose.yaml

# Step 2: Add memory limits
deploy:
      resources:
        limits:
          memory: 1500M


# Step 3: Restart the containers
sudo docker compose -f compose.yaml -p greenbone-community-edition up -d
-------------------------------------------------------------------------


# Stop the OpenVAS Containers
cd ~/openvas-docker
sudo docker compose -f compose.yaml -p greenbone-community-edition down
# Start the OpenVAS Containers
sudo docker compose -f compose.yaml -p greenbone-community-edition up -d

sudo docker ps

http://localhost:9392


- OpenVAS needs to load its massive vulnerability database (scap-data, cert-bund-data, etc.) into the main engine memory. This happens automatically in the background right now.

To check if it is ready for your first test scan, run this log command:
sudo docker compose -f compose.yaml -p greenbone-community-edition logs -f gvmd

==============================================================================
# apt openvas

sudo systemctl edit gvmd

sudo systemctl stop gvmd


sudo gvm-check-setup
 1286  sudo gvm-start


sudo systemctl stop gvmd gsad ospd-openvas
sudo systemctl disable gvmd gsad ospd-openvas
