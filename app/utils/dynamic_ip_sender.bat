@echo off

D:\Anaconda\Scripts\activate.bat
conda activate CUHKSZ-CE

cd D:
cd D:\Repos\CUHKSZ-CE

python utils\dynamic_ip_sender.py
