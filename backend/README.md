# Accident Reconstruction Backend Repo
- python3.10
- poetry
- django
- Docker 

## Usage this repo
1. dependency 설치
   1. poetry 혹은 virtualenv를 사용한 dependency관리
   2. `poetry shell` or `virtualenv venv` 사용
   3. poetry 사용 한다면 `pyproject.toml`에 남아있음
      1. poetry export --without-hashes --format=requirements.txt > requirements.txt
   4. virtualenv 사용한다면 `pip freeze > requriements.txt` 필요

## Run Server
- Docker 사용
  ```shell
  docker build test-server .
  docker run -e ENV=local -p 8000:8000 test-server 
  ```
- local에서 개발
  - 개발환경 설정을 모두 마친 후에 .env에 `ENV=local`을 설정 해 준다