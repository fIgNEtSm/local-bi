// Business form handling
(function() {
  'use strict';

  // Initialize business form
  document.addEventListener('DOMContentLoaded', function() {
    const businessForm = document.getElementById('businessForm');
    
    if (businessForm) {
      businessForm.addEventListener('submit', handleBusinessFormSubmit);
    }
  });

  // Handle business form submission
  async function handleBusinessFormSubmit(event) {
    event.preventDefault();
    
    const form = event.target;
    const submitButton = form.querySelector('.btn-submit');
    const originalButtonText = submitButton.textContent;
    
    // Get form data
    const formData = new FormData(form);
    const data = Object.fromEntries(formData.entries());
    
    // Validate form data
    if (!validateBusinessForm(data)) {
      return;
    }
    
    // Show loading state
    submitButton.disabled = true;
    submitButton.textContent = 'Sending...';
    
    try {
      // Send data to backend
      const response = await fetch(`${window.CONFIG.API_BASE_URL}/business`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${window.apiUtils.getAuthToken()}`
        },
        body: JSON.stringify(data)
      });
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      
      const result = await response.json();
      
      // Show success message
      showNotification('Business information submitted successfully!', 'success');
      
      // Reset form
      form.reset();
      
      // Redirect to dashboard after successful submission
      setTimeout(() => {
        window.location.href = 'dashboard.html';
      }, 2000);
      
    } catch (error) {
      console.error('Error submitting business form:', error);
      showNotification('Failed to submit business information. Please try again.', 'error');
    } finally {
      // Reset button state
      submitButton.disabled = false;
      submitButton.textContent = originalButtonText;
    }
  }

  // Validate business form data
  function validateBusinessForm(data) {
    const errors = [];
    
    // Validate required fields
    if (!data.firstName || data.firstName.trim().length < 2) {
      errors.push('First name must be at least 2 characters long');
    }
    
    if (!data.lastName || data.lastName.trim().length < 2) {
      errors.push('Last name must be at least 2 characters long');
    }
    
    if (!data.website || !isValidUrl(data.website)) {
      errors.push('Please enter a valid website URL');
    }
    
    if (!data.businessType) {
      errors.push('Please select a business type');
    }
    
    // Show errors if any
    if (errors.length > 0) {
      showNotification(errors.join('\n'), 'error');
      return false;
    }
    
    return true;
  }

  // Validate URL format
  function isValidUrl(string) {
    try {
      const url = new URL(string);
      return url.protocol === 'http:' || url.protocol === 'https:';
    } catch (_) {
      return false;
    }
  }

  // Show notification message
  function showNotification(message, type = 'info') {
    // Create notification element
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.textContent = message;
    
    // Add styles
    Object.assign(notification.style, {
      position: 'fixed',
      top: '20px',
      right: '20px',
      padding: '12px 20px',
      borderRadius: '8px',
      color: 'white',
      fontWeight: '500',
      zIndex: '9999',
      opacity: '0',
      transform: 'translateX(100%)',
      transition: 'all 0.3s ease'
    });
    
    // Set background color based on type
    switch (type) {
      case 'success':
        notification.style.background = '#10b981';
        break;
      case 'error':
        notification.style.background = '#ef4444';
        break;
      default:
        notification.style.background = '#3b82f6';
    }
    
    // Add to DOM
    document.body.appendChild(notification);
    
    // Animate in
    setTimeout(() => {
      notification.style.opacity = '1';
      notification.style.transform = 'translateX(0)';
    }, 100);
    
    // Remove after 3 seconds
    setTimeout(() => {
      notification.style.opacity = '0';
      notification.style.transform = 'translateX(100%)';
      setTimeout(() => {
        if (notification.parentNode) {
          notification.parentNode.removeChild(notification);
        }
      }, 300);
    }, 3000);
  }

})();
