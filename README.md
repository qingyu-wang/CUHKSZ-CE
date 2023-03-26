# CUHKSZ-CE Activity Management System

<p align="center">
  <img src="./docs/images/screenshot-index.png" width="80%">
</p>

![screenshot-index](./docs/images/screenshot-index.png)

- [Environment](#environment)
- [Service](#service)
- [Tool](#Tool)
- [Server](#Server)
- [Problem](#problem)
  - [Dynamic IP Access](#dynamic-ip-access)
- [Reference](#reference)

## Environment

- [windows](./notes/environment-windows.md)
- [linux](./notes/environment-linux.md)



## Service

**linux**
- [debug](scripts/script-linux-debug.sh)
  - ```shell
    sh scripts/script-linux-debug.sh
    ```
- [deploy](scripts/script-linux-deploy.sh)
  - ```shell
    sh scripts/script-linux-deploy.sh
    ```

**windows**
- [debug](scripts/script-windows-debug.bat)
  - ```shell
    scripts\script-windows-debug.bat
    ```
- [deploy](scripts/script-windows-deploy.bat)
  - ```shell
    scripts\script-windows-deploy.bat
    ```



## Tool
- [mongo](./notes/tool-mongo.md)
- [oracle](./notes/tool-oracle.md)



## Server

[server](./notes/server.md#main)



## External Access

### Static IP Access

1. **config domain**: bind local IP address (with 80 port) in DNS setting
2. **config Nginx**: set `proxy_pass` to define the redirect location according to the `server_name`

### Dynamic IP Access

1. [`localhost`](#localhost) send current IP address to [`cloud database`](#cloud-database)
2. [`URL`](#URL) search IP address on [`cloud database`](#cloud-database) and redirect

**localhost**
- windows
  - script
    - [`utils\dynamic_ip_sender.py`](utils\dynamic_ip_sender.py)
    - [`utils\dynamic_ip_sender.bat`](utils\dynamic_ip_sender.bat): execute `dynamic_ip_sender.py` in conda
    - [`utils\dynamic_ip_sender.vbs`](utils\dynamic_ip_sender.vbs): execute `dynamic_ip_sender.bat` in silent
  - windows service: `Task Scheduler`
    - trigger
      - begin the task: `at log on`
      - repeat task every `5 minutes` for a duration of `indefinitely`
      - stop task if it runs longer than `30 minutes`
      - `enable`
    - action
      - action: `start a program`
      - program/script: `send_dynamic_ip.vbs`
      - start in: `D:\Repos\CUHKSZ-CE\utils`

**URL**
- `https://url.cuhkszce.link/`
  - [Google Cloud](https://cloud.google.com/)
    - [Google Cloud Console](https://console.cloud.google.com/)
    - [Google Cloud Run (Pricing)](https://cloud.google.com/run/pricing)
      - mode: allocate CPU when request
      - | each month free   | usage                             | Cool                |
        |:-----------------:|:---------------------------------:|:-------------------:|
        |  180k vCPUs       |  0.08 vCPU  * 10k users * 30days  | 7.5s / (user * day) |
        |  360k GiBs        |   128 MiB   * 10k users * 30days  | 9.6s / (user * day) |
        | 2000k requests    |   10k users * 30days              | 6.0  / (user * day) |
    - [Google Cloud Function (Pricing)](https://cloud.google.com/functions/pricing)
      - each month free 2000k requests  =>               10k users * 30days  => 6.0  / (user * day)
  - [NameSilo](https://www.namesilo.com/account_domains.php)
    - `https://cuhkszce.link/`
    - 15 RMB/Y
- `https://cuhkszce.pythonanywhere.com/`
  - [Python Anywhere](https://www.pythonanywhere.com/)
    - free

**cloud database**
- [MongoDB Cloud](https://www.mongodb.com/cloud)
  - [MongoDB Cloud (Pricing)](https://www.mongodb.com/pricing)
    - storage 512MB



## Reference

- [Bulma](https://bulma.io/documentation/)
- [Jinja Template](https://jinja.palletsprojects.com/en/3.1.x/templates/)
