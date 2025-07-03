# ToDo for Server Configuration

- Named Arguments
- Setup Cuda Visible Devices
- Add cache_dir when loading LLM model (cache_dir=f"/external-raid/scratch/SIT/akarsh_sit/{checkpoint}")
- Setup Dockerfile
  - Change WORKDIR
  - Make sure requirements are correct
- Setup .devcontainer
  - Change name
  - Add new image name
  - Add new workspaceFolder
  - Make sure the "target" inside the mount is same as the above workspaceFolder
  - Make sure the "postCreateCommand" are same as the requirements


# How to access NVIDIA's GPU

Connect to Zerotier VPN
```bash
sudo zerotier-cli join <vpn_id>
```

Connect to server via SSH
```bash
ssh <username>@<server_ip>
```

**PS: docker image name is what you give to your project in Dockerfile, but container\_name and container\_id is provided by docker**

## Before Building the Docker
Please create a folder inside '/external-raid/scratch/SIT/' with your name such as: /external-raid/scratch/SIT/akarsh_sit/

### To run a docker, make sure you are in the folder containting Dockerfile
```bash
docker build -t <image_name> .
```

### To run and access the docker from terminal
```bash
# To run the docker with respect to the workspace in background
# Please change the /workspace folder name if already exsists
docker run -d --gpus=all -v $(pwd):/workspace -v /raid:/external-raid -w /workspace -e PYTHONUNBUFFERED=1 <image_name> tail -f /dev/null

# To access the docker from terminal
docker exec -it <container_id> /bin/bash
``` 

### To run the python program inside the workspace
```bash
# Please note the --cuda_device argument specifies which GPU you are accessing in the system
# If running in server, please type the GPU number from the list (0,1,2,3...), example --cuda_device 2
python main.py --is_server True --cuda_device 0

# If running on personal system with more than one GPU, for example two GPU
python main.py --is_server False --cuda_device 0,1

# You can also shorten the argument with:
python main.py -s True -c 0
```

### To stop and delete docker container
```bash
# To search your container_id, you can perform the following (-a provides result even if the docker is stopped).
# The first column with your image name has your container_id (example of container_id: 75984bc77751)
docker ps -a | grep <image_name>
docker stop <container_id> 

# When you no longer require the the container
docker rm <container_id> 
```

### To use the same docker container 
```bash
# To search your container_id, you can perform the following (-a provides result even if the docker is stopped).
# The first column with your image name has your container_id (example of container_id: 75984bc77751)
docker ps -a | grep <image_name>
docker restart <container_id>
```

## To delete an image
```bash
# To delete an image properly, use the image_id. Third column will provide you with the image_id (example of image_id: 624994aa8f5d)
docker images | grep <image_name>
docker rmi <image_id>
```

## Note
If folders is not being deleted from the SSH VSCode, enter into the workspace and delete the folder.

PS: Please make sure the container is running, and you can use '/bin/bash' or '/bin/sh' accoridng to conveninence.