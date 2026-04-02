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
$ mkdir -p workspace/docker-practice # mkdir = make directory / # -p = 경로에 필요한 모든 디렉토리를 한 번에 생성하는 옵션
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
-rw-r--r--  1 user  staff  0 Apr  1 10:10 test.txt
# 첫 글자는 파일 타입(- : 파일, d : 디렉토리)
# 이후 아홉 자리(rw-r--r--)는 권한을 뜻하며, 세 자리씩 나누어 각 [소유자][그룹][기타]의 권한 구조를 담당한다.```
#### r = read, w = write, x = execute

### 권한 변경

```zsh
$ chmod 755 test.txt
# chmod = change mode
# 755는 빈번하게 사용되는 권한이다. 소유자에게는 전체 권한을, 그 외에는 읽기/실행.


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
Docker version 28.5.2, build ecc6942

$ docker info
Client:
 Version:    28.5.2 # 현재 사용 중인 Docker CLI 버전
 Context:    orbstack # 어떤 Docker 환경에 연결되어 있는지(OrbStack)
 Debug Mode: false # 디버깅 로그 출력 여부 (false -> 일반 모드)
 Plugins:
  buildx: Docker Buildx (Docker Inc.) # Docker 이미지 빌드 확장 도구 / 멀티 플랫폼 빌드 가능(예: amd64, arm64)
    Version:  v0.29.1
    Path:     /Users/f22losophysics1091/.docker/cli-plugins/docker-buildx
  compose: Docker Compose (Docker Inc.) # compose : 여러 컨테이너를 한 번에 관리하는 도구 / 서비스 단위 실행 가능
    Version:  v2.40.3
    Path:     /Users/f22losophysics1091/.docker/cli-plugins/docker-compose

Server: # 실제 컨테이너를 실행하는 핵심 엔진
 Containers: 0 # 이하 현재 컨테이너 상태(하나도 없음.)
  Running: 0
  Paused: 0
  Stopped: 0
 Images: 0 # 다운로드 된 Docker 이미지 없음.
 Server Version: 28.5.2 # Docker 엔진 버전(Client와 동일)
 Storage Driver: overlay2 # 파일 저장 방식(컨테이너 파일 시스템 구현 방식), 여러 레이어를 겹쳐서 사용하는 구조(이미지 + 변경사항)
  Backing Filesystem: btrfs # 실제 디스크 파일 시스템
  Supports d_type: true # 파일 타입 정보 지원 여부 (성능/안정성 관련)
  Using metacopy: false
  Native Overlay Diff: true # 레이어 간 변경사항 비교 최적화 기능
  userxattr: false
 Logging Driver: json-file # 컨테이너 로그를 JSON 파일로 저장
 Cgroup Driver: cgroupfs
 Cgroup Version: 2
 Plugins: # Docker 기능 플러그인
  Volume: local # 기본 볼륨 저장 방식
  Network: bridge host ipvlan macvlan null overlay # 사용 가능한 네트워크 모드(bridge: 기본 네트워크 (컨테이너 간 통신), host: 호스트와 동일 네트워크, overlay: 여러 서버 간 네트워크 (클러스터), ...)
  Log: awslogs fluentd gcplogs gelf journald json-file local splunk syslog # 다양한 로그 전송 방식 지원
 CDI spec directories:
  /etc/cdi
  /var/run/cdi
 Swarm: inactive # Docker 클러스터 기능(현재 비활성화)
 Runtimes: io.containerd.runc.v2 runc # 실제로 컨테이너를 실행하는 저수준 엔진
 Default Runtime: runc
 Init Binary: docker-init
 containerd version: 1c4457e00facac03ce1d75f7b6777a7a851e5c41 # Docker 내부 구성 요소 버전
 runc version: d842d7719497cc3b774fd71620278ac9e17710e0
 init version: de40ad0
 Security Options: # 보안 설정
  seccomp # 위험한 시스템 호출 제한
   Profile: builtin
  cgroupns # 컨테이너 간 자원 격리
 Kernel Version: 6.17.8-orbstack-00308-g8f9c941121b1
 Operating System: OrbStack
 OSType: linux # macOS 위에서 Linux 커널이 실행됨 (OrbStack 내부)
 Architecture: x86_64 # CPU 아키텍처
 CPUs: 6
 Total Memory: 15.67GiB # 도커에 할당된 자원
 Name: orbstack
 ID: 575f344e-dd26-4577-8090-d43a3600d00d
 Docker Root Dir: /var/lib/docker # 이미지, 컨테이너 데이터 저장 위치
 Debug Mode: false
 Experimental: false
 Insecure Registries: # 인증 없이 접근 가능한 레지스트리
  ::1/128
  127.0.0.0/8
 Live Restore Enabled: false # Docker 재시작 시 컨테이너 유지 여부
 Product License: Community Engine
 Default Address Pools: # Docker가 내부 네트워크 생성할 때 사용하는 IP 범위
   Base: 192.168.97.0/24, Size: 24
   Base: 192.168.107.0/24, Size: 24
   Base: 192.168.117.0/24, Size: 24
   Base: 192.168.147.0/24, Size: 24
   Base: 192.168.148.0/24, Size: 24
   Base: 192.168.155.0/24, Size: 24
   Base: 192.168.156.0/24, Size: 24
   Base: 192.168.158.0/24, Size: 24
   Base: 192.168.163.0/24, Size: 24
   Base: 192.168.164.0/24, Size: 24
   Base: 192.168.165.0/24, Size: 24
   Base: 192.168.166.0/24, Size: 24
   Base: 192.168.167.0/24, Size: 24
   Base: 192.168.171.0/24, Size: 24
   Base: 192.168.172.0/24, Size: 24
   Base: 192.168.181.0/24, Size: 24
   Base: 192.168.183.0/24, Size: 24
   Base: 192.168.186.0/24, Size: 24
   Base: 192.168.207.0/24, Size: 24
   Base: 192.168.214.0/24, Size: 24
   Base: 192.168.215.0/24, Size: 24
   Base: 192.168.216.0/24, Size: 24
   Base: 192.168.223.0/24, Size: 24
   Base: 192.168.227.0/24, Size: 24
   Base: 192.168.228.0/24, Size: 24
   Base: 192.168.229.0/24, Size: 24
   Base: 192.168.237.0/24, Size: 24
   Base: 192.168.239.0/24, Size: 24
   Base: 192.168.242.0/24, Size: 24
   Base: 192.168.247.0/24, Size: 24
   Base: fd07:b51a:cc66:d000::/56, Size: 64

WARNING: DOCKER_INSECURE_NO_IPTABLES_RAW is set # 네트워크 보안 관련 경고, iptables 일부 기능 비활성화 상태
```

