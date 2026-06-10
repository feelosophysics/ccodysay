# 극한 상세 학습 가이드: 바닐라 JS 포트폴리오 (현미경 해부 버전)

초심자의 시선에 맞춰, 단 하나의 속성이나 태그도 건너뛰지 않고 "이 코드가 왜 여기 있어야 하는가"를 완전히 파헤칩니다. 전체 코드를 기능(섹션) 단위로 묶어 HTML(뼈대) $\rightarrow$ CSS(옷) $\rightarrow$ JS(동작) 순으로 하나하나 뜯어봅니다.

---

## 🗺️ 리팩토링된 전체 학습 로드맵 (기능/섹션 중심)

*모든 챕터는 해당 기능과 관련된 HTML, CSS, JS 코드를 한 호흡에 묶어서 분석합니다.*

1. **Chapter 1: 웹의 기반 다지기 (사전 준비와 전역 설정)** 👈 [현재 진행 파트 (1/3)]
   - **HTML**: 문서 선언, `<head>` 안의 모든 `<meta>` 속성, 구글 폰트 불러오기(`<link>`) 완벽 해부.
   - **CSS**: 모든 브라우저의 기본 여백을 없애는 Reset CSS, 테마를 결정하는 `:root` 변수 선언.

2. **Chapter 2: 길잡이 만들기 (헤더와 네비게이션 바)** 👈 [현재 진행 파트 (1/3)]
   - **HTML**: `<header>`, `<nav>`, `<ul>`, `<li>`, `<a>` 태그의 상하관계와 `href="#home"`의 작동 원리.
   - **CSS**: Flexbox를 이용한 메뉴 좌우 끝 정렬, 스크롤 시 생기는 그림자 효과.
   - **JS**: 모바일 햄버거 메뉴를 클릭했을 때 메뉴가 튀어나오는 `classList.toggle` 원리.

3. **Chapter 3: 첫인상과 테마 변경 (히어로 섹션 & 다크 모드)**
   - 다크 모드가 어떻게 HTML `data-theme` 속성과 CSS, JS `localStorage`를 거쳐 동작하는지.
   - 타이핑 효과를 만드는 자바스크립트 `setTimeout` 함수의 원리.

4. **Chapter 4: 나를 소개하다 (About & Skills 섹션)**
   - 이미지 태그 `<img src alt>`의 의미.
   - 반응형 디자인의 꽃, CSS Grid(`repeat`, `auto-fit`, `minmax`)를 이용해 카드를 배치하는 완벽한 공식.

5. **Chapter 5: 내 작업물 자랑하기 (Projects 섹션 & GitHub API)**
   - **JS**: `fetch`와 `async/await`를 통해 GitHub 저장소 데이터를 훔쳐(?)오는 과정.
   - **JS**: `map`으로 HTML 카드를 만들어내고, `filter`로 JavaScript, Python 등 언어별 버튼 클릭 시 걸러내는 마법.

6. **Chapter 6: 문의 받기 (Contact Form & Footer)**
   - **HTML**: `<form>`, `<input>`, `<textarea>`, `<label for="">` 태그의 속성들.
   - **JS**: 사용자가 이름을 안 썼거나 이메일 형식이 틀렸을 때 경고를 띄우는 폼 유효성 검사 원리.
   - **JS**: Formspree를 이용해 내 이메일로 진짜 메시지를 보내는 원리.

---

## 📖 Chapter 1: 웹의 기반 다지기 (사전 준비와 전역 설정)

이 웹사이트를 열자마자 보이지 않는 곳에서 브라우저가 무슨 일을 하는지, `index.html` 최상단 코드를 모두 해부합니다.

### 1-1. 문서의 시작과 신분증 (`index.html`)

```html
<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Portfolio - feelosophysics</title>
```

