# Accident Detection App

Kotlin으로 만든 Kafka Streams의 Accident Detection Lv.0의 Application

---
## 환경설정
- JDK version : [17.0.5](https://www.oracle.com/java/technologies/javase/jdk17-archive-downloads.html)
- Kafka version : [2.6.2](https://kafka.apache.org/downloads)

## 관련 링크
- Jira Issues
    - [UF-724](https://42dot.atlassian.net/browse/UF-964): Accident Reconstruction Lv.1 Project
    - [UF-900](https://42dot.atlassian.net/browse/UF-900): Accident Detection App 개발
- Confluence Pages
    - [Accident Detection Lv.0](https://42dot.atlassian.net/wiki/spaces/UFII/pages/2554462312/Accident+Detection+Lv.0)
    - [Accident Reconstruction Lv.1](https://42dot.atlassian.net/wiki/spaces/UFII/pages/2611020555/WIP+Accident+Reconstruction+Lv.1)
    - [IFS를 위한 시스템 구조 설계](https://42dot.atlassian.net/wiki/spaces/UFII/pages/2591785385/WIP+IFS)

---

## Directory Structure
```
├── README.md
│
├── src/main/kotlin/AccidentDetectionApp             <- Accident Detection Main App
│
├── .env                                             <- 환경변수
│
├── jass.conf                                        <- SASL_SSH 로그인 정보
│
```

---
## How to execute AD Lv.0
- `AccidentDetectionApp` 빌드 후 실행
