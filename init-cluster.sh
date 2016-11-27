# Deps
sudo apt-get install -y \
    libhdf5-serial-dev \
    python-pip \
    python-dev \
    build-essential \
    python-h5py \
    python-numpy \
    python-scipy \
    python-pandas

# symlink to get hdf5 to work correctly

cd /usr/lib/x86_64-linux-gnu
sudo ln -s libhdf5_serial.so.8.0.2 libhdf5.so
sudo ln -s libhdf5_serial_hl.so.8.0.2 libhdf5_hl.so

# Python deps

sudo pip install pymongo networkx boto3 hyperopt keras


# Install TF

export TF_BINARY_URL=https://storage.googleapis.com/tensorflow/linux/cpu/tensorflow-0.11.0rc2-cp27-none-linux_x86_64.whl &&\
sudo pip install --upgrade $TF_BINARY_URL

# Install Picard!

sudo pip install git+https://jakebian:3epRebef@github.com/jakebian/picard.git#egg=picard


# AWS credentials
echo "export AWS_ACCESS_KEY_ID=AKIAIERW4XK43L2NMXDQ &&\
export AWS_SECRET_ACCESS_KEY=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 &&\
export AWS_DEFAULT_REGION=us-west-2" | tee -a /etc/profile.d/conda_config.sh /etc/*bashrc /etc/profile
