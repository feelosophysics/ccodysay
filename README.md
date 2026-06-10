# Frontend Portfolio Project (Vanilla HTML/CSS/JS)

순수 HTML, CSS, JavaScript만을 사용하여 제작한 반응형 포트폴리오 웹사이트입니다. 외부 라이브러리(React, Bootstrap, Tailwind 등)를 일절 사용하지 않고, DOM 조작과 이벤트 처리, 비동기 통신 등 웹의 동작 원리를 체득하기 위해 만들어졌습니다.

## 🚀 배포 링크

> **배포 예정** — GitHub Pages 활성화 후 아래 URL을 업데이트합니다.

- 배포 URL: `https://feelosophysics.github.io/glad/portfolio/`

## ✨ 주요 기능

| 기능 | 설명 |
|------|------|
| **시맨틱 마크업** | `header`, `nav`, `main`, `section`, `article`, `footer` 등 시맨틱 태그를 활용한 구조적 마크업 |
| **반응형 레이아웃** | CSS Flexbox와 Grid를 적극 활용, **모바일 퍼스트**(`min-width`) 미디어 쿼리 적용 |
| **다크 모드** | CSS 변수(`:root`)와 시스템 설정 감지(`prefers-color-scheme`)를 조합한 다크 모드 지원 및 상태 유지(`localStorage`) |
| **외부 API 연동** | GitHub API 비동기 호출(`fetch`, `async/await`)을 통한 프로젝트 카드 렌더링 |
| **언어별 필터링** | 가져온 저장소 목록을 언어별로 필터링 (`Array.prototype.filter`) |
| **폼 유효성 검사** | 실시간(`input` 이벤트) + 제출 시(`submit` 이벤트) 유효성 검사. Formspree 연동 |
| **스크롤 인터랙션** | Intersection Observer를 활용한 스크롤 등장 애니메이션 및 부드러운 스크롤 이동 |

## 🛠️ 기술 스택

- **HTML5** — 시맨틱 태그, 접근성(`alt`, `label`-`for` 매칭)
- **CSS3** — Variables, Flexbox, Grid, `transition`, `@keyframes`, 모바일 퍼스트 미디어 쿼리
- **JavaScript (ES6+)** — `const`/`let`, 화살표 함수, 템플릿 리터럴, 구조분해 할당, `map`/`filter`/`forEach`, `async`/`await`, Intersection Observer

## 📁 프로젝트 구조

```text
glad/portfolio/
├── index.html        # 메인 페이지 (시맨틱 마크업)
├── css/
│   └── style.css     # 전역 변수 및 스타일, 레이아웃 (모바일 퍼스트)
├── js/
│   └── main.js       # 상태 관리, DOM 제어, 비동기 API 통신
└── images/
    └── profile.jpg   # 프로필 이미지
```

## ⚙️ 인터랙션 기준값

미션 요구사항에 따라, 본 프로젝트에서 사용하는 인터랙션 기준값은 다음과 같습니다.

| 인터랙션 | 기준값 | 설명 |
|----------|--------|------|
| **스크롤 탑 버튼** | `300px` | 스크롤이 300px 이상일 때 버튼이 나타남 |
| **네비게이션 스타일 변경** | `60px` | 스크롤이 60px 이상일 때 네비게이션 배경에 `box-shadow` 추가 |
| **스크롤 애니메이션** | `threshold: 0.2` | Intersection Observer의 임계값. 요소가 20% 이상 화면에 보일 때 애니메이션 발동 |

## 🔄 상태 → 렌더링 흐름 (3가지 이상)

| # | 이벤트 | 상태 변경 | 렌더링 변화 |
|---|--------|-----------|-------------|
| 1 | 다크 모드 토글 클릭 | `STATE.theme` 변경 + `localStorage` 저장 | `data-theme` 속성 전환 → 전체 CSS 변수 적용 |
| 2 | GitHub API 호출 | `STATE.portfolio.status` (`loading`→`success`/`error`) | Projects 섹션: 로딩 스피너 → 카드 리스트 or 에러 메시지 |
| 3 | 폼 입력 (input/submit) | 각 필드의 유효성 상태 변경 | 에러 메시지 표시/숨김, `invalid` 클래스 토글 |
| 4 | 필터 버튼 클릭 | `STATE.portfolio.filter` 변경 | 프로젝트 카드 목록 필터링 재렌더링 |