---

## 6. Docker 기본 명령어 실행

### 이미지 확인

```zsh
$ docker images # 내 로컬에 저장되어 있는 도커 이미지들의 목록을 보여주는 명령어
REPOSITORY   TAG       IMAGE ID
```

### hello-world 실행

```zsh
$ docker run hello-world
Unable to find image 'hello-world:latest' locally # 해당 Docker image가 없어서 공식 저장소인 인터넷(Docker Hub)에서 다운(pull).
latest: Pulling from library/hello-world
4f55086f7dd0: Pull complete
Digest: sha256:452a468a4bf985040037cb6d5392410206e47db9bf5b7278d281f94d1c2d0931
Status: Downloaded newer image for hello-world:latest # 이미지를 다 내려받았고, 그 이미지를 기반으로 컨테이너를 생성해서Create 실행Run 했음.

Hello from Docker! # 컨테이너 내부에서 실행된 프로그램이 출력한 결과물.
This message shows that your installation appears to be working correctly.

To generate this message, Docker took the following steps:
 1. The Docker client contacted the Docker daemon.
 2. The Docker daemon pulled the "hello-world" image from the Docker Hub.
    (amd64)
 3. The Docker daemon created a new container from that image which runs the
    executable that produces the output you are currently reading.
 4. The Docker daemon streamed that output to the Docker client, which sent it
    to your terminal.

# Docker Client: 우리가 터미널에 입력한 docker run 명령어를 받습니다.
# Docker Daemon: 클라이언트의 명령을 실제로 수행하는 '일꾼'입니다. 이미지가 없으면 Docker Hub에서 가져옵니다.
# Container 생성: 가져온 이미지(붕어빵 틀)를 가지고 컨테이너(붕어빵)를 만듭니다.
# 출력 전달: 컨테이너 안에서 프로그램이 실행되고, 그 결과를 다시 우리 터미널 화면으로 보여줍니다.

To try something more ambitious, you can run an Ubuntu container with:
 $ docker run -it ubuntu bash

Share images, automate workflows, and more with a free Docker ID:
 https://hub.docker.com/

For more examples and ideas, visit:
 https://docs.docker.com/get-started/
```

