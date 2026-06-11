// ==========================================
// 0. 중앙 집중식 상태(STATE) 관리 객체
// ==========================================
// 흩어진 변수들(theme, projects 데이터 등)을 하나의 객체로 관리합니다.
// 이렇게 하면 "현재 앱이 어떤 상태인가?"를 STATE 객체 하나만 보고 파악할 수 있으며,
// 추후 React의 useState와 같은 상태 관리 개념을 이해하는 강력한 기초가 됩니다.
const STATE = {
  theme: localStorage.getItem('theme') || (window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light'),
  portfolio: {
    allData: [],      // GitHub에서 가져온 원본 데이터
    filter: 'all',    // 현재 선택된 언어 필터
    status: 'idle',   // 'loading', 'success', 'error', 'empty'
    errorMsg: ''
  }
};


// ==========================================
// 1. 다크 모드 처리 (상태 기반 렌더링)
// ==========================================
const themeToggleBtn = document.getElementById('theme-toggle');
const themeIcon = themeToggleBtn.querySelector('.icon');
const htmlElement = document.documentElement;

// 테마 렌더링 함수: STATE.theme 값에 따라 화면을 업데이트
const renderTheme = () => {
  if (STATE.theme === 'dark') {
    htmlElement.setAttribute('data-theme', 'dark');
    themeIcon.textContent = '☀️';
  } else {
    htmlElement.setAttribute('data-theme', 'light');
    themeIcon.textContent = '🌙';
  }
};

// 초기 테마 렌더링
renderTheme();

// 토글 버튼 클릭 시 '상태 변경' 후 '렌더링' 호출 (단방향 데이터 흐름)
themeToggleBtn.addEventListener('click', () => {
  // 1. 상태 변경
  STATE.theme = STATE.theme === 'dark' ? 'light' : 'dark';
  localStorage.setItem('theme', STATE.theme);

  // 2. 렌더링 업데이트
  renderTheme();
});


// ==========================================
// 2. 네비게이션 및 햄버거 메뉴 처리
// ==========================================
const navToggle = document.getElementById('nav-toggle');
const navMenu = document.getElementById('nav-menu');
const navLinks = document.querySelectorAll('.nav__link');
const header = document.querySelector('.header');

navToggle.addEventListener('click', () => {
  navToggle.classList.toggle('active');
  navMenu.classList.toggle('active');
});

navLinks.forEach(link => {
  link.addEventListener('click', () => {
    navToggle.classList.remove('active');
    navMenu.classList.remove('active');
  });
});

window.addEventListener('scroll', () => {
  if (window.scrollY >= 60) {
    header.classList.add('scrolled');
  } else {
    header.classList.remove('scrolled');
  }
});


// ==========================================
// 3. 스크롤 탑 버튼
// ==========================================
const scrollTopBtn = document.getElementById('scroll-top');

window.addEventListener('scroll', () => {
  if (window.scrollY >= 300) {
    scrollTopBtn.classList.add('show');
  } else {
    scrollTopBtn.classList.remove('show');
  }
});

scrollTopBtn.addEventListener('click', (e) => {
  e.preventDefault();
  window.scrollTo({ top: 0, behavior: 'smooth' });
});


// ==========================================
// 4. 스크롤 애니메이션 (Intersection Observer)
// ==========================================
const observerOptions = { root: null, rootMargin: '0px', threshold: 0.5 };
const observer = new IntersectionObserver((entries, observer) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      entry.target.classList.add('appear');
      observer.unobserve(entry.target);
    }
  });
}, observerOptions);

document.querySelectorAll('.section__title, .about__img-wrapper, .about__info, .skills__card, .project-card, .contact__container').forEach(el => {
  el.classList.add('fade-in');
  observer.observe(el);
});


// ==========================================
// 5. 타이핑 효과 보너스 과제
// ==========================================
const typingElement = document.getElementById('typing-text');
const actualText = "안녕하세요, 저는 feelosophysics입니다.";
let charIndex = 0;

const typeText = () => {
  if (charIndex < actualText.length) {
    typingElement.textContent += actualText.charAt(charIndex);
    charIndex++;
    setTimeout(typeText, 100);
  }
};
setTimeout(typeText, 500);


// ==========================================
// 6. GitHub API 연동 및 필터링 (상태 기반 렌더링)
// ==========================================
const GITHUB_USERNAME = 'feelosophysics';
const projectsContainer = document.getElementById('projects-container');
const filterBtns = document.querySelectorAll('.filter-btn');

