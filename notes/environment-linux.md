# Environment Linux

```
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

# mongodb
pip install pymongo[srv]

# oracle
# install https://www.oracle.com/database/technologies/instant-client/linux-x86-64-downloads.html
sudo apt-get install libaio1
conda install cx_oracle
# modify "lib_dir" in utils/utils_oracle.py
```

## Deploy - Supervisor
```shell
sudo apt install supervisor

# /etc/supervisor/supervisord.conf

sudo systemctl status  supervisor
sudo systemctl start   supervisor
sudo systemctl stop    supervisor
sudo systemctl restart supervisor

# /etc/supervisor/conf.d/*.conf

cp \
/home/hss001/HSS/repo/CUHKSZ-CE/notes/supervisor-linux.conf \
/etc/supervisor/conf.d/supervisor-CUHKSZ-CE.conf

vi /etc/supervisor/conf.d/supervisor-CUHKSZ-CE.conf

sudo supervisorctl start   CUHKSZ-CE
sudo supervisorctl restart CUHKSZ-CE
sudo supervisorctl status  CUHKSZ-CE
sudo supervisorctl stop    CUHKSZ-CE

sudo supervisorctl update CUHKSZ-CE & sudo supervisorctl restart CUHKSZ-CE

tail -n 100 /home/hss001/HSS/repo/CUHKSZ-CE/log/stdout.log
tail -n 100 /home/hss001/HSS/repo/CUHKSZ-CE/log/stderr.log
```

## Gunicorn
```
pip install gunicorn

gunicorn -w 4 -b 0.0.0.0 "app:app"
```