### Ubuntu 컨테이너 실행 및 접속

```zsh
$ docker run -it ubuntu zsh
Unable to find image 'ubuntu:latest' locally # 로컬에 우분투 이미지가 없어서 Docker Hub에서 다운로드
latest: Pulling from library/ubuntu
817807f3c64e: Pull complete 
Digest: sha256:186072bba1b2f436cbb91ef2567abca677337cfc786c86e107d25b7072feef0c
Status: Downloaded newer image for ubuntu:latest # 최신 이미지를 성공적으로 내려받음.
docker: Error response from daemon: failed to create task for container: failed to create shim task: OCI runtime create failed: runc create failed: unable to start container process: error during container init: exec: "zsh": executable file not found in $PATH # 컨테이너 내부의 환경 변수($PATH)를 다 뒤져봐도 zsh라는 실행 파일을 찾을 수 없다. ubuntu:latest라는 공식 이미지는 아주 가벼운 기본 상태로 제공된다. 이 기본 이미지 안에는 우리가 흔히 사용하는 bash 쉘은 포함되어 있지만, zsh는 기본적으로 설치되어 있지 않기 때문에 실행할 수 없는 것.

Run 'docker run --help' for more information

$ ls
Desktop		Downloads	Movies		OrbStack	Public
Documents	Library		Music		Pictures

$ echo hello
hello # echo 명령어는 터미널에서 **"입력한 문자열이나 변수의 값을 화면에 그대로 출력하라"**는 명령

# echo 활용 예시
# test.txt라는 파일을 만들고, 그 안에 'Hello'라는 내용을 넣음
# $ echo "Hello" > test.txt

# 기존 파일 내용에 이어 붙이기 (>>)
# $ echo "World" >> test.txt
```

---

## 7. 컨테이너 운영 명령

