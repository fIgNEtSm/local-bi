// app-medium.js — medium feature set: hover + click + tooltip (no export/debug)
(function () {
  'use strict';

  const $ = (sel, ctx = document) => ctx.querySelector(sel);
  const $$ = (sel, ctx = document) => Array.from((ctx || document).querySelectorAll(sel));
  const on = (el, ev, fn) => el && el.addEventListener(ev, fn);

  // Small tooltip manager (lightweight)
  function createTooltip() {
    const tip = document.createElement('div');
    tip.className = 'dashboard-tooltip';
    tip.style.position = 'fixed';
    tip.style.pointerEvents = 'none';
    tip.style.padding = '6px 8px';
    tip.style.borderRadius = '6px';
    tip.style.zIndex = 9999;
    tip.style.fontSize = '0.85rem';
    tip.style.background = 'rgba(8,10,14,0.88)';
    tip.style.color = '#fff';
    tip.style.transition = 'opacity .12s ease';
    tip.style.opacity = '0';
    document.body.appendChild(tip);

    let hideTimer = null;
    return {
      show(text, x, y) {
        clearTimeout(hideTimer);
        tip.textContent = text;
        tip.style.left = (x + 12) + 'px';
        tip.style.top = (y + 12) + 'px';
        tip.style.opacity = '1';
      },
      move(x, y) {
        tip.style.left = (x + 12) + 'px';
        tip.style.top = (y + 12) + 'px';
      },
      hide(delay = 80) {
        clearTimeout(hideTimer);
        hideTimer = setTimeout(() => tip.style.opacity = '0', delay);
      },
      destroy() {
        tip.remove();
      }
    };
  }

  const tooltip = createTooltip();

  /* -----------------------------
     Sentiment (pie + legend) interactions
     ----------------------------- */
  function initSentiment() {
    const container = document.querySelector('.sentiment-pie');
    if (!container) return;

    const pie = container.querySelector('.pie');
    const legendItems = Array.from(container.querySelectorAll('.legend li'));

    // Make legend items keyboard-focusable
    legendItems.forEach((li, i) => {
      if (!li.hasAttribute('tabindex')) li.setAttribute('tabindex', '0');
      li.dataset.index = String(i);
      li.setAttribute('role', 'button');
      li.setAttribute('aria-pressed', 'false');
    });

    // Add hover/focus handlers to container to affect pie
    const enter = () => pie && pie.classList.add('is-hover');
    const leave = () => { pie && pie.classList.remove('is-hover'); tooltip.hide(); };

    on(container, 'mouseenter', enter);
    on(container, 'mouseleave', leave);
    on(container, 'focusin', enter);
    on(container, 'focusout', (e) => {
      if (!container.contains(e.relatedTarget)) leave();
    });

    // Legend item behavior: tooltip + toggle selected + highlight pie segment
    legendItems.forEach((li, index) => {
      on(li, 'mouseenter', (ev) => {
        li.classList.add('hovered');
        pie.classList.add(`segment-${index}`);
        const text = li.textContent.trim() || 'item';
        tooltip.show(text, ev.clientX, ev.clientY);
      });

      on(li, 'mousemove', (ev) => tooltip.move(ev.clientX, ev.clientY));

      on(li, 'mouseleave', () => {
        li.classList.remove('hovered');
        pie.classList.remove(`segment-${index}`);
        tooltip.hide();
      });

      on(li, 'click', () => {
        // toggle selected
        const isSelected = li.classList.toggle('selected');
        li.setAttribute('aria-pressed', String(Boolean(isSelected)));
        // place to add filtering logic later
      });

      on(li, 'keydown', (ev) => {
        if (ev.key === 'Enter' || ev.key === ' ') {
          ev.preventDefault();
          li.click();
        }
      });
    });

    // Make pie focusable and manageable by keyboard (optional toggle)
    if (pie) {
      pie.setAttribute('tabindex', '0');
      pie.setAttribute('role', 'button');
      on(pie, 'keydown', (ev) => {
        if (ev.key === 'Enter' || ev.key === ' ') {
          ev.preventDefault();
          pie.classList.toggle('is-active');
        }
      });
    }
  }

  /* -----------------------------
     Stat-card interactions (click + keyboard)
     ----------------------------- */
  function initStatCards() {
    const cards = $$('.stat-card');
    cards.forEach(card => {
      if (!card.hasAttribute('tabindex')) card.setAttribute('tabindex', '0');
      card.setAttribute('role', 'button');
      card.setAttribute('aria-pressed', 'false');

      const toggle = () => {
        const pressed = card.getAttribute('aria-pressed') === 'true';
        card.setAttribute('aria-pressed', String(!pressed));
        card.classList.toggle('active', !pressed);
        // place to add card-specific action later
      };

      on(card, 'click', toggle);
      on(card, 'keydown', (ev) => {
        if (ev.key === 'Enter' || ev.key === ' ') {
          ev.preventDefault();
          toggle();
        }
      });
    });
  }

  /* -----------------------------
     Trend chart mouse tracking
     ----------------------------- */
  function initTrendChart() {
    const trendChart = $('.trend-chart');
    if (!trendChart) return;

    const svg = trendChart.querySelector('svg');
    if (!svg) return;

    on(trendChart, 'mousemove', (ev) => {
      const rect = trendChart.getBoundingClientRect();
      const x = ev.clientX - rect.left;
      const percent = (x / rect.width) * 100;
      
      trendChart.style.setProperty('--mouse-x', percent + '%');
      trendChart.classList.add('mouse-active');
    });

    on(trendChart, 'mouseleave', () => {
      trendChart.classList.remove('mouse-active');
    });
  }

  /* -----------------------------
     Init
     ----------------------------- */
  function init() {
    initSentiment();
    initStatCards();
    initTrendChart();
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }

  // expose for minimal debugging in console
  window.__appMedium = { tooltip };
})();




/*login-registration - css*/


      document.getElementById('loginForm').addEventListener('submit', function(e) {
        e.preventDefault();
        
        // Here you would typically send the data to your backend
        const email = document.getElementById('email').value;
        const password = document.getElementById('password').value;
        
        // Simulate login (replace with actual API call)
        if (email && password) {
          alert('Login successful! Redirecting to dashboard...');
          setTimeout(() => {
            // Redirect to your dashboard
            window.location.href = 'my-app/index.html';
          }, 1500);
        }
      });
   

     
  
      document.getElementById('registerForm').addEventListener('submit', function(e) {
        e.preventDefault();
        
        const password = document.getElementById('password').value;
        const confirmPassword = document.getElementById('confirmPassword').value;
        
        if (password !== confirmPassword) {
          alert('Passwords do not match!');
          return;
        }
        
        // Here you would typically send the data to your backend
        alert('Registration successful! Redirecting to login...');
        setTimeout(() => {
          window.location.href = 'login.html';
        }, 1500);
      });
 
   


      