// UI 렌더링 함수: STATE.portfolio 상태를 바탕으로 화면을 그립니다.
const renderProjectsUI = () => {
  const { status, allData, filter, errorMsg } = STATE.portfolio;

  if (status === 'loading') {
    projectsContainer.innerHTML = '<div class="projects__loading">프로젝트를 불러오는 중입니다...</div>';
    return;
  }

  if (status === 'error') {
    projectsContainer.innerHTML = `
      <div class="projects__error">
        <p>${errorMsg}</p>
        <button class="btn btn--outline" id="retry-btn">다시 시도</button>
      </div>
    `;
    // onclick 대신 addEventListener로 이벤트 연결 (미션 제약사항 준수)
    const retryBtn = projectsContainer.querySelector('#retry-btn');
    if (retryBtn) {
      retryBtn.addEventListener('click', fetchProjects);
    }
    return;
  }

  // 필터 상태에 따라 데이터 가공
  const filteredData = filter === 'all'
    ? allData
    : allData.filter(repo => repo.language === filter);

  if (status === 'success' && filteredData.length === 0) {
    projectsContainer.innerHTML = '<div class="projects__empty">표시할 프로젝트가 없습니다.</div>';
    return;
  }

  // HTML 카드 생성
  const projectsHTML = filteredData.map(repo => {
    const description = repo.description || '프로젝트에 대한 설명이 없습니다.';
    const language = repo.language || 'Others';

    return `
      <article class="project-card fade-in appear">
        <h3><a href="${repo.html_url}" target="_blank" rel="noopener noreferrer">${repo.name}</a></h3>
        <p>${description}</p>
        <div class="project-meta">
          <span>${language}</span>
          <span>⭐ ${repo.stargazers_count}</span>
        </div>
      </article>
    `;
  }).join('');

  projectsContainer.innerHTML = projectsHTML;
};

// API 호출 함수
const fetchProjects = async () => {
  // 1. 상태 변경: 로딩 중
  STATE.portfolio.status = 'loading';
  renderProjectsUI();

  try {
    const response = await fetch(`https://api.github.com/users/${GITHUB_USERNAME}/repos?sort=updated`);
    if (!response.ok) {
      throw new Error(response.status === 403 ? 'API 호출 제한 초과' : '데이터를 불러올 수 없습니다.');
    }
    const data = await response.json();

    // 2. 상태 변경: 성공
    STATE.portfolio.allData = data.filter(repo => !repo.fork);
    STATE.portfolio.status = 'success';
    renderProjectsUI();

  } catch (error) {
    // 3. 상태 변경: 에러
    STATE.portfolio.status = 'error';
    STATE.portfolio.errorMsg = error.message;
    renderProjectsUI();
  }
};

// 필터 버튼 이벤트
filterBtns.forEach(btn => {
  btn.addEventListener('click', (e) => {
    // UI 활성화 변경
    filterBtns.forEach(b => b.classList.remove('active'));
    e.target.classList.add('active');

    // 상태 변경: 필터 값 갱신 후 렌더링
    STATE.portfolio.filter = e.target.getAttribute('data-filter');
    renderProjectsUI();
  });
});

// 앱 시작 시 데이터 로드
fetchProjects();


// ==========================================
// 7. 폼 유효성 검사 및 전송 (보너스: Formspree)
// ==========================================
const contactForm = document.getElementById('contact-form');
const nameInput = document.getElementById('name');
const emailInput = document.getElementById('email');
const messageInput = document.getElementById('message');
const formSuccess = document.getElementById('form-success');

const validateEmail = (email) => {
  return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(String(email).toLowerCase());
};

const showError = (inputElement, errorElementId, message) => {
  const errorEl = document.getElementById(errorElementId);
  inputElement.classList.add('invalid');
  errorEl.textContent = message;
  errorEl.style.display = 'block';
};

const clearError = (inputElement, errorElementId) => {
  const errorEl = document.getElementById(errorElementId);
  inputElement.classList.remove('invalid');
  errorEl.style.display = 'none';
};

contactForm.addEventListener('submit', async (e) => {
  e.preventDefault();
  let isValid = true;

  if (!nameInput.value.trim()) {
    showError(nameInput, 'name-error', '이름은 필수 항목입니다.');
    isValid = false;
  } else { clearError(nameInput, 'name-error'); }

  if (!emailInput.value.trim()) {
    showError(emailInput, 'email-error', '이메일은 필수 항목입니다.');
    isValid = false;
  } else if (!validateEmail(emailInput.value)) {
    showError(emailInput, 'email-error', '유효한 이메일 형식이 아닙니다.');
    isValid = false;
  } else { clearError(emailInput, 'email-error'); }

  if (!messageInput.value.trim()) {
    showError(messageInput, 'message-error', '메시지는 필수 항목입니다.');
    isValid = false;
  } else { clearError(messageInput, 'message-error'); }

  if (isValid) {
    try {
      const response = await fetch(contactForm.action, {
        method: 'POST',
        body: new FormData(contactForm),
        headers: { 'Accept': 'application/json' }
      });
      if (response.ok) {
        contactForm.reset();
        formSuccess.style.display = 'block';
        setTimeout(() => formSuccess.style.display = 'none', 5000);
      } else {
        alert('이메일 전송에 실패했습니다.');
      }
    } catch (error) {
      alert('네트워크 오류가 발생했습니다.');
    }
  }
});

// 실시간 유효성 검사 (input 이벤트 처리 — 미션 4-4 요구사항)
nameInput.addEventListener('input', () => {
  if (nameInput.value.trim()) {
    clearError(nameInput, 'name-error');
  }
});

emailInput.addEventListener('input', () => {
  if (emailInput.value.trim() && validateEmail(emailInput.value)) {
    clearError(emailInput, 'email-error');
  }
});

messageInput.addEventListener('input', () => {
  if (messageInput.value.trim()) {
    clearError(messageInput, 'message-error');
  }
});
