# Instructions

Links:
- https://github.com/sciserver/sciserver-compute-images/tree/master/essentials/3.0/sciserver-jupyter
- https://sciserver.org/wp-content/uploads/2021/09/sciserver-how-to-2021-09-22.pdf
- SLITE https://sci-visus.slite.com/app/channels/OwxhuMq3GHY_Jk


## Pip

```bash

python3 -m venv ./.venv
source .venv/bin/activate
python3 --version

python3 -m pip install  -r requirements.txt

jupyter lab --no-browser --ip=* --port 7777 \
    --notebook-dir=${PWD}/notebooks \
    --NotebookApp.token= \
    --KernelSpecManager.ensure_native_kernel=False \
    --NotebookApp.allow_remote_access=True \
    --NotebookApp.quit_button=False 

# http://canada3.nationalsciencedatafabric.org:7777/lab

```

## Miniforge

```bash

# install miniforge
curl -L "https://github.com/conda-forge/miniforge/releases/latest/download/Miniforge3-$(uname)-$(uname -m).sh" -o miniforge3.sh 
bash miniforge3.sh -b
rm -f miniforge3.sh

# create the environment
export PATH=${HOME}/miniforge3/bin:$PATH

mamba create --name my-env -y -c conda-forge --file requirements.txt

# activate the environment
source ~/miniforge3/envs/my-env/bin/activate

# run jupyter lab
jupyter lab --no-browser --ip=* --port 8888 \
    --notebook-dir=${PWD}/notebooks \
    --NotebookApp.token= \
    --KernelSpecManager.ensure_native_kernel=False \
    --NotebookApp.allow_remote_access=True \
    --NotebookApp.quit_button=False 

# http://canada3.nationalsciencedatafabric.org:8888/lab
```

## Docker

**PROBLEM HERE**
- bokeh port is not reachable from the outside
- if you need bokeh, use `--network host` to make all the ports reachable

```bash

# for debugging
# screen -S sciserver
# screen -d -r sciserver


sudo docker build --tag nsdf/sciserver:$TAG  --build-arg TAG=3.1.0
sudo docker run --rm --publish 9999:9999 -it -v ./notebooks:/home/idies/notebooks nsdf/sciserver:3.1.0 /bin/bash
jupyter lab --no-browser --ip=* --port 9999 \
    --notebook-dir=/home/idies/notebooks \
    --NotebookApp.token= \
    --KernelSpecManager.ensure_native_kernel=False \
    --NotebookApp.allow_remote_access=True \
    --NotebookApp.quit_button=False 

# http://canada3.nationalsciencedatafabric.org:9999/lab

sudo docker push nsdf/sciserver:3.1.0
```


