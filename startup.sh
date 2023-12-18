#!/bin/bash

jupyter lab \
    --no-browser \
    --ip=* \
     --port 8888 \
    --notebook-dir=/home/idies/workspace \
    --NotebookApp.token= \
    --KernelSpecManager.ensure_native_kernel=False \
    --NotebookApp.allow_remote_access=True \
    --NotebookApp.quit_button=False 
    