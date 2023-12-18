# Instructions

Links:
- https://github.com/sciserver/sciserver-compute-images/tree/master/essentials/3.0/sciserver-jupyter
- https://sciserver.org/wp-content/uploads/2021/09/sciserver-how-to-2021-09-22.pdf

```


# for debugging
screen -S sciserver
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

sudo docker push nsdf/sciserver:$TAG
```

Open
- # http://canada3.nationalsciencedatafabric.org:8888/lab

