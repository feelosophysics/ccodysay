// ==========================================
// 1. 네비게이션 및 햄버거 메뉴 처리
// ==========================================
const navToggle = document.getElementById('nav-toggle');
const navMenu = document.getElementById('nav-menu');
const navLinks = document.querySelectorAll('.nav__link');
const header = document.querySelector('.header');

// 햄버거 버튼 클릭
navToggle.addEventListener('click', () => {
  navToggle.classList.toggle('active');
  navMenu.classList.toggle('active');
});

// 네비게이션 링크 클릭 시 메뉴 닫기 및 부드러운 스크롤
navLinks.forEach(link => {
  link.addEventListener('click', (e) => {
    // 메뉴 닫기
    navToggle.classList.remove('active');
    navMenu.classList.remove('active');

    // 부드러운 스크롤 (href 속성 활용)
    // 브라우저의 scroll-behavior: smooth 설정이 있으므로 기본 동작 유지
  });
});

// 스크롤 시 헤더 스타일 변경
window.addEventListener('scroll', () => {
  if (window.scrollY >= 60) {
    header.classList.add('scrolled');
  } else {
    header.classList.remove('scrolled');
  }
});


// ==========================================
// 2. 다크 모드 처리 (보너스: 시스템 설정 감지 포함)
// ==========================================
const themeToggleBtn = document.getElementById('theme-toggle');
const themeIcon = themeToggleBtn.querySelector('.icon');
const htmlElement = document.documentElement;

// 시스템 기본 설정 감지
const prefersDarkScheme = window.matchMedia('(prefers-color-scheme: dark)');

// 로컬 스토리지 또는 시스템 설정에 따른 초기 테마 설정
const currentTheme = localStorage.getItem('theme');
if (currentTheme === 'dark' || (!currentTheme && prefersDarkScheme.matches)) {
  htmlElement.setAttribute('data-theme', 'dark');
  themeIcon.textContent = '☀️';
} else {
  htmlElement.setAttribute('data-theme', 'light');
  themeIcon.textContent = '🌙';
}

// 다크 모드 토글 버튼 클릭 이벤트
themeToggleBtn.addEventListener('click', () => {
  let theme = htmlElement.getAttribute('data-theme');
  
  if (theme === 'dark') {
    htmlElement.setAttribute('data-theme', 'light');
    themeIcon.textContent = '🌙';
    localStorage.setItem('theme', 'light');
  } else {
    htmlElement.setAttribute('data-theme', 'dark');
    themeIcon.textContent = '☀️';
    localStorage.setItem('theme', 'dark');
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
  window.scrollTo({
    top: 0,
    behavior: 'smooth'
  });
});


// ==========================================
// 4. 스크롤 애니메이션 (Intersection Observer)
// ==========================================
const observerOptions = {
  root: null,
  rootMargin: '0px',
  threshold: 0.2 // 요소가 20% 보일 때 트리거
};

const observer = new IntersectionObserver((entries, observer) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      entry.target.classList.add('appear');
      observer.unobserve(entry.target); // 한 번만 애니메이션 실행
    }
  });
}, observerOptions);

// 애니메이션을 적용할 요소들에 클래스 추가 및 관찰 시작
document.querySelectorAll('.section__title, .about__img-wrapper, .about__info, .skills__card, .project-card, .contact__container').forEach(el => {
  el.classList.add('fade-in');
  observer.observe(el);
});


// ==========================================
// 5. 타이핑 효과 보너스 과제
// ==========================================
const typingElement = document.getElementById('typing-text');
const textToType = "Hello, I am [Name].";
// 임의로 본인 소개를 작성 (추후 수정 가능)
const actualText = "안녕하세요, 저는 feelosophysics입니다.";
let charIndex = 0;

const typeText = () => {
  if (charIndex < actualText.length) {
    typingElement.textContent += actualText.charAt(charIndex);
    charIndex++;
    setTimeout(typeText, 100); // 100ms 간격으로 글자 표시
  }
};

// 페이지 로드 후 약간의 지연 뒤 시작
setTimeout(typeText, 500);


// ==========================================
// 6. 폼 유효성 검사 및 전송 (보너스: Formspree)
// ==========================================
const contactForm = document.getElementById('contact-form');
const nameInput = document.getElementById('name');
const emailInput = document.getElementById('email');
const messageInput = document.getElementById('message');
const formSuccess = document.getElementById('form-success');

