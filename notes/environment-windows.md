# Environment Windows

```
conda create -n CUHKSZ-CE python=3.9

conda activate CUHKSZ-CE

comda install -y tqdm
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
# install https://www.oracle.com/database/technologies/instant-client/winx64-64-downloads.html
conda install -y cx_oracle 
# modify "lib_dir" in utils/utils_oracle.py

# windows
conda install -y pywin32
conda install -y waitress
```
