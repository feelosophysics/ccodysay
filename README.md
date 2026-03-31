# 개발 환경 이해하기

## 1. 프로젝트 개요

본 미션은 개발을 시작하기 위한 기본 환경을 직접 구축하고, 그 과정을 통해 개발 도구의 원리와 구조를 이해하는 것을 목표로 한다.
터미널 기반의 작업 환경 구성, Docker를 활용한 컨테이너 실행 및 관리, Git/GitHub를 통한 버전 관리까지 포함한 전체 개발 흐름을 경험한다.
특히 다음과 같은 핵심 개념을 직접 실습하고 검증한다

- 로컬 개발 환경 구성 및 CLI 활용
- Docker 기반 컨테이너 실행 구조 이해
- 이미지와 컨테이너의 분리 개념
- 포트 매핑을 통한 외부 접근 구조
- 바인드 마운트와 볼륨을 통한 데이터 관리
- Git과 GitHub를 통한 협업 기반 코드 관리

또한 동일한 환경을 반복적으로 재현할 수 있는 개발 방식에 대해 학습한다.

---

## 2. 실행 환경

- OS: macOS 15.7.4
- Shell: zsh 5.9 (x86_64-apple-darwin24.0)
- Docker: OrbStack 내 Docker Engine(version 28.5.2)
- Git: git version 2.53.0

#### 실행 환경을 확인하는 터미널 명령어
```
$ sw_vers
ProductName:		macOS
ProductVersion:		15.7.4
BuildVersion:		24G517

$ echo $SHELL
/bin/zsh

$ zsh --version
zsh 5.9 (x86_64-apple-darwin24.0)

$ docker --version
Docker version 28.5.2, build ecc6942

$ git --version
git version 2.53.0
```

---

## 3. 터미널 기본 조작 로그

### 현재 위치 및 파일 확인

```zsh
$ pwd # 참고로, 명령어 pwd의 뜻은 print working directory이다.
/Users/user


$ ls -la
total 0
drwxr-xr-x  5 user  staff  160 Apr  1 10:00 .
drwxr-xr-x  3 root  admin   96 Apr  1 09:00 ..

# ls = list (파일 목록 출력)
# -l = long format (권한, 소유자, 크기 등 상세 정보 표시)
# -a = all (숨김 파일 포함)
```

### 디렉토리 생성 및 이동

```zsh
$ mkdir -p workspace/docker-practice # mkdir = make directory / -p 옵션은 만들고자 하는 디렉토리 상위 경로에, 명령어에서 지칭한 디렉토리가 없더라도 만들어서 실행하는 기능이다.
$ cd workspace/docker-practice # cd = change directory
$ pwd
/Users/user/workspace/docker-practice
```

### 파일 생성 및 복사/이동

```zsh
$ touch test.txt
$ cp test.txt copy.txt # cp = copy
$ mv copy.txt moved.txt # mv = move
$ ls
test.txt moved.txt
```

### 파일 내용 확인

```zsh
$ echo "hello world" > test.txt
$ cat test.txt
hello world
```

### 파일 삭제

```zsh
$ rm moved.txt
$ ls
test.txt
```

---

## 4. 파일 권한 실습

### 권한 확인

```zsh
$ ls -l
-rw-r--r--  1 user  staff  0 Apr  1 10:10 test.txt # 두 번째 글자부터 아홉 자리의 문자가 권한을 나타낸다.(rw-r--r--)
```
#### r = read, w = write, x = execute

### 권한 변경

```zsh
$ chmod 755 test.txt # chmod = change mode / 755는 빈번하게 사용되는 권한이다. [소유자][그룹][기타]의 권한 구조에서, 소유자에게만 write를 부여하기 때문.
$ ls -l
-rwxr-xr-x  1 user  staff  0 Apr  1 10:10 test.txt
```

### 디렉토리 권한 변경

```zsh
$ chmod 755 .
$ ls -ld .
drwxr-xr-x  5 user  staff  160 Apr  1 10:10 .
```

---

## 5. Docker 설치 및 점검

```zsh
$ docker --version
Docker version 26.x

$ docker info
Server:
 Containers: 0
 Running: 0
 Paused: 0
 Stopped: 0
```

---

## 6. Docker 기본 명령어 실행

### 이미지 확인

```zsh
$ docker images
REPOSITORY   TAG       IMAGE ID
```

### hello-world 실행

```zsh
$ docker run hello-world

Hello from Docker!
```

### Ubuntu 컨테이너 실행 및 접속

