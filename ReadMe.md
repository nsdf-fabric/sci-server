# Instructions
 

List of examples:

- examples/geoviews      https://github.com/holoviz/geoviews/tree/main/examples/gallery
- examples/panel         https://github.com/holoviz/panel/tree/main/examples/gallery
- examples/holoviews     https://github.com/holoviz/holoviews/tree/main/examples/gallery/demos

List of learning notebooks:

- learning/gis_notebooks https://github.com/Automating-GIS-processes/notebooks

Table of content:

- [Windows PIP      ](#windows-pip)
- [Windows Conda    ](#windows-conda)
- [Linux/macOS PIP  ](#linux-macos-pip)
- [Linux/macOS Conda](#linux-macos-conda)
- [Dev notes]        (#developer-notes)


# Windows PIP

- Download and Install Python for windows (see https://www.python.org/downloads/windows/) 
- Download and install [git for windows](https://gitforwindows.org/)- 

in a MSDOS prompt

```bat
git clone https://github.com/nsdf-fabric/sci-server
cd sci-server

python -m venv .venv
.venv\Scripts\activate
python -m pip install  -r requirements.pip.txt -r requirements.txt
jupyter lab .
```

# Windows Conda

- Download and install [Miniforge3-Windows-x86_64.exe](https://github.com/conda-forge/miniforge/releases/latest/download/Miniforge3-Windows-x86_64.exe)
- Download and install [git for windows](https://gitforwindows.org/)- 

in a MSDOS prompt

```bat

git clone https://github.com/nsdf-fabric/sci-server`
cd sci-server

set PATH=%PATH%;%USERPROFILE%\miniforge3\Scripts
mamba create --name my-env -y -c bokeh -c conda-forge --file requirements.conda.txt --file requirements.txt
conda init
# you may have to open a new prompt
mamba activate my-env
jupyter lab .
```

## Linux/macOS PIP 

```bash

git clone https://github.com/nsdf-fabric/sci-server
cd sci-server

python3 -m venv ./.venv
source .venv/bin/activate
python3 -m pip install  -r requirements.pip.txt -r requirements.txt
jupyter lab  .
```

## Linux/macOS Conda

NOTE: This works on Apple ARM64 too (i.e. Silicon M1/M2)

Download and Install miniforge3:

```bash
curl -L "https://github.com/conda-forge/miniforge/releases/latest/download/Miniforge3-$(uname)-$(uname -m).sh" -o miniforge3.sh 
bash miniforge3.sh -b
```

```bash

git clone https://github.com/nsdf-fabric/sci-server
cd sci-server

export PATH=${HOME}/miniforge3/bin:$PATH
mamba create --name my-env -y -c bokeh -c conda-forge python=3.10 --file requirements.conda.txt --file requirements.txt
conda init # you may have to re-open your shell 
conda activate my-env
jupyter lab .
```

