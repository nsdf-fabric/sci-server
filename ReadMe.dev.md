
# Developer notes (INTERNAL USE ONLY)



## Docker build

```bash

# for debugging you may want to create a screen session
# screen -S    sciserver
# screen -d -r sciserver

# change tag as needed
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


# Setup SciServer node

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
# read this https://docs.bokeh.org/en/latest/docs/user_guide/output/jupyter.html
jupyter serverextension enable --py jupyter_server_proxy
jupyter labextension install    @jupyterlab/server-proxy

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

## JupyterHub


See:
- https://github.com/jupyterhub/jupyterhub-the-hard-way/blob/HEAD/docs/installation-guide-hard.md
- https://tljh.jupyter.org/en/latest/install/custom-server.html
- https://docs.bokeh.org/en/latest/docs/user_guide/output/jupyter.htm




```bash

# uninstall previous TLJH
#   sudo rm -rf /opt/tljh/hub
#   sudo rm -rf /opt/tljh/config
#   sudo systemctl stop jupyterhub.service || true
#   sudo systemctl stop traefik.service

sudo apt install python3 python3-dev git curl
curl -L https://tljh.jupyter.org/bootstrap.py | sudo -E python3 - --admin admin

# open http://<public-ip>
# USERNAME admin
# PASSWORD <choose-your-password>

# from `Admin` create/remove users as needed

mkdir -p github.com/nsdf-fabric
cd github.com/nsdf-fabric
git clone git@github.com:nsdf-fabric/sci-server.git
cd sci-server

sudo tljh-config set user_environment.default_app jupyterlab
sudo tljh-config show

# ref https://tljh.jupyter.org/en/latest/howto/user-env/user-environment.html 
sudo /opt/tljh/user/bin/mamba update --all -y

# sudo /opt/tljh/user/bin/mamba uninstall -y openvisusnogui
# sudo /opt/tljh/user/bin/mamba uninstall -y pillow libjpeg-turbo jpeg

sudo /opt/tljh/user/bin/mamba install -y -c conda-forge python==3.10
sudo /opt/tljh/user/bin/mamba install -y -c conda-forge -c bokeh --file requirements.conda.txt --file requirements.txt
sudo /opt/tljh/user/bin/mamba install -y -c conda-forge nbgitpuller

# don't think I need this
#   curl -fsSL https://deb.nodesource.com/setup_16.x | sudo bash
#   sudo apt-get update
#   sudo apt-get install -y  nodejs yarn 

# CHANGE HOSTNAME as needed
sudo hostname http://chpc3.nationalsciencedatafabric.org

cat <<EOF > ./environment.py
c.Spawner.environment = {
        'JUPYTER_BOKEH_EXTERNAL_URL': '$(hostname)'
}
EOF
sudo mv environment.py  /opt/tljh/config/jupyterhub_config.d/environment.py

sudo tljh-config reload 
sudo tljh-config reload proxy
sudo tljh-config reload hub
```

Links:
- http://chpc1.nationalsciencedatafabric.org/
- http://chpc2.nationalsciencedatafabric.org/
- http://chpc3.nationalsciencedatafabric.org/

Populate user folder:
- https://nbgitpuller.readthedocs.io/en/latest/link.html
- http://chpc2.nationalsciencedatafabric.org/hub/user-redirect/git-pull?repo=https%3A%2F%2Fgithub.com%2Fnsdf-fabric%2Fsci-server&urlpath=lab%2Ftree%2Fsci-server%2F&branch=main