#### 🔬 현미경 분석 (한 줄도 빠짐없이)
- `<!DOCTYPE html>`: 브라우저(크롬 등)에게 "이 문서는 10년 전 옛날 문법이 아니라, 최신 규격인 **HTML5**로 작성되었어. 최신 방식으로 읽어줘!"라고 알려주는 선언문입니다. 이 태그가 없으면 브라우저가 화면을 이상하게 그릴 수 있습니다(호환성 모드).
- `<html lang="ko">`: HTML 문서의 진짜 시작점입니다. `lang="ko"`는 Language(언어)가 Korean(한국어)이라는 뜻입니다. 시각장애인용 화면 낭독기가 이 문서를 읽을 때 "아, 한국어 발음 엔진으로 읽어야겠구나" 하고 판단하게 돕습니다.
- `<head>`: 브라우저 탭 이름, 폰트, 검색 엔진 설정 등 **화면에는 안 보이지만 페이지에 꼭 필요한 설정**들을 담는 그릇입니다.
- `<meta charset="UTF-8">`: `meta`는 문서의 정보(데이터)를 의미합니다. `charset`은 Character Set(문자 집합)의 약자입니다. `UTF-8`은 전 세계 모든 언어와 이모티콘(😊)을 깨지지 않고 보여주는 만능 번역기 규칙입니다. 이걸 안 쓰면 한글이 "웗꿳"하고 깨집니다.
- `<meta name="viewport" content="width=device-width, initial-scale=1.0">`: **반응형 웹을 위한 절대 반지**입니다.
  - `viewport`: 스마트폰 화면에서 보이는 영역을 뜻합니다.
  - `width=device-width`: "웹사이트의 가로 너비를 네가 지금 보고 있는 기기(스마트폰, 태블릿)의 가로 너비와 똑같이 맞춰라"라는 뜻입니다.
  - `initial-scale=1.0`: "처음 들어왔을 때 화면 확대/축소 비율을 무조건 1배율(기본)로 해라."
- `<title>`: 브라우저 탭 맨 위에 뜨는 이름이자, 즐겨찾기를 할 때 저장되는 이름입니다.

### 1-2. 외부 자원 끌어오기 (폰트와 파일 연결)

```html
  <!-- 폰트 추가: 구글 폰트 (Inter) -->
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
  
  <link rel="stylesheet" href="css/style.css">
  <script src="js/main.js" defer></script>
</head>
```

#### 🔬 현미경 분석
이 부분은 질문에서 특히 궁금해하셨던, 내 컴퓨터 밖(구글 서버)에서 무언가를 가져오는 마법의 통로입니다.

- `<link>` 태그: 현재 HTML 문서와 외부 문서(폰트 파일, CSS 파일 등)를 **연결(Link)**해주는 태그입니다.
- `<link rel="preconnect" href="https://fonts.googleapis.com">`
  - `rel="preconnect"`: relation(관계)가 preconnect(미리 연결)라는 뜻입니다. 
  - `href`: Hypertext Reference의 약자로, 연결할 주소입니다.
  - **해석**: 브라우저야, 이따가 내가 구글 서버(`https://fonts.googleapis.com`)에서 폰트를 다운받을 건데, 시간 아까우니까 **미리 서버랑 몰래 연결선부터 꽂아놔!** (로딩 속도 최적화 기술입니다).
- `<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>`
  - `fonts.gstatic.com`은 구글이 실제 폰트 파일을 쟁여두는 진짜 창고 주소입니다.
  - `crossorigin`: 내 웹사이트 도메인(예: naver.com)과 구글 서버의 도메인이 서로 다르지만(Cross Origin), 폰트를 가져오는 걸 허락해달라는 보안 통과 암호입니다.
- `<link href="...Inter:wght@400;500..." rel="stylesheet">`
  - 이제 미리 선을 꽂아둔 구글 창고에서 진짜로 `Inter`라는 이름의 폰트를 굵기별(400, 500, 600, 700)로 다운로드해 옵니다. `rel="stylesheet"`는 가져오는 이 파일이 디자인을 담당하는 스타일시트 파일임을 알립니다.
