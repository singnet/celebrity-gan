FROM nvidia/cuda:10.0-cudnn7-runtime-ubuntu16.04

RUN apt update && \
    apt install -y wget curl nano git python3-dev python3-pip && \
    cd ~ && \
    git clone https://github.com/tkarras/progressive_growing_of_gans.git && \
    cd progressive_growing_of_gans &&\
    pip3 install --upgrade pip && \
    pip install -r requirements-pip.txt && \
    pip install tensorflow-gpu==1.12.0 && \
    wget https://raw.githubusercontent.com/singnet/semantic-segmentation-aerial/master/service/download_models.py && \
    chmod +x download_models.py && \
    ./download_models.py --filepath ./import_example.py --google_file_id 1xZul7DwqqJoe5OCuKHw6fQVeQZNIMSuF && \
    ./download_models.py --filepath ./karras2018iclr-celebahq-1024x1024.pkl --google_file_id 188K19ucknC6wg1R6jbuPEhTq9zoufOx4 && \
    chmod +x import_example.py && \
    python3 import_example.py


RUN pip3 install https://download.pytorch.org/whl/cu100/torch-1.1.0-cp35-cp35m-linux_x86_64.whl && \
    pip3 install torchvision && \
    cd ~ && \
    git clone https://github.com/ToniCreswell/InvertingGAN.git && \
    wget https://raw.githubusercontent.com/ToniCreswell/attribute-cVAEGAN/master/notebooks/DataToTensorCelebA_smileLabel.ipynb && \
    # INSTALL SCIKIT-IMAGE
    # REMOVE NOTEBOOKS
    # PUT GOOGLE DRIVE DOWNLOADING SCRIPT INSIDE THIS REPO