```zsh
$ docker ps # 현재 실행 중인 컨테이너들의 목록만 보여줍니다.
CONTAINER ID   IMAGE     COMMAND   CREATED   STATUS    PORTS     NAMES

$ docker ps -a # 옵션 a(=all) 실행 중인 컨테이너뿐만 아니라, 중지되었거나(Exited) 오류로 종료된 컨테이너까지 포함하여 모든 컨테이너의 목록을 보여줍니다. 내가 이전에 실행했다가 꺼버린 컨테이너들은 어디로 갔을까요? 사라진 게 아니라 도커 내부에 기록으로 남아 있습니다. 이 명령어를 쓰면 그 기록까지 전부 볼 수 있습니다.
CONTAINER ID   IMAGE         COMMAND    CREATED          STATUS                      PORTS     NAMES
eb1998fa94bb   ubuntu        "zsh"      18 minutes ago   Created                               funny_boyd
bf26a4b6348d   hello-world   "/hello"   25 minutes ago   Exited (0) 25 minutes ago             hungry_chatterjee

$ docker logs <container_id> # 특정 컨테이너 안에서 생성된 출력(로그) 기록을 가져옵니다. 컨테이너 안에서 무슨 일이 일어나고 있는지 확인하는 '블랙박스'와 같습니다.
$ docker logs hungry_chatterjee
Hello from Docker!
This message shows that your installation appears to be working correctly.

To generate this message, Docker took the following steps:
 1. The Docker client contacted the Docker daemon.
 2. The Docker daemon pulled the "hello-world" image from the Docker Hub.
    (amd64)
 3. The Docker daemon created a new container from that image which runs the
    executable that produces the output you are currently reading.
 4. The Docker daemon streamed that output to the Docker client, which sent it
    to your terminal.

To try something more ambitious, you can run an Ubuntu container with:
 $ docker run -it ubuntu bash

Share images, automate workflows, and more with a free Docker ID:
 https://hub.docker.com/

For more examples and ideas, visit:
 https://docs.docker.com/get-started/


$ docker stats 실행 중인 모든 컨테이너가 **현재 사용하고 있는 시스템 자원(CPU, 메모리, 네트워크 등)**을 실시간으로 보여줍니다.
Last login: Wed Apr  1 14:49:29 on console
f22losophysics1091@c6r5s4 ~ % docker images
REPOSITORY   TAG       IMAGE ID   CREATED   SIZE
f22losophysics1091@c6r5s4 ~ % docker run hello-world
Unable to find image 'hello-world:latest' locally
latest: Pulling from library/hello-world
4f55086f7dd0: Pull complete 
Digest: sha256:452a468a4bf985040037cb6d5392410206e47db9bf5b7278d281f94d1c2d0931
Status: Downloaded newer image for hello-world:latest

Hello from Docker!
This message shows that your installation appears to be working correctly.

To generate this message, Docker took the following steps:
 1. The Docker client contacted the Docker daemon.
 2. The Docker daemon pulled the "hello-world" image from the Docker Hub.
    (amd64)
 3. The Docker daemon created a new container from that image which runs the
    executable that produces the output you are currently reading.
 4. The Docker daemon streamed that output to the Docker client, which sent it
    to your terminal.

To try something more ambitious, you can run an Ubuntu container with:
 $ docker run -it ubuntu bash

CONTAINER ID   NAME      CPU %     MEM USAGE / LIMIT   MEM %     NET I/O   BLOCK I/O   PIDS 
```

---

## 8. Dockerfile 기반 커스텀 이미지

### Dockerfile
Dockerfile : "컨테이너를 만드는 설명서(레시피)", 어떤 OS를 쓸지, 어떤 프로그램을 설치할지, 어떻게 실행할지를 '위에서 아래로 순서대로 적는 파일'
즉, "환경 + 코드 + 실행방법"을 순서대로 쌓아 만든 이미지 설계서


이미지 : 도커파일로 완성된 실행 파일(읽기 전용)(스냅샷:어느 시점의 상태를 그대로 저장한 것)
컨테이너 : (실제로 실행된 상태)기존 OS 위에서 프로세스만 격리(같은 컴퓨터 안에서 '독립된 앱 박스' 여러 개)
기본 구조 : 레이어 구조. 레이어(스냅샷)가 쌓인 이미지. 그래서 특징은 중간 단계 캐싱됨(속도 빠름), 일부 수정해도 나머지는 재사용.

(1) 시작점
FROM(Docker 예약어이므로 관례적으로 대문자, 소문자도 동작함.) : 베이스 이미지 선택(거의 필수)

(2) 작업 환경
WORKDIR : 작업 디렉토리 설정, 이후 명령어 기준 위치

(3) 파일 넣기
COPY : 그냥 복사(기본) → “내 코드 넣자”
ADD : 압축 해제, URL가능 (잘 안 씀)

(4) 실행(빌드 시)
RUN : 이미지 만들 때 실행 / 패키지 설치, 설정 작업

(5) 실행(컨테이너 시작 시)
CMD : 기본 실행 명령(간단할 때)
ENTRYPOINT : "고정 실행"(강제 실행)

(6) 기타 중요
ENV : 


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
