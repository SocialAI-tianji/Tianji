## Docker Installation

### Use default MetaGPT image

```bash
# Step 1: Download metagpt official image and prepare config.yaml
docker pull metagpt/metagpt:latest
mkdir -p /opt/metagpt/{config,workspace}
docker run --rm metagpt/metagpt:latest cat /app/metagpt/config/config.yaml > /opt/metagpt/config/key.yaml
vim /opt/metagpt/config/key.yaml # Change the config

# Step 2: Run metagpt demo with container
docker run --rm \
    --privileged \
    -v /opt/metagpt/config/key.yaml:/app/metagpt/config/key.yaml \
    -v /opt/metagpt/workspace:/app/metagpt/workspace \
    metagpt/metagpt:latest \
    python3 startup.py "Write a cli snake game"

# You can also start a container and execute commands in it
docker run --name metagpt -d \
    --privileged \
    -v /opt/metagpt/config/key.yaml:/app/metagpt/config/key.yaml \
    -v /opt/metagpt/workspace:/app/metagpt/workspace \
    metagpt/metagpt:latest

docker exec -it metagpt /bin/bash
$ python3 startup.py "Write a cli snake game"
```

The command `docker run ...` do the following things:

- Run in privileged mode to have permission to run the browser
- Map host configure file `/opt/metagpt/config/key.yaml` to container `/app/metagpt/config/key.yaml`
- Map host directory `/opt/metagpt/workspace` to container `/app/metagpt/workspace`
- Execute the demo command `python3 startup.py "Write a cli snake game"`

### Build image by yourself

```bash
# You can also build metagpt image by yourself.
git clone https://github.com/geekan/MetaGPT.git
cd MetaGPT && docker build -t metagpt:custom .
```
