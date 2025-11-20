// static/js/homepage.js - PRODUCTION VERSION
console.log('🚀 Homepage JS Loading...');

function createParticles() {
  const container = document.getElementById('particleContainer');
  if (!container) return;
  
  container.innerHTML = ''; // Prevent duplicates
  
  for (let i = 0; i < 15; i++) {
    const particle = document.createElement('div');
    particle.className = 'particle';
    particle.style.width = Math.random() * 60 + 20 + 'px';
    particle.style.height = particle.style.width;
    particle.style.left = Math.random() * 100 + '%';
    particle.style.top = Math.random() * 100 + '%';
    particle.style.animationDelay = Math.random() * 6 + 's';
    particle.style.animationDuration = (Math.random() * 4 + 4) + 's';
    container.appendChild(particle);
  }
}

function animateCounter(element, target) {
  if (!element) return;

  const targetNum = parseInt(target);
  if (isNaN(targetNum) || targetNum <= 0) {
    element.textContent = element.dataset.raw || '0';
    return;
  }

  let current = 0;
  const increment = targetNum / 50;
  const timer = setInterval(() => {
    current += increment;
    if (current >= targetNum) {
      element.textContent = targetNum;
      clearInterval(timer);
    } else {
      element.textContent = Math.floor(current);
    }
  }, 30);
}

// Initialize on DOM ready
document.addEventListener('DOMContentLoaded', function() {
  createParticles();
  
  // Animate counters after brief delay
  setTimeout(() => {
    const productEl = document.getElementById('productCount');
    const lowStockEl = document.getElementById('lowStockCount');
    const activeUsersEl = document.getElementById('activeUsers');
    
    if (productEl) {
      const target = parseInt(productEl.dataset.target) || 0;
      if (target > 0) animateCounter(productEl, target);
    }
    
    if (lowStockEl) {
      const target = parseInt(lowStockEl.dataset.target) || 0;
      if (target > 0) animateCounter(lowStockEl, target);
    }
    
    if (activeUsersEl) {
      const target = parseInt(activeUsersEl.dataset.target) || 0;
      if (target > 0) animateCounter(activeUsersEl, target);
    }
  }, 400); // Shorter delay for snappier feel
  
  // Feature cards animation
  document.querySelectorAll('.feature-card').forEach((card, index) => {
    card.style.opacity = '0';
    card.style.transform = 'translateY(50px)';
    card.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
    card.style.transitionDelay = index * 0.1 + 's';
    
    setTimeout(() => {
      card.style.opacity = '1';
      card.style.transform = 'translateY(0)';
    }, 600 + index * 100);
  });
  
  // Product hover effects
  document.querySelectorAll('.product-slide').forEach(slide => {
    slide.addEventListener('mouseenter', function() {
      this.style.transform = 'scale(1.05) rotateY(5deg)';
      this.style.transition = 'transform 0.3s ease';
    });
    slide.addEventListener('mouseleave', function() {
      this.style.transform = 'scale(1) rotateY(0deg)';
    });
  });
});