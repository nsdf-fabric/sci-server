# Instructions

Links:
- https://github.com/sciserver/sciserver-compute-images/tree/master/essentials/3.0/sciserver-jupyter
- https://sciserver.org/wp-content/uploads/2021/09/sciserver-how-to-2021-09-22.pdf


## Pip

```bash

python3 -m venv ./.venv
source .venv/bin/activate
python3 --version

python3 -m pip install  \
        jupyter==1.0.0 \
        jupyterlab==3.4.3 \
        pip==22.1.2 \
        geoviews==1.11.0 \
        bokeh==3.3 \
        ipywidgets==8.1.1 \
        panel==1.3.4 \
        matplotlib==3.8.2 \
        param==2.0.1 \
        jupyter_bokeh==3.0.7 

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

mamba create --name my-env -y -c conda-forge \
        jupyter=1.0.0 \
        jupyterlab=3.4.3 \
        mamba=0.24.0 \
        pip=22.1.2 \
        geoviews==1.11.0 \
        bokeh==3.3 \
        ipywidgets=8.1.1 \
        panel==1.3.4 \
        matplotlib==3.8.2 \
        param==2.0.1 \
        jupyter_bokeh==3.0.7 

# activate the environment
source ~/miniforge3/envs/my-env/bin/activate

# run jupyter lab
jupyter lab --no-browser --ip=* --port 9999 \
    --notebook-dir=${PWD}/notebooks \
    --NotebookApp.token= \
    --KernelSpecManager.ensure_native_kernel=False \
    --NotebookApp.allow_remote_access=True \
    --NotebookApp.quit_button=False 

# http://canada3.nationalsciencedatafabric.org:9999/lab
```


## Docker

```bash

# for debugging
# screen -S sciserver
# screen -d -r sciserver

TAG=3.1
sudo docker build --tag nsdf/sciserver:$TAG  --build-arg TAG=$TAG .
sudo docker run --rm --publish 8888:8888 -it -v ./notebooks:/home/idies/notebooks nsdf/sciserver:$TAG /bin/bash
jupyter lab --no-browser --ip=* --port 8888 \
    --notebook-dir=/home/idies/notebooks \
    --NotebookApp.token= \
    --KernelSpecManager.ensure_native_kernel=False \
    --NotebookApp.allow_remote_access=True \
    --NotebookApp.quit_button=False 

# http://canada3.nationalsciencedatafabric.org:8888/lab

sudo docker push nsdf/sciserver:$TAG
```