- `<link rel="stylesheet" href="css/style.css">`: 내가 직접 만든 CSS 파일에 연결합니다.
- `<script src="js/main.js" defer></script>`: 내가 만든 자바스크립트 파일(`src`: Source)을 불러옵니다. **`defer`**는 "HTML 뼈대 그림을 끝까지 다 그리고 나서 이 자바스크립트를 실행해!"라는 아주 중요한 지시어입니다.

### 1-3. 초기화와 변수 세팅 (`style.css` 도입부)

CSS 파일의 첫 부분에서는 모든 브라우저가 멋대로 가진 기본 여백을 청소하고, 프로젝트 전체에서 쓸 색상 변수를 만듭니다.

```css
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

:root {
  --color-bg: #fffbf7;
  --font-main: 'Inter', sans-serif;
}
```

#### 🔬 현미경 분석
- `*` (별표): "HTML 문서 안에 있는 **모~든 태그**야 내 말 들어라"라는 뜻입니다.
- `margin: 0; padding: 0;`: 크롬, 사파리 등은 기본적으로 태그마다 약간의 띄어쓰기(여백)를 몰래 가지고 있습니다. 이걸 0으로 싹 다 청소(초기화)해야 우리가 원하는 대로 정확히 디자인을 얹을 수 있습니다.
- `box-sizing: border-box;`: 매우 중요한 공식입니다! 가로 너비를 100px로 줬는데 테두리(border)를 5px 주면 전체 크기가 110px로 뚱뚱해지는 현상을 막아줍니다. "테두리를 포함해서 무조건 전체 너비를 100px로 꽉 맞춰라"라는 마법의 코드입니다.
- `:root`: 이 웹사이트의 최상위 뿌리를 말합니다.
- `--color-bg: #fffbf7;`: 이름 앞에 `--`를 붙이면 CSS 안에서 언제든 재사용할 수 있는 **변수**가 됩니다. 나중에 배경색을 바꿀 때, 수백 줄의 CSS를 다 고칠 필요 없이 여기서 `#fffbf7` 하나만 고치면 사이트 전체의 배경색이 싹 바뀝니다.
- `var(--color-bg)`: 나중에 CSS 파일 아래쪽에서 변수 값을 쓸 때 이렇게 꺼내 씁니다.


---

## 📖 Chapter 2: 길잡이 만들기 (헤더와 네비게이션 바)

이제 본격적으로 화면 상단에 찰싹 붙어있는 메뉴바(네비게이션)가 어떻게 구조를 잡고 디자인되는지 파헤칩니다.

### 2-1. 네비게이션 바의 HTML 구조 (`index.html`)

```html
<header class="header">
  <nav class="nav container">
    <a href="#" class="nav__logo">Dev.feel</a>
    
    <div class="nav__menu" id="nav-menu">
      <ul class="nav__list">
        <li class="nav__item"><a href="#home" class="nav__link">Home</a></li>
        <li class="nav__item"><a href="#about" class="nav__link">About</a></li>
      </ul>
    </div>
  </nav>
</header>
```