```zsh
$ docker run -it ubuntu zsh

root@container:/# ls
bin  boot  dev  etc

root@container:/# echo hello
hello
```

---

## 7. 컨테이너 운영 명령

```zsh
$ docker ps
$ docker ps -a
$ docker logs <container_id>
$ docker stats
```

---

## 8. Dockerfile 기반 커스텀 이미지

### Dockerfile

```dockerfile
FROM nginx:alpine

LABEL maintainer="user"

ENV APP_ENV=dev

COPY ./app /usr/share/nginx/html
```

### 디렉토리 구조

```
.
├── Dockerfile
└── app
    └── index.html
```

### index.html

```html
<h1>Hello Docker</h1>
```

### 이미지 빌드

```zsh
$ docker build -t my-web:1.0 .
```

### 컨테이너 실행

```zsh
$ docker run -d -p 8080:80 --name my-web my-web:1.0
```

### 접속 확인

```zsh
$ curl http://localhost:8080
<h1>Hello Docker</h1>
```

---

## 9. 포트 매핑 검증

```zsh
$ docker run -d -p 8081:80 my-web:1.0
$ curl http://localhost:8081
<h1>Hello Docker</h1>
```

포트 매핑을 통해 동일한 컨테이너 이미지를 서로 다른 포트로 접근 가능함을 확인하였다.

---

## 10. 바인드 마운트 실습

```zsh
$ docker run -d -p 8082:80 \
  -v $(pwd)/app:/usr/share/nginx/html \
  --name bind-test nginx:alpine
```

### 파일 수정 전

```zsh
$ curl http://localhost:8082
<h1>Hello Docker</h1>
```

### 파일 수정

```zsh
$ echo "<h1>Updated</h1>" > app/index.html
```

### 수정 후

```zsh
$ curl http://localhost:8082
<h1>Updated</h1>
```

---

## 11. Docker 볼륨 영속성 검증

### 볼륨 생성

```zsh
$ docker volume create mydata
```

### 컨테이너 실행 및 데이터 저장

```zsh
$ docker run -d --name vol-test -v mydata:/data ubuntu sleep infinity

$ docker exec -it vol-test zsh
# echo hello > /data/test.txt
# cat /data/test.txt
hello
```

### 컨테이너 삭제

```zsh
$ docker rm -f vol-test
```

### 재실행 후 데이터 확인

```zsh
$ docker run -d --name vol-test2 -v mydata:/data ubuntu sleep infinity

$ docker exec -it vol-test2 zsh
# cat /data/test.txt
hello
```

데이터가 유지됨을 확인하였다.

---

## 12. Git 설정 및 GitHub 연동

### Git 설정

```zsh
$ git config --global user.name "user"
$ git config --global user.email "user@example.com"

$ git config --list
user.name=user
user.email=user@example.com
```

### 저장소 초기화 및 연결

```zsh
$ git init
$ git add .
$ git commit -m "init"
```

GitHub 저장소 생성 후 원격 연결:

```zsh
$ git remote add origin <repository_url>
$ git push -u origin main
```

---

## 13. 트러블슈팅

### 문제 1: Docker 실행 불가

* 원인 가설: 시스템 권한 제한
* 확인: sudo 없이 docker 실행 실패
* 해결: OrbStack 사용으로 Docker 엔진 실행

---

### 문제 2: 포트 접속 불가

* 원인 가설: 포트 매핑 오류
* 확인: docker ps에서 포트 확인
* 해결: 올바른 포트로 재실행 (-p 옵션 수정)

---

## 14. 핵심 개념 정리

### 절대 경로 vs 상대 경로

* 절대 경로: `/Users/user/workspace`
* 상대 경로: `./workspace`

### 파일 권한

* r: read
* w: write
* x: execute

예:

* 755 → rwxr-xr-x
* 644 → rw-r--r--

### Docker 구조

* 이미지: 실행 환경 정의
* 컨테이너: 실행된 인스턴스

### 포트 매핑

* 외부 → 컨테이너 내부 연결
* 예: 8080:80

### 볼륨

* 컨테이너 외부에 데이터 저장
* 삭제 후에도 유지됨

### Git vs GitHub

* Git: 로컬 버전 관리
* GitHub: 원격 저장소 및 협업 플랫폼

---

## 15. 결론

본 미션을 통해 개발 환경 구축부터 컨테이너 기반 실행, 데이터 관리, 협업 도구 활용까지의 전체 흐름을 경험하였다.

특히 Docker를 통한 재현 가능한 실행 환경 구성과 Git을 통한 코드 관리 방식에 대한 이해를 확보하였다.

```
```
