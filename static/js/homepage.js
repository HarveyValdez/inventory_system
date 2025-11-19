// Particle animation
function createParticles() {
  const container = document.getElementById('particleContainer');
  if (!container) return;
  
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

// Animated counters
function animateCounter(element, target) {
  if (!element) return;
  let current = 0;
  const increment = target / 50;
  const timer = setInterval(() => {
    current += increment;
    if (current >= target) {
      element.textContent = target;
      clearInterval(timer);
    } else {
      element.textContent = Math.floor(current);
    }
  }, 30);
}

// Intersection Observer for scroll animations
const observer = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      entry.target.style.opacity = '1';
      entry.target.style.transform = 'translateY(0)';
    }
  });
});

// Initialize on load
document.addEventListener('DOMContentLoaded', function() {
  createParticles();
  
  // Animate counters when stats section is visible
  const statsSection = document.querySelector('.glass-card');
  if (statsSection) {
    observer.observe(statsSection);
    setTimeout(() => {
      // Read target values from data attributes
      const productCountEl = document.getElementById('productCount');
      const lowStockCountEl = document.getElementById('lowStockCount');
      const activeUsersEl = document.getElementById('activeUsers');
      
      if (productCountEl) animateCounter(productCountEl, parseInt(productCountEl.dataset.target));
      if (lowStockCountEl) animateCounter(lowStockCountEl, parseInt(lowStockCountEl.dataset.target));
      if (activeUsersEl) animateCounter(activeUsersEl, parseInt(activeUsersEl.dataset.target));
    }, 500);
  }
  
  // Feature cards scroll animation
  document.querySelectorAll('.feature-card').forEach((card, index) => {
    card.style.opacity = '0';
    card.style.transform = 'translateY(50px)';
    card.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
    card.style.transitionDelay = index * 0.1 + 's';
    observer.observe(card);
  });
  
  // Product slide hover effect
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