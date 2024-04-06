# Hackerdom Checksystem for Services Testing

## Usage

```bash
git clone https://github.com/hacker-volodya/mini-checksystem.git
cd mini-checksystem

# download and start example service
(cd services && git clone https://github.com/hacker-volodya/intro-training.git && cd intro-training/services/simple && docker compose up -d)

# start checksystem
docker compose up -d --build
```

Checksystem will immediately start the game at http://127.0.0.1:8080.

Admin: http://127.0.0.1:8080/admin, credentials `root:root`.

To reset the game, run:
```bash
docker compose down -v
docker compose up -d --build
```

## Writing own services

During docker build, `build.py` will search for `services.yml` files in `./services` folder and subfolders. It will copy checkers to checksystem, generate `setup.sh` script and checksystem config.

services.yml layout:
```yaml
services:
  simple:  # that how service will be named internally, must be a valid directory name
    name: Simple Web Service  # pretty name, will be shown at checksystem board
    checker:
      basedir: ./checkers/simple  # directory with checkers relative to services.yml directory
      script: ./checker.py  # checker script that checksystem will run, double-check for chmod +x; this path is relative to checker.basedir
      setup: pip install --break-system-packages requests  # setup bash command, workdir is checker.basedir
    vuln:
      basedir: ./services/simple  # this repo don't do anything with it, should be a folder which will be copied to vulnbox, assumed to have docker-compose.yml file
```