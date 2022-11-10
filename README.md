# FII-Accident-Reconstruction

- UFOs FII IFS 솔루션 중 하나인 Accident Reconstruction 시스템

## Directory Structure

```
├── README.md
│
├── frontend
│
├── backend
│
└── boostrap
```
-----
## Gitflow Guide

### Branch guid
- branch 는 main, develop, feature branches, hotfix branches, chore branches 로 구성한다.
- feature branch와 지라 이슈는 1:1 연결되도록 생성하며, merge는 develop 브랜치로 한다.
- branch 이름은 아래의 패턴을 유지한다.
    - `topic-type/{Jira issue #}-{:desc}`
        - e.g., `feature/UF-999-test_google_api`
    - topic types
        - feature : 기능 추가
        - hotfix : 버그 수정
        - chore : 나머지 (리팩토링, 환경변수 설정, 파일 삭제 등)
- 참고 : [Git branch management](https://42dot.atlassian.net/wiki/spaces/EN/pages/105414823/Git+branch+management)


### Commit note guide
- [Conventional Commit](https://www.conventionalcommits.org/en/v1.0.0/#summary) 을 따른다.
- commit note 는 아래의 패턴을 유진한다.
    - `{commit type}: {description}`
        - e.g., `feat: geolocation mapmatching API added`
        - commit이 task랑 연결되어 있으면 `feat: [UF-999] desc` 형식으로 적어도 된다.
    - commit types
        - `fix`: A bug fix. Correlates with PATCH in SemVer
        - `feat`: A new feature. Correlates with MINOR in SemVer
        - `docs`: Documentation only changes
        - `style`: Changes that do not affect the meaning of the code (white-space, formatting, missing semi-color)
        - `refactor`: A code change that neither fixes a bug nor adds a feature
        - `perf`: A code change that improves performance
        - `test`: Adding missing or correcting existing tests
        - `build`: Changes that affect the build system or external dependencies (example scopes: pip, docker)
        - `ci`: Changes to our CI configuration files and scripts (example scopes: GitLabCI)
- commit 메세지 형식을 유지하기 위해 `commitizen`, `pre-commit` 플러그인을 사용한다.
    - `ufos-solution` 디렉토리의 터미널에서 commit 해야 commitizen 적용 가능
    - 디렉토리 안에 있는 `.pre-commit-config.yaml` 파일을 기반으로 commit 메세지 형식 검토
    - 참고 : [Git 환경설정 컨플루언스 문서](https://42dot.atlassian.net/wiki/spaces/UFII/pages/2501869793/WIP+Git)
