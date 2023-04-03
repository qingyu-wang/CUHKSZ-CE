# Environment Linux

```shell
conda create -n CUHKSZ-CE python=3.9

conda activate CUHKSZ-CE

conda install -y tqdm
conda install -y flask
conda install -y flask-login
conda install -y ipython
conda install -y openpyxl
conda install -y pandas
conda install -y requests

pip install Flask-APScheduler

# MongoDB
pip install pymongo[srv]

# Oracle
# install https://www.oracle.com/database/technologies/instant-client/linux-x86-64-downloads.html
sudo apt-get install libaio1
conda install cx_oracle
# modify "lib_dir" in utils/utils_oracle.py
```

## Deploy - Gunicorn
```shell
pip install gunicorn

gunicorn -w 4 -b 0.0.0.0 "app:app"
```

## Deploy - Nginx
```shell
sudo apt install nginx

# Control Service
sudo systemctl status  nginx
sudo systemctl start   nginx
sudo systemctl stop    nginx
sudo systemctl restart nginx

# Config
# /etc/nginx/sites-enabled/default
# copy
sudo cp \
./docs/configs/nginx-linux.conf \
/etc/nginx/sites-enabled/default
# edit
sudo vi /etc/nginx/sites-enabled/default
```

## Deploy - Supervisor
```shell
sudo apt install supervisor

# Control Service
sudo systemctl status  supervisor
sudo systemctl start   supervisor
sudo systemctl stop    supervisor
sudo systemctl restart supervisor

# Control Task
sudo supervisorctl start   CUHKSZ-CE
sudo supervisorctl restart CUHKSZ-CE
sudo supervisorctl status  CUHKSZ-CE
sudo supervisorctl stop    CUHKSZ-CE

# Config
# /etc/supervisor/supervisord.conf
# /etc/supervisor/conf.d/*.conf
# copy
cp \
./docs/configs/supervisor-linux.conf \
/etc/supervisor/conf.d/supervisor-CUHKSZ-CE.conf
# edit
vi /etc/supervisor/conf.d/supervisor-CUHKSZ-CE.conf
```