#### 🔬 현미경 분석
- `<header>`: 머리말을 뜻하는 시맨틱 태그입니다. 로봇(검색 엔진)이 "아, 여기가 사이트의 간판 메뉴 영역이구나"라고 인식합니다. `class="header"`를 달아서 나중에 CSS로 디자인할 이름표를 붙여줬습니다.
- `<nav>`: Navigation(조종/탐색)의 약자입니다. 다른 페이지나 섹션으로 이동하는 링크들의 묶음을 감쌀 때 쓰는 태그입니다. `container`라는 클래스를 하나 더 달았는데, 이는 콘텐츠가 화면 양옆 끝에 너무 딱 달라붙지 않게 가운데로 모아주는 상자 역할을 합니다.
- `<a href="#" class="nav__logo">`: `<a>`는 닻(Anchor)을 의미하며 링크를 만듭니다. `href="#"`는 "클릭해도 다른 페이지로 가지 말고 지금 페이지의 맨 위로 가라"는 뜻입니다. 로고를 누르면 보통 화면 맨 위로 가니까요.
- `<ul>`과 `<li>`: 메뉴 항목들을 만들 때 쓰는 세트 메뉴입니다.
  - `<ul>`: Unordered List (순서가 없는 목록). 메뉴 1, 메뉴 2를 묶는 큰 포장지입니다.
  - `<li>`: List Item (목록 항목). 포장지 안의 알맹이(Home, About 등) 하나하나입니다. 왜 굳이 이렇게 쓰냐면, 메뉴라는 것이 본질적으로 '항목들의 목록'이기 때문입니다. 로봇이 이 코드를 보면 "아, 이 사이트는 메뉴가 5개인 목록이구나" 하고 정확히 파악합니다.
- `<a href="#home">Home</a>`: 이 버튼을 클릭하면, 페이지에서 `<section id="home">`이라는 이름표가 붙은 곳으로 화면이 스크롤되어 내려갑니다! `id`를 찾아가는 앵커 링크의 마법입니다.

### 2-2. 네비게이션 바를 양옆으로 찢는 CSS 마법 (`style.css`)

HTML만 적어두면 메뉴가 아래로 한 줄씩 못생기게 나열됩니다. 이를 멋지게 가로로 배치하는 것이 CSS Flexbox입니다.

```css
.nav {
  display: flex;
  justify-content: space-between;
  align-items: center;
  height: 100%;
}

.nav__list {
  display: flex;
  gap: 2rem;
}
```

#### 🔬 현미경 분석
- `.nav`: CSS에서 쩜(`.`)은 클래스(이름표)를 부르는 말입니다. 즉, HTML의 `<nav class="nav">`를 부릅니다.
- `display: flex;`: **"네 안에 있는 자식 요소들을 가로 1차원으로 쫙 배열하겠다!"**라는 뜻입니다. 이 순간 묶여있던 로고, 메뉴 뭉치, 다크모드 버튼 뭉치가 가로로 정렬됩니다.
- `justify-content: space-between;`: Flexbox의 핵심입니다. 가로축 정렬을 결정하는데, `space-between`은 요소들 사이(between)에 공간(space)을 줘서 **자석의 같은 극처럼 양쪽 끝으로 쫘아악 밀어버립니다.** (왼쪽 끝엔 로고, 오른쪽 끝엔 메뉴).
- `align-items: center;`: 세로축 정렬입니다. 로고 글씨와 메뉴 글씨의 높낮이가 약간 달라도, 정확히 한가운데에 꼬치처럼 중심을 꽂아서 맞춰줍니다.
- `.nav__list`: 메뉴 알맹이(`<li>`들)를 묶고 있는 `<ul>` 태그입니다. 이 녀석에게도 `display: flex;`를 주면 세로로 나오던 Home, About 글씨들이 가로로 배치됩니다.
- `gap: 2rem;`: 메뉴 사이사이의 간격을 띄워줍니다. (`margin`을 일일이 안 줘도 알아서 사이를 띄우는 꿀 기능입니다).

> 여기까지가 재설계된 1/3 분량입니다. HTML 파일의 구글 폰트 로드 부분부터, 네비게이션 `ul li` 구조, 그리고 CSS Flexbox를 통한 정렬까지, **왜 이 코드가 거기에 있어야 하는지 단 하나도 빠짐없이** 현미경처럼 들여다보았습니다.
> 이런 방식의 설명이 이제 코드 전체를 명확히 이해하시는데 도움이 되셨나요? 피드백을 주시면 계속해서 남은 로드맵(히어로 섹션의 다크모드/타이핑 효과 등)을 같은 깊이로 진행하겠습니다!
