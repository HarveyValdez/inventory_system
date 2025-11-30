

document.addEventListener('DOMContentLoaded', function() {
  // Load configuration from meta/script tag
  const configEl = document.getElementById('vortex-config');
  window.VortexConfig = configEl ? JSON.parse(configEl.textContent) : {
    userId: 0,
    username: 'Guest',
    isAdmin: false,
    csrfToken: null,
    routes: {}
  };

  // Initialize components
  initAccountFeatures();
  initAdminFeatures();
});

// Account deletion 
async function confirmAccountDelete() {
  const { username, userId, routes, csrfToken } = window.VortexConfig;
  
  if (!userId) {
    alert("❌ You must be logged in to delete your account.");
    return;
  }

  if (!confirm(`🚨 DANGER: Delete account '${username}'?\n\nThis will permanently erase:\n• Your profile\n• Activity history\n• Submitted reports\n\nThis action CANNOT be undone!`)) {
    return;
  }
  
  if (prompt("Type DELETE to confirm:") !== "DELETE") {
    return;
  }

  const deleteBtn = document.activeElement;
  const originalText = deleteBtn.innerHTML;
  
  
  deleteBtn.disabled = true;
  deleteBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Deleting...';

  try {
    const response = await fetch(
      `${routes.deleteAccount}${userId}`,
      {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          ...(csrfToken && { "X-CSRFToken": csrfToken })
        },
        body: JSON.stringify({ confirm: true })
      }
    );

    const data = await response.json();

    if (data.success) {
      window.location.href = routes.logout;
    } else {
      throw new Error(data.message || 'Deletion failed');
    }
  } catch (error) {
    deleteBtn.disabled = false;
    deleteBtn.innerHTML = originalText;
    console.error("Account deletion error:", error);
    alert("❌ Account deletion failed: " + error.message);
  }
}

// Flash message utility
function showFlashMessage(message, category = 'info') {
  const flashContainer = document.createElement('div');
  flashContainer.className = `alert alert-${category} alert-dismissible fade show position-fixed top-0 end-0 m-3 shadow-lg`;
  flashContainer.style.zIndex = '9999';
  flashContainer.style.minWidth = '300px';
  flashContainer.innerHTML = `
    ${message}
    <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
  `;
  document.body.appendChild(flashContainer);
  
  
  setTimeout(() => {
    if (flashContainer.parentNode) {
      flashContainer.remove();
    }
  }, 5000);
}

// Admin report 
let reportCheckInterval;
let lastReportCount = 0;

function initAdminFeatures() {
  if (!window.VortexConfig.isAdmin) return;

  
  if ('Notification' in window && Notification.permission === 'default') {
    Notification.requestPermission();
  }

  checkReports(); 
  reportCheckInterval = setInterval(checkReports, 30000); 
}

async function checkReports() {
  const { routes } = window.VortexConfig;
  
  try {
    const response = await fetch(routes.unreadReports);
    if (!response.ok) throw new Error('Network error');
    
    const data = await response.json();
    const notification = document.getElementById('reportNotification');
    const countEl = document.getElementById('unreadCount');
    
    if (!notification || !countEl) return;

    if (data.count > 0) {
      notification.style.display = 'block';
      countEl.textContent = data.count;
      
      
      if (data.count > lastReportCount) {
        
        try {
          const audio = new Audio('/static/sounds/notification.mp3');
          audio.volume = 0.3;
          audio.play().catch(() => {});
        } catch (e) {
          console.log('Notification sound not available');
        }

        
        if ('Notification' in window && Notification.permission === 'granted') {
          new Notification('New User Report', {
            body: `${data.count} new report${data.count > 1 ? 's' : ''} need attention`,
            icon: '/static/images/logo.png',
            tag: 'report-notification'
          });
        }
      }
      lastReportCount = data.count;
    } else {
      notification.style.display = 'none';
      lastReportCount = 0;
    }
  } catch (e) {
    console.error("Error checking reports:", e);
  }
}

function openReports() {
  const { routes, isAdmin } = window.VortexConfig;
  if (!isAdmin) return;
  
  const width = 900;
  const height = 700;
  const left = (screen.width - width) / 2;
  const top = (screen.height - height) / 2;
  
  window.open(
    routes.adminReports,
    "_blank",
    `width=${width},height=${height},left=${left},top=${top},scrollbars=yes,resizable=yes`
  );
}


window.addEventListener('beforeunload', function() {
  if (reportCheckInterval) clearInterval(reportCheckInterval);
});