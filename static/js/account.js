

// Edit account 
function editAccount() {
  showFlashMessage("🚧 Account editing is coming soon! Contact admin for changes.", "info");
}

// load animations
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

  // Update report 
  setTimeout(() => {
    const reportCountEl = document.getElementById('reportCount');
    if (reportCountEl && window.VortexConfig.userId) {
     
      reportCountEl.textContent = reportCountEl.textContent || '0';
    }
  }, 500);
});