## 📸 스크린샷

> **배포 후 추가 예정** — 데스크톱, 모바일, 다크 모드 스크린샷을 촬영하여 아래에 추가합니다.

| 뷰 | 스크린샷 |
|-----|----------|
| 데스크톱 (Light) | *추가 예정* |
| 모바일 (Light) | *추가 예정* |
| 다크 모드 | *추가 예정* |

## 🧠 학습 목표 및 성과

- HTML 시맨틱 태그의 접근성 및 SEO 이점 체득.
- CSS 변수를 이용한 글로벌 상태(테마) 관리 방법 이해.
- `addEventListener`를 통한 이벤트 처리와 DOM 렌더링 사이클 이해.
- 외부 API 통신 시 발생하는 4가지 상태(Loading, Success, Error, Empty)에 대한 UI 처리 완수.
- 모바일 퍼스트 반응형 디자인 접근법 실습.

---

## ✅ 미션 요구사항 체크리스트

### 4-1. 프로젝트 기본 구성
- [x] `index.html`, `css/`, `js/`, `images/` 폴더 구조 분리
- [x] 외부 스타일시트(`css/style.css`)와 JavaScript(`js/main.js`)를 HTML에 올바르게 연결
- [x] VS Code + Live Server로 실시간 개발 환경 구성

### 4-2. HTML 구조 (시맨틱 마크업)
- [x] `<header>`, `<nav>`, `<main>`, `<section>`, `<article>`, `<footer>` 시맨틱 태그 사용
- [x] Hero 섹션: 인사말(`타이핑 효과`), CTA 버튼(`View Projects`, `Contact Me`)
- [x] About 섹션: 자기소개, 프로필 이미지
- [x] Skills 섹션: 기술 스택 목록 (Frontend / Backend / Database & Tools)
- [x] Projects 섹션: GitHub API 연동 카드
- [x] Contact 섹션: 문의 폼 (이름, 이메일, 메시지)
- [x] Footer: 저작권, 소셜 링크 (GitHub)
- [x] 네비게이션에 각 섹션으로 이동하는 앵커 링크 존재
- [x] 모든 이미지에 의미있는 `alt` 속성 존재
- [x] 폼 요소에 `<label>`이 `for`-`id` 매칭으로 올바르게 연결

### 4-3. CSS 스타일링 (레이아웃 & 반응형)
- [x] 외부 스타일시트(`css/style.css`) 사용
- [x] CSS 변수(`:root`)로 색상, 폰트, 간격 정의
- [x] 다크 모드용 CSS 변수 별도 정의 (`[data-theme="dark"]`)
- [x] 네비게이션: Flexbox 사용 (로고 왼쪽, 메뉴 오른쪽)
- [x] Projects 카드: Grid 사용 (`auto-fit`, `minmax`로 반응형)
- [x] **모바일 퍼스트**(`min-width`) 미디어 쿼리 적용
- [x] 브레이크포인트: `768px` (태블릿), `1024px` (데스크톱)
- [x] 모바일에서 네비게이션 숨겨짐 + 햄버거 버튼 노출
- [x] 버튼, 카드에 `hover` 효과 + `transition` 적용
- [x] 카드에 `box-shadow` 적용

### 4-4. JavaScript 기초 (DOM & 이벤트)
- [x] JavaScript 파일을 `defer` 속성으로 연결
- [x] `var` 대신 `const`, `let`만 사용
- [x] HTML에 `onclick` 속성 미사용, `addEventListener`로 이벤트 연결
- [x] `querySelector`, `querySelectorAll`로 요소 선택
- [x] `textContent`, `innerHTML`로 내용 변경
- [x] `classList.add`, `remove`, `toggle`로 클래스 조작
- [x] `click`, `submit`, `scroll`, `input` 이벤트 처리
- [x] `event.preventDefault()`로 기본 동작 방지

