# Instructions

Links:
- https://github.com/sciserver/sciserver-compute-images/tree/master/essentials/3.0/sciserver-jupyter
- https://sciserver.org/wp-content/uploads/2021/09/sciserver-how-to-2021-09-22.pdf
- SLITE https://sci-visus.slite.com/app/channels/OwxhuMq3GHY_Jk


## Docker


```bash

# for debugging
# screen -S sciserver-valerio
# screen -d -r sciserver-valerio

TAG=3.3.1
sudo docker build --tag nsdf/sciserver:$TAG  --build-arg TAG=$TAG .

# # check chrome developer console to see if the address is correct
JUPYTER_PORT=8888
JUPYTER_HOSTNAME=canada3.nationalsciencedatafabric.org
JUPYTER_TOKEN=""
sudo docker run \
  --rm \
  -it  \
  --publish ${JUPYTER_PORT}:${JUPYTER_PORT} \
  -e JUPYTER_BOKEH_EXTERNAL_URL="http://${JUPYTER_HOSTNAME}:${JUPYTER_PORT}" \
  -e JUPYTERHUB_SERVICE_PREFIX="/lab" \
  -e JUPYTER_PORT=${JUPYTER_PORT} \
  -e JUPYTER_TOKEN=${JUPYTER_TOKEN} \
  -v ${PWD}:${PWD} \
  -w ${PWD} \
  nsdf/sciserver:$TAG \
  /bin/bash

# run jupyter lab
jupyter lab --no-browser \
    --ip=* \
    --port ${JUPYTER_PORT} \
    --notebook-dir=${PWD} \
    --NotebookApp.token=${JUPYTER_TOKEN} \
    --KernelSpecManager.ensure_native_kernel=False \
    --NotebookApp.allow_remote_access=True \
    --NotebookApp.quit_button=False 

# http://canada3.nationalsciencedatafabric.org:8888/lab

sudo docker push nsdf/sciserver:${TAG}
```

## pip 


```bash

# best if you have python3.10
# rm -Rf  ./.venv
python3 -m venv ./.venv
source .venv/bin/activate
python -m pip install  PyQt5==5.15.9 -r requirements.txt

# Install NodeJS (see section below)

# enable bokeh for jupyter lab
jupyter serverextension enable --py jupyter_server_proxy
jupyter labextension install    @jupyterlab/server-proxy

# run jupyter lab
JUPYTER_PORT=8888
JUPYTER_HOSTNAME=canada3.nationalsciencedatafabric.org
JUPYTER_TOKEN=""
export JUPYTER_BOKEH_EXTERNAL_URL="http://${JUPYTER_HOSTNAME}:${JUPYTER_PORT}"
export JUPYTERHUB_SERVICE_PREFIX="/lab" # check chrome developer console to see if the address is correct

jupyter lab --no-browser \
    --ip=${JUPYTER_HOSTNAME} \
    --port ${JUPYTER_PORT} \
    --notebook-dir=${PWD} \
    --NotebookApp.token=${JUPYTER_TOKEN} \
    --KernelSpecManager.ensure_native_kernel=False \
    --NotebookApp.allow_remote_access=True \
    --NotebookApp.quit_button=False 

# http://canada3.nationalsciencedatafabric.org:8888/lab
```

## conda

```bash

# Install conda
curl -L "https://github.com/conda-forge/miniforge/releases/latest/download/Miniforge3-$(uname)-$(uname -m).sh" -o miniforge3.sh 
bash miniforge3.sh -b
rm -f miniforge3.sh

# Install NodeJS 
# see section below

# create the environment
export PATH=${HOME}/miniforge3/bin:$PATH

# rm -Rf ~/miniforge3/envs/my-env
mamba create --name nsdf-sciserver-env -y -c bokeh -c conda-forge python=3.10 pyqt==5.15.9 --file requirements.txt

# activate the environment
conda activate nsdf-sciserver-env

# enable bokeh for jupyter lab
jupyter serverextension enable --py jupyter_server_proxy
jupyter labextension install    @jupyterlab/server-proxy

# run jupyter lab
JUPYTER_PORT=8888
JUPYTER_HOSTNAME=canada3.nationalsciencedatafabric.org
JUPYTER_TOKEN=""
export JUPYTER_BOKEH_EXTERNAL_URL="http://${JUPYTER_HOSTNAME}:${JUPYTER_PORT}"
export JUPYTERHUB_SERVICE_PREFIX="/lab" # check chrome developer console to see if the address is correct
jupyter lab --no-browser \
    --ip ${JUPYTER_HOSTNAME} \
    --port ${JUPYTER_PORT} \
    --notebook-dir=${PWD} \
    --NotebookApp.token=${JUPYTER_TOKEN} \
    --KernelSpecManager.ensure_native_kernel=False \
    --NotebookApp.allow_remote_access=True \
    --NotebookApp.quit_button=False 

# http://canada3.nationalsciencedatafabric.org:8888/lab

conda deactivate
conda deactivate
```

## Install NodeJS

NoJS is needed foor jupyter lab proxy for bokeh:

```bash

sudo apt-get update
sudo apt-get install -y ca-certificates curl gnupg
sudo mkdir -p /etc/apt/keyrings
curl -fsSL https://deb.nodesource.com/gpgkey/nodesource-repo.gpg.key | sudo gpg --dearmor -o /etc/apt/keyrings/nodesource.gpg
NODE_MAJOR=16
echo "deb [signed-by=/etc/apt/keyrings/nodesource.gpg] https://deb.nodesource.com/node_$NODE_MAJOR.x nodistro main" | sudo tee /etc/apt/sources.list.d/nodesource.list
sudo apt-get update
sudo apt-get install -y yarn nodejs
```


