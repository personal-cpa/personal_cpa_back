# 🚀 Personal CPA Application

TBD

## 📚 프로젝트 문서

- [설계 문서](doc/design.md) - 프로젝트 아키텍처 및 기술 스택

## ✨ 주요 기능

TBD

## 🛠️ 기술 스택

### 프론트엔드

TBD

### 백엔드

- Python
    - FastAPI

## 🏗 시스템 아키텍처

TBD

## 🔄 시스템 상호작용

TBD

## 📦 프로젝트 구조

```
personal_cpa/            # 리포지토리 루트
├── personal_cpa/        # 실제 패키지 코드 (프로젝트명과 동일한 폴더)
│   ├── __init__.py
│   ├── main.py             # FastAPI 진입점 등
│   ├── ledger/             # 원장(ledger) 기능 관련 디렉터리
│   │   ├── __init__.py
│   │   ├── domain/
│   │   ├── use_cases/
│   │   ├── interfaces/
│   │   └── ...
│   ├── report/             # 보고서(report) 기능 관련
│   │   ├── __init__.py
│   │   ├── domain/
│   │   ├── use_cases/
│   │   ├── interfaces/
│   │   └── ...
│   ├── core/               # 공통(core) 모듈 (DB, config 등)
│   │   ├── __init__.py
│   │   ├── config.py
│   │   └── database.py
│   └── ...
├── tests/                  # 테스트용 폴더
│   ├── __init__.py
│   ├── test_main.py
│   ├── ledger/
│   │   └── test_create_account.py
│   └── report/
│       └── test_report_api.py
├── pyproject.toml          # 프로젝트 메타데이터 (Poetry / PEP 621)
├── requirements.txt        # (Poetry 대신 pip 사용 시)
├── Dockerfile
├── docker-compose.yml
├── .gitignore
└── README.md
```

## 🚀 시작하기

### 사전 요구사항

- pyenv, virtualenv 설치
    - Python 3.13.1 버전 설치

```bash
pyenv install 3.13.1
pyenv virtualenv 3.13.1 personal_cpa
pyenv activate personal_cpa
```

### 설치 방법

1. 저장소 클론
```bash
git clone https://github.com/personal-cpa/personal_cpa.git
cd personal_cpa
```

2. 백엔드 배포

TBD

3. 프론트엔드 실행

TBD

## 🌳 브랜치 관리

이 프로젝트는 [GitHub Flow](https://guides.github.com/introduction/flow/) 브랜치 전략을 따릅니다.

### 브랜치 전략 다이어그램

```mermaid
gitGraph
    commit
    branch develop
    checkout develop
    commit
    branch feature/login
    checkout feature/login
    commit
    checkout develop
    merge feature/login
    branch feature/todo-list
    checkout feature/todo-list
    commit
    checkout develop
    merge feature/todo-list
    commit  %% develop에 추가 커밋 추가
    branch release/25.3.1
    checkout release/25.3.1
    merge develop
    checkout main
    merge release/25.3.1
    branch bugfix/auth-error
    checkout bugfix/auth-error
    commit
    checkout main
    merge bugfix/auth-error
```

### 주요 브랜치
- `main`: Production에 배포되어 서비스되는 브랜치
- `develop`: 개발환경에서 테스트가 완료된 코드를 관리하는 브랜치 (base: `main`)
- `release/*`: 배포 준비를 위한 브랜치 (base: `develop`)
- `feature/*`: 새로운 기능 개발을 위한 브랜치 (base: `develop`)
- `bugfix/*`: 버그 수정을 위한 브랜치 (base: `develop`)

### 브랜치 네이밍 규칙
- 기능 개발: `feature/login`, `feature/todo-list`
- 버그 수정: `bugfix/auth-error`, `bugfix/api-timeout`
- 배포 준비: `release/v25.3.1` (year.month.patch)

### 작업 프로세스
1. 새로운 작업 시작
   ```bash
   git checkout develop
   git pull origin develop
   git checkout -b feature/new-feature
   ```

2. 작업 중 주기적인 커밋
   ```bash
   git add .
   git commit -m "feat: 새로운 기능 구현"
   git push origin feature/new-feature
   ```

3. Pull Request 생성 및 리뷰
   - GitHub에서 Pull Request 생성
   - 코드 리뷰 진행
   - CI/CD 파이프라인 통과 확인

4. 작업 완료 및 병합
   ```bash
   # GitHub UI에서 "Merge pull request" 버튼 클릭
   git checkout develop
   git pull origin develop
   ```

### Pull Request 규칙
1. 제목 형식: `[Github Issue 번호] 작업 내용 요약`
   - 예: `[#1 - feat] 로그인 기능 구현`
   - 예: `[#2 - fix] 인증 오류 수정`

2. 타입 분류
   - `feat`: 새로운 기능
   - `fix`: 버그 수정
   - `docs`: 문서 수정
   - `style`: 코드 포맷팅
   - `refactor`: 코드 리팩토링
   - `test`: 테스트 코드
   - `chore`: 기타 작업

3. PR 템플릿

[PR 템플릿](.github/ISSUE_TEMPLATE/feature.md)

## 🤝 기여하기

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request