### 4-5. 인터랙션 구현
- [x] **a. 햄버거 메뉴 토글**: `classList.toggle('active')` 활용
- [x] **b. 부드러운 스크롤**: `scroll-behavior: smooth` + 메뉴 클릭 시 해당 섹션 이동
- [x] **c. 스크롤 탑 버튼**: 스크롤 `300px` 이상에서 나타남, 클릭 시 페이지 최상단 이동
- [x] **d. 네비게이션 스타일 변경**: 스크롤 `60px` 이상에서 배경에 `box-shadow` 추가
- [x] **e. 다크 모드**: 토글 전환 + `localStorage` 저장으로 새로고침 후에도 유지
- [x] **f. 스크롤 애니메이션**: Intersection Observer `threshold: 0.2` 사용

### 4-6. 폼 UX
- [x] Contact 섹션에 문의 폼 존재 (이름, 이메일, 메시지)
- [x] 필수값 검증 (빈 필드 제출 불가)
- [x] 이메일 형식 검증 (정규식)
- [x] 에러 메시지가 입력 필드 근처에 표시
- [x] `event.preventDefault()`로 기본 동작 방지 + 성공 메시지 표시

### 4-7. ES6+ 문법 & 배열 메서드
- [x] 화살표 함수 활용
- [x] 템플릿 리터럴로 HTML 동적 생성
- [x] 구조분해 할당 (`const { status, allData, filter, errorMsg } = STATE.portfolio`)
- [x] `map`: GitHub 데이터 → HTML 카드 변환
- [x] `filter`: 언어별 프로젝트 필터링
- [x] `forEach`: 배열 순회 (navLinks, filterBtns 등)

### 4-8. 비동기 처리 & API 연동
- [x] `fetch` + `async/await`로 GitHub API 호출
- [x] 로딩 상태: "프로젝트를 불러오는 중입니다..." 텍스트
- [x] 성공 상태: 카드 리스트 렌더링
- [x] 에러 상태: 에러 메시지 + "다시 시도" 버튼
- [x] 빈 상태: "표시할 프로젝트가 없습니다" 메시지
- [x] `try/catch`로 에러 처리
- [x] 레이트 리밋(403) 에러 시 에러 상태 UI 표시

### 4-9. 상태 관리 패턴
- [x] "이벤트 → 상태 변경 → 화면 업데이트" 흐름 명확 (중앙 집중식 `STATE` 객체)
- [x] 상태 → 렌더링 흐름 4가지 구현 (다크 모드, API 상태, 폼 유효성, 필터)

### 4-10. 배포
- [ ] GitHub Pages 배포 (⏳ 예정)
- [ ] 배포 URL에서 모든 기능 정상 동작 확인 (⏳ 예정)
- [x] README에 프로젝트 설명, 사용 기술, 배포 URL 섹션 포함
- [ ] README에 스크린샷 포함 (⏳ 배포 후 추가 예정)

---

### 보너스 과제

- [x] **5-1. 프로젝트 필터링**: 언어별 필터링 버튼 구현 (`array.filter()` 활용)
- [x] **5-2. 타이핑 효과**: Hero 섹션에 타자기처럼 한 글자씩 나타나는 효과 구현
- [x] **5-3. 폼 실제 전송**: Formspree 연동 (⚠️ action URL을 실제 Formspree ID로 교체 필요: `https://formspree.io/f/my_form_id_here`)
- [x] **5-4. 시스템 다크 모드 감지**: `prefers-color-scheme` 미디어 쿼리로 초기 테마 자동 감지

---

## 📝 남은 작업 (TODO)

| 작업 | 상태 |
|------|------|
| Formspree에서 실제 Form ID 발급 후 `index.html`의 action URL 교체 | ⏳ |
| GitHub Pages 배포 활성화 | ⏳ |
| 데스크톱 / 모바일 / 다크모드 스크린샷 촬영 후 README에 추가 | ⏳ |
