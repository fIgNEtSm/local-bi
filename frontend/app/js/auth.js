// Authentication handling and JWT management
(function() {
  'use strict';

  // Wait for DOM to be ready
  function initAuth() {
    // Login form handler
    const loginForm = document.getElementById('loginForm');
    if (loginForm) {
      loginForm.addEventListener('submit', async function(e) {
        e.preventDefault();
        
        const email = document.getElementById('email').value;
        const password = document.getElementById('password').value;
        const remember = document.getElementById('remember')?.checked || false;
        
        if (!email || !password) {
          alert('Please fill in all fields');
          return;
        }

        const submitButton = loginForm.querySelector('button[type="submit"]');
        const originalText = submitButton.textContent;
        submitButton.disabled = true;
        submitButton.textContent = 'Signing in...';

        try {
          if (window.api && window.api.auth) {
            const data = await window.api.auth.login(email, password, remember);
            if (data.token) {
              window.apiUtils.setAuthToken(data.token, remember);
              alert('Login successful! Redirecting to dashboard...');
              setTimeout(() => {
                window.location.href = 'dashboard.html';
              }, 1500);
            } else {
              alert('Login failed. Please check your credentials.');
            }
          } else {
            // Fallback for demo purposes
            alert('Login successful! Redirecting to dashboard...');
            setTimeout(() => {
              window.location.href = 'dashboard.html';
            }, 1500);
          }
        } catch (error) {
          console.error('Login error:', error);
          alert('Login failed. Please try again.');
        } finally {
          submitButton.disabled = false;
          submitButton.textContent = originalText;
        }
      });
    }

    // Registration form handler
    const registerForm = document.getElementById('registerForm');
    if (registerForm) {
      registerForm.addEventListener('submit', async function(e) {
        e.preventDefault();
        
        const fullName = document.getElementById('fullName').value;
        const email = document.getElementById('email').value;
        const password = document.getElementById('password').value;
        const confirmPassword = document.getElementById('confirmPassword').value;
        const terms = document.getElementById('terms')?.checked || false;
        
        // Validation
        if (!fullName || !email || !password || !confirmPassword) {
          alert('Please fill in all fields');
          return;
        }

        if (password.length < 8) {
          alert('Password must be at least 8 characters long');
          return;
        }

        if (password !== confirmPassword) {
          alert('Passwords do not match!');
          return;
        }

        if (!terms) {
          alert('Please agree to the Terms of Service and Privacy Policy');
          return;
        }

        const submitButton = registerForm.querySelector('button[type="submit"]');
        const originalText = submitButton.textContent;
        submitButton.disabled = true;
        submitButton.textContent = 'Creating account...';

        try {
          if (window.api && window.api.auth) {
            const userData = {
              name: fullName,
              email: email,
              password: password
            };
            const data = await window.api.auth.register(userData);
            if (data.success || data.token) {
              if (data.token) {
                window.apiUtils.setAuthToken(data.token, true);
              }
              alert('Registration successful! Redirecting to login...');
              setTimeout(() => {
                window.location.href = 'login.html';
              }, 1500);
            } else {
              alert('Registration failed. Please try again.');
            }
          } else {
            // Fallback for demo purposes
            alert('Registration successful! Redirecting to login...');
            setTimeout(() => {
              window.location.href = 'login.html';
            }, 1500);
          }
        } catch (error) {
          console.error('Registration error:', error);
          alert('Registration failed. Please try again.');
        } finally {
          submitButton.disabled = false;
          submitButton.textContent = originalText;
        }
      });
    }

    // Check if user is already authenticated
    if (window.apiUtils && window.apiUtils.getAuthToken()) {
      const currentPath = window.location.pathname;
      if (currentPath.includes('login.html') || currentPath.includes('registration.html') || currentPath.endsWith('/')) {
        // Redirect to dashboard if already logged in
        window.location.href = 'dashboard.html';
      }
    }
  }

  // Handle auth status check for showing/hiding UI elements
  function checkAuthStatus() {
    const authButtons = document.getElementById('authButtons');
    const profileMenu = document.getElementById('profileMenu');
    
    if (window.apiUtils && window.apiUtils.getAuthToken()) {
      // User is logged in
      if (authButtons) authButtons.style.display = 'none';
      if (profileMenu) profileMenu.style.display = 'block';
    } else {
      // User is not logged in
      if (authButtons) authButtons.style.display = 'flex';
      if (profileMenu) profileMenu.style.display = 'none';
    }
  }

  // Initialize when DOM is ready
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', function() {
      initAuth();
      checkAuthStatus();
    });
  } else {
    initAuth();
    checkAuthStatus();
  }
})();

