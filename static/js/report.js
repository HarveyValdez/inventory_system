/**
 * Report Modal JavaScript - Bulletproof Version
 */

// Global state
let reportModal = null;
let reportForm = null;

// Initialize on DOM ready
document.addEventListener('DOMContentLoaded', function() {
  initializeReportModal();
  console.log('✅ Report system initialized');
});

function initializeReportModal() {
  // Get modal element safely
  const modalEl = document.getElementById('reportModal');
  if (!modalEl) {
    console.error('❌ Report modal element not found!');
    return;
  }

  // Initialize Bootstrap modal
  try {
    reportModal = new bootstrap.Modal(modalEl, {
      backdrop: 'static',
      keyboard: true
    });
  } catch (e) {
    console.error('❌ Bootstrap modal initialization failed:', e);
    return;
  }

  // Get form
  reportForm = document.getElementById('reportForm');
  if (!reportForm) {
    console.error('❌ Report form not found!');
    return;
  }

  // Attach event listeners
  const submitBtn = document.getElementById('submitReportBtn');
  if (submitBtn) {
    submitBtn.addEventListener('click', submitReport);
  } else {
    console.error('❌ Submit button not found!');
  }

  // Reset form on modal close
  modalEl.addEventListener('hidden.bs.modal', function() {
    resetReportForm();
  });

  // Real-time validation
  const messageField = reportForm.querySelector('textarea[name="message"]');
  if (messageField) {
    messageField.addEventListener('input', validateMessageLength);
  }
}

// Safe modal opener
function openReportModal() {
  console.log('🚀 Opening report modal...');
  
  if (!reportModal) {
    console.error('❌ Modal not initialized!');
    alert('Report system not loaded. Please refresh the page.');
    return;
  }

  try {
    reportModal.show();
    console.log('✅ Modal opened successfully');
  } catch (e) {
    console.error('❌ Modal show() failed:', e);
    alert('Cannot open report form: ' + e.message);
  }
}

// Validation
function validateMessageLength() {
  const field = this;
  const minLength = 10;
  
  if (field.value.length < minLength) {
    field.setCustomValidity(`Message must be at least ${minLength} characters. Current: ${field.value.length}`);
  } else {
    field.setCustomValidity('');
  }
}

// Submit report
async function submitReport() {
  console.log('📤 Submitting report...');
  
  if (!reportForm || !reportModal) {
    alert('❌ Report system not ready. Please refresh.');
    return;
  }

  // Validate form
  if (!reportForm.checkValidity()) {
    reportForm.classList.add('was-validated');
    return;
  }

  const formData = new FormData(reportForm);
  const data = Object.fromEntries(formData);
  
  // Add user context
  data.user_id = window.VortexConfig?.userId || 0;
  
  // Validate data
  if (!data.report_type || !data.message || data.message.trim().length < 10) {
    showError('Please fill all fields. Message must be at least 10 characters.');
    return;
  }

  // Show loading state
  const submitBtn = document.getElementById('submitReportBtn');
  const originalHTML = submitBtn.innerHTML;
  submitBtn.disabled = true;
  submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Sending...';

  try {
    const headers = {
      "Content-Type": "application/json"
    };

    // Add CSRF token if available
    if (window.VortexConfig?.csrfToken) {
      headers["X-CSRFToken"] = window.VortexConfig.csrfToken;
    }

    console.log('📡 Fetching:', '/submit_report', data);
    
    const response = await fetch('/submit_report', {
      method: "POST",
      headers: headers,
      body: JSON.stringify(data)
    });

    const result = await response.json();
    console.log('✅ Response:', result);

    if (result.success) {
      // Success
      reportModal.hide();
      showFlashMessage("✅ Report sent successfully! Admin will review shortly.", "success");
      resetReportForm();
      
      // Update report count on account page if present
      const reportCountEl = document.getElementById('reportCount');
      if (reportCountEl) {
        reportCountEl.textContent = parseInt(reportCountEl.textContent || '0') + 1;
      }
    } else {
      throw new Error(result.message || 'Submission failed');
    }
  } catch (error) {
    console.error('❌ Report submission error:', error);
    showError('Failed to send report: ' + error.message);
  } finally {
    // Restore button state
    submitBtn.disabled = false;
    submitBtn.innerHTML = originalHTML;
  }
}

// Error display
function showError(message) {
  const errorDiv = document.getElementById('reportError');
  if (errorDiv) {
    errorDiv.textContent = message;
    errorDiv.style.display = 'block';
    setTimeout(() => errorDiv.style.display = 'none', 5000);
  } else {
    alert('❌ ' + message);
  }
}

// Reset form
function resetReportForm() {
  if (reportForm) {
    reportForm.reset();
    reportForm.classList.remove('was-validated');
  }
  const errorDiv = document.getElementById('reportError');
  if (errorDiv) errorDiv.style.display = 'none';
}