const validateEmail = (email) => {
  const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return re.test(String(email).toLowerCase());
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
  // 기본 동작(페이지 이동) 방지
  e.preventDefault();
  
  let isValid = true;
  
  // 이름 검증
  if (!nameInput.value.trim()) {
    showError(nameInput, 'name-error', '이름은 필수 항목입니다.');
    isValid = false;
  } else {
    clearError(nameInput, 'name-error');
  }
  
  // 이메일 검증
  if (!emailInput.value.trim()) {
    showError(emailInput, 'email-error', '이메일은 필수 항목입니다.');
    isValid = false;
  } else if (!validateEmail(emailInput.value)) {
    showError(emailInput, 'email-error', '유효한 이메일 형식이 아닙니다.');
    isValid = false;
  } else {
    clearError(emailInput, 'email-error');
  }
  
  // 메시지 검증
  if (!messageInput.value.trim()) {
    showError(messageInput, 'message-error', '메시지는 필수 항목입니다.');
    isValid = false;
  } else {
    clearError(messageInput, 'message-error');
  }
  
  // 유효한 경우만 전송 진행
  if (isValid) {
    try {
      const response = await fetch(contactForm.action, {
        method: 'POST',
        body: new FormData(contactForm),
        headers: {
          'Accept': 'application/json'
        }
      });
      
      if (response.ok) {
        // 성공 시 폼 초기화 및 메시지 표시
        contactForm.reset();
        formSuccess.style.display = 'block';
        setTimeout(() => {
          formSuccess.style.display = 'none';
        }, 5000);
      } else {
        alert('이메일 전송에 실패했습니다. 올바른 Formspree URL을 확인해주세요.');
      }
    } catch (error) {
      // CORS 에러나 네트워크 문제인 경우 (임시 데모용으로 성공 처리로 보여줄 수도 있음)
      console.error('Submission error:', error);
      alert('네트워크 오류가 발생했습니다.');
    }
  }
});


// ==========================================
// 7. GitHub API 연동 및 상태, 언어 필터링 보너스
// ==========================================
const GITHUB_USERNAME = 'feelosophysics';
const projectsContainer = document.getElementById('projects-container');
const filterBtns = document.querySelectorAll('.filter-btn');

let allProjects = [];

// GitHub 데이터 가져오기
const fetchProjects = async () => {
  try {
    // 1. 로딩 상태
    projectsContainer.innerHTML = '<div class="projects__loading">프로젝트를 불러오는 중입니다...</div>';
    
    const response = await fetch(`https://api.github.com/users/${GITHUB_USERNAME}/repos?sort=updated`);
    
    if (!response.ok) {
      if (response.status === 403) {
        throw new Error('API 호출 제한(Rate Limit)을 초과했습니다.');
      }
      throw new Error('프로젝트를 불러올 수 없습니다.');
    }
    
    const data = await response.json();
    
    // 포크된 레포지토리는 제외하고 직접 만든 것만 보여주기
    allProjects = data.filter(repo => !repo.fork);
    
    // 2. 성공 상태 렌더링
    renderProjects(allProjects);
    
  } catch (error) {
    // 3. 에러 상태
    projectsContainer.innerHTML = `
      <div class="projects__error">
        <p>${error.message}</p>
        <button class="btn btn--outline" onclick="fetchProjects()">다시 시도</button>
      </div>
    `;
  }
};

// 프로젝트 렌더링 함수
const renderProjects = (projects) => {
  // 4. 빈 상태
  if (projects.length === 0) {
    projectsContainer.innerHTML = '<div class="projects__empty">표시할 프로젝트가 없습니다.</div>';
    return;
  }
  
  // HTML 생성 (map 활용)
  const projectsHTML = projects.map(repo => {
    // 설명이 없을 경우 기본 텍스트
    const description = repo.description || '프로젝트에 대한 설명이 없습니다.';
    const language = repo.language || 'Others';
    
    return `
      <article class="project-card fade-in appear">
        <h3>
          <a href="${repo.html_url}" target="_blank" rel="noopener noreferrer">${repo.name}</a>
        </h3>
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

// 보너스: 언어별 필터링 기능
filterBtns.forEach(btn => {
  btn.addEventListener('click', (e) => {
    // 활성 클래스 변경
    filterBtns.forEach(b => b.classList.remove('active'));
    e.target.classList.add('active');
    
    const filterValue = e.target.getAttribute('data-filter');
    
    // 필터링 적용 (filter 활용)
    if (filterValue === 'all') {
      renderProjects(allProjects);
    } else {
      const filteredProjects = allProjects.filter(repo => 
        repo.language === filterValue
      );
      renderProjects(filteredProjects);
    }
  });
});

// 초기 데이터 로드
fetchProjects();
