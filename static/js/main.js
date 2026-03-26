/* =============================================
   BEKIR YILMAZ - WEB DEV PORTFOLIO
   Main JavaScript
   ============================================= */

'use strict';

// ---- Hamburger Menu ----
(function () {
  const hamburger = document.getElementById('hamburger');
  const navMenu = document.getElementById('navMenu');
  if (!hamburger || !navMenu) return;

  hamburger.addEventListener('click', () => {
    const isOpen = navMenu.classList.toggle('open');
    hamburger.classList.toggle('active', isOpen);
    hamburger.setAttribute('aria-expanded', String(isOpen));
    document.body.style.overflow = isOpen ? 'hidden' : '';
  });

  // Close on nav link click
  navMenu.querySelectorAll('.navbar__link').forEach(link => {
    link.addEventListener('click', () => {
      navMenu.classList.remove('open');
      hamburger.classList.remove('active');
      hamburger.setAttribute('aria-expanded', 'false');
      document.body.style.overflow = '';
    });
  });

  // Close on outside click
  document.addEventListener('click', (e) => {
    if (!hamburger.contains(e.target) && !navMenu.contains(e.target)) {
      navMenu.classList.remove('open');
      hamburger.classList.remove('active');
      hamburger.setAttribute('aria-expanded', 'false');
      document.body.style.overflow = '';
    }
  });
})();

// ---- Sticky Navbar Shadow ----
(function () {
  const navbar = document.getElementById('navbar');
  if (!navbar) return;

  const onScroll = () => {
    navbar.classList.toggle('scrolled', window.scrollY > 20);
  };

  window.addEventListener('scroll', onScroll, { passive: true });
  onScroll();
})();

// ---- Scroll-triggered Fade-up Animations ----
(function () {
  const elements = document.querySelectorAll('.fade-up');
  if (!elements.length) return;

  const observer = new IntersectionObserver(
    (entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          entry.target.classList.add('visible');
          observer.unobserve(entry.target);
        }
      });
    },
    { threshold: 0.12, rootMargin: '0px 0px -40px 0px' }
  );

  elements.forEach(el => observer.observe(el));
})();

// ---- Smooth Scroll for Anchor Links ----
(function () {
  document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', (e) => {
      const target = document.querySelector(anchor.getAttribute('href'));
      if (!target) return;
      e.preventDefault();
      const navH = parseInt(getComputedStyle(document.documentElement).getPropertyValue('--nav-h')) || 72;
      const top = target.getBoundingClientRect().top + window.scrollY - navH - 16;
      window.scrollTo({ top, behavior: 'smooth' });
    });
  });
})();

// ---- Contact Form Validation ----
(function () {
  const form = document.getElementById('contactForm');
  if (!form) return;

  const showError = (fieldId, msg) => {
    const input = document.getElementById(fieldId);
    const error = document.getElementById(fieldId + 'Error');
    if (input) input.classList.add('error');
    if (error) error.textContent = msg;
  };

  const clearError = (fieldId) => {
    const input = document.getElementById(fieldId);
    const error = document.getElementById(fieldId + 'Error');
    if (input) input.classList.remove('error');
    if (error) error.textContent = '';
  };

  // Live validation
  ['isim', 'eposta', 'mesaj'].forEach(id => {
    const el = document.getElementById(id);
    if (el) el.addEventListener('input', () => clearError(id));
  });

  form.addEventListener('submit', (e) => {
    let valid = true;

    const isim = document.getElementById('isim');
    const eposta = document.getElementById('eposta');
    const mesaj = document.getElementById('mesaj');

    if (isim && !isim.value.trim()) {
      showError('isim', 'Lütfen adınızı ve soyadınızı girin.');
      valid = false;
    }

    if (eposta) {
      const emailVal = eposta.value.trim();
      if (!emailVal) {
        showError('eposta', 'Lütfen e-posta adresinizi girin.');
        valid = false;
      } else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(emailVal)) {
        showError('eposta', 'Geçerli bir e-posta adresi girin.');
        valid = false;
      }
    }

    if (mesaj && mesaj.value.trim().length < 10) {
      showError('mesaj', 'Mesajınız en az 10 karakter olmalıdır.');
      valid = false;
    }

    if (!valid) {
      e.preventDefault();
      return;
    }

    // Show loading state
    const btn = document.getElementById('submitBtn');
    if (btn) {
      btn.disabled = true;
      btn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Gönderiliyor...';
    }
  });
})();

// ---- Active Nav Link Based on Current Path ----
(function () {
  // Already handled server-side via Jinja, but ensure hash links work
  const path = window.location.pathname;
  document.querySelectorAll('.navbar__link').forEach(link => {
    const href = link.getAttribute('href');
    if (href && href !== '/' && path.startsWith(href)) {
      link.classList.add('active');
    } else if (href === '/' && path === '/') {
      link.classList.add('active');
    }
  });
})();

// ---- Auto-dismiss Flash Messages ----
(function () {
  document.querySelectorAll('.flash').forEach(flash => {
    setTimeout(() => {
      flash.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
      flash.style.opacity = '0';
      flash.style.transform = 'translateX(100%)';
      setTimeout(() => flash.remove(), 500);
    }, 5000);
  });
})();
