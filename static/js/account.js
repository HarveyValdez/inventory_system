/**
 * Account Page JavaScript
 * Handles user account interactions
 */

// Edit account placeholder
function editAccount() {
  showFlashMessage("🚧 Account editing is coming soon! Contact admin for changes.", "info");
}

// Page load animations
document.addEventListener('DOMContentLoaded', function() {
  const cards = document.querySelectorAll('.card');
  cards.forEach((card, index) => {
    card.style.opacity = '0';
    card.style.transform = 'translateY(20px)';
    card.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
    setTimeout(() => {
      card.style.opacity = '1';
      card.style.transform = 'translateY(0)';
    }, 100 * index);
  });

  // Update report count after slight delay
  setTimeout(() => {
    const reportCountEl = document.getElementById('reportCount');
    if (reportCountEl && window.VortexConfig.userId) {
      // Could fetch actual count from API here
      reportCountEl.textContent = reportCountEl.textContent || '0';
    }
  }, 500);
});