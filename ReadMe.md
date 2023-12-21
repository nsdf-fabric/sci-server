# Instructions


List of examples:

- examples/geoviews      https://github.com/holoviz/geoviews/tree/main/examples/gallery
- examples/panel         https://github.com/holoviz/panel/tree/main/examples/gallery
- examples/holoviews     https://github.com/holoviz/holoviews/tree/main/examples/gallery/demos
- examples/gis_notebooks https://github.com/Automating-GIS-processes/notebooks

Table of content:

- [Windows PIP      ](#windows-pip)
- [Windows Conda    ](#windows-conda)
- [Linux/macOS PIP  ](#linux-macos-pip)
- [Linux/macOS Conda](#linux-macos-conda)
- [Dev notes]        (#developer-notes)


# Windows PIP

Install python for windows (see https://www.python.org/downloads/windows/) or `git clone https://github.com/nsdf-fabric/sci-server`

- Download https://codeload.github.com/nsdf-fabric/sci-server/zip/refs/heads/main
- Unzip it in a folder

in a MSDOS prompt

```bat

cd \directory\containing\unzipped\folder

python -m venv .venv
.venv\Scripts\activate
python -m pip install  -r requirements.pip.txt -r requirements.txt
jupyter lab .
```

# Windows Conda

Download and install [Miniforge3-Windows-x86_64.exe](https://github.com/conda-forge/miniforge/releases/latest/download/Miniforge3-Windows-x86_64.exe)

- Download https://codeload.github.com/nsdf-fabric/sci-server/zip/refs/heads/main or or `git clone https://github.com/nsdf-fabric/sci-server`
- Unzip it in a folder

in a MSDOS prompt

```bat

cd \directory\containing\unzipped\folder
set PATH=%PATH%;%USERPROFILE%\miniforge3\Scripts
mamba create --name my-env -y -c bokeh -c conda-forge --file requirements.conda.txt --file requirements.txt

conda init
# or `source $HOME/miniforge3/bin/activate`
# you may have to open a new prompt

mamba activate my-env
jupyter lab .
```

## Linux/macOS PIP 

This works on Apple ARM64 too (i.e. Silicon M1/M2)

```bash

git clone https://github.com/nsdf-fabric/sci-server
cd sci-server

# create a virtual environment
python3 -m venv ./.venv
source .venv/bin/activate

# install requirements
python -m pip install  -r requirements.pip.txt -r requirements.txt

# run jupyter lab locally
jupyter lab  .
```


## Linux/macOS Conda

This works on Apple ARM64 too (i.e. Silicon M1/M2)

Install conda:

```bash
curl -L "https://github.com/conda-forge/miniforge/releases/latest/download/Miniforge3-$(uname)-$(uname -m).sh" -o miniforge3.sh 
bash miniforge3.sh -b
```

```bash

git clone https://github.com/nsdf-fabric/sci-server
cd sci-server

# create the environment
export PATH=${HOME}/miniforge3/bin:$PATH

# rm -Rf ~/miniforge3/envs/my-env
mamba create --name my-env -y -c bokeh -c conda-forge python=3.10 --file requirements.conda.txt --file requirements.txt

conda init
# or `source $HOME/miniforge3/bin/activate`
# you may have to re-open your shell 

# activate the environment
conda activate my-env

# run jupyter lab locally
jupyter lab .
```


## Developer notes

### Docker build

```bash

# for debugging
# screen -S    sciserver
# screen -d -r sciserver

TAG=3.3.2
sudo docker build --tag nsdf/sciserver:$TAG  --build-arg TAG=$TAG .

# # check chrome developer console to see if the address is correct
JUPYTER_PORT=8888
JUPYTER_HOSTNAME=canada3.nationalsciencedatafabric.org
JUPYTER_TOKEN=""
JUPYTER_BOKEH_EXTERNAL_URL="http://${JUPYTER_HOSTNAME}:${JUPYTER_PORT}"
JUPYTERHUB_SERVICE_PREFIX="/lab"
sudo docker run \
  --rm \
  -it  \
  --publish ${JUPYTER_PORT}:${JUPYTER_PORT} \
  -e JUPYTER_BOKEH_EXTERNAL_URL=${JUPYTER_BOKEH_EXTERNAL_URL} \
  -e JUPYTERHUB_SERVICE_PREFIX=${JUPYTERHUB_SERVICE_PREFIX} \
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


### Setup public node

```bash

# need nodejs for jupyter lab
sudo apt-get update
sudo apt-get install -y ca-certificates curl gnupg
sudo mkdir -p /etc/apt/keyrings
curl -fsSL https://deb.nodesource.com/gpgkey/nodesource-repo.gpg.key | sudo gpg --dearmor -o /etc/apt/keyrings/nodesource.gpg
NODE_MAJOR=16
echo "deb [signed-by=/etc/apt/keyrings/nodesource.gpg] https://deb.nodesource.com/node_$NODE_MAJOR.x nodistro main" | sudo tee /etc/apt/sources.list.d/nodesource.list
sudo apt-get update
sudo apt-get install -y yarn nodejs

# here assuming you have the python ready
# ....

# enablejupyter lab proxy for bokeh
jupyter serverextension enable --py jupyter_server_proxy
upyter labextension install    @jupyterlab/server-proxy

# run jupyter lab on a public node
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
```

