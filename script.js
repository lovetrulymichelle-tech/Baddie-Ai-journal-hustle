// Smooth scrolling for navigation links
document.addEventListener('DOMContentLoaded', function() {
    // Get all navigation links
    const navLinks = document.querySelectorAll('a[href^="#"]');
    
    navLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            
            const targetId = this.getAttribute('href');
            const targetElement = document.querySelector(targetId);
            
            if (targetElement) {
                const headerHeight = document.querySelector('.header').offsetHeight;
                const targetPosition = targetElement.offsetTop - headerHeight - 20;
                
                window.scrollTo({
                    top: targetPosition,
                    behavior: 'smooth'
                });
            }
        });
    });
    
    // Add scroll effect to header
    const header = document.querySelector('.header');
    let lastScrollTop = 0;
    
    window.addEventListener('scroll', function() {
        const scrollTop = window.pageYOffset || document.documentElement.scrollTop;
        
        if (scrollTop > 100) {
            header.style.background = 'rgba(255, 255, 255, 0.98)';
            header.style.boxShadow = '0 2px 20px rgba(0, 0, 0, 0.1)';
        } else {
            header.style.background = 'rgba(255, 255, 255, 0.95)';
            header.style.boxShadow = 'none';
        }
        
        lastScrollTop = scrollTop;
    });
    
    // Animate stats on scroll
    const statsObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const statNumbers = entry.target.querySelectorAll('.stat-number');
                statNumbers.forEach(stat => {
                    animateNumber(stat);
                });
                statsObserver.unobserve(entry.target);
            }
        });
    });
    
    const statsCard = document.querySelector('.stats-card');
    if (statsCard) {
        statsObserver.observe(statsCard);
    }
    
    // Number animation function
    function animateNumber(element) {
        const finalNumber = element.textContent;
        const numericValue = parseInt(finalNumber.replace(/\D/g, ''));
        const suffix = finalNumber.replace(/\d/g, '');
        let currentNumber = 0;
        const increment = numericValue / 50;
        
        const timer = setInterval(() => {
            currentNumber += increment;
            if (currentNumber >= numericValue) {
                currentNumber = numericValue;
                clearInterval(timer);
            }
            element.textContent = Math.floor(currentNumber) + suffix;
        }, 30);
    }
    
    // Add hover effects to feature cards
    const featureCards = document.querySelectorAll('.feature-card');
    featureCards.forEach(card => {
        card.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-8px) scale(1.02)';
        });
        
        card.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0) scale(1)';
        });
    });
    
    // Journal mockup interaction
    const journalMockup = document.querySelector('.journal-mockup');
    if (journalMockup) {
        journalMockup.addEventListener('mouseenter', function() {
            this.style.transform = 'perspective(1000px) rotateY(-5deg) rotateX(2deg) scale(1.05)';
        });
        
        journalMockup.addEventListener('mouseleave', function() {
            this.style.transform = 'perspective(1000px) rotateY(-15deg) rotateX(5deg) scale(1)';
        });
    }
    
    // Add click handlers for CTA buttons
    const ctaButtons = document.querySelectorAll('.btn');
    ctaButtons.forEach(button => {
        if (button.textContent.includes('Download') || button.textContent.includes('Get Started') || button.textContent.includes('Try Web')) {
            button.addEventListener('click', function(e) {
                e.preventDefault();
                // Show a demo message since this is just a landing page
                showNotification('🚀 Thanks for your interest! This is a demo landing page. The app is coming soon!');
            });
        }
        
        if (button.textContent.includes('Referral Link')) {
            button.addEventListener('click', function(e) {
                e.preventDefault();
                showNotification('🎁 Referral program is coming soon! Stay tuned for updates.');
            });
        }
    });
    
    // Notification system
    function showNotification(message) {
        // Remove existing notification if any
        const existingNotification = document.querySelector('.notification');
        if (existingNotification) {
            existingNotification.remove();
        }
        
        // Create notification element
        const notification = document.createElement('div');
        notification.className = 'notification';
        notification.textContent = message;
        notification.style.cssText = `
            position: fixed;
            top: 100px;
            right: 20px;
            background: linear-gradient(135deg, #6366f1, #8b5cf6);
            color: white;
            padding: 15px 25px;
            border-radius: 12px;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
            z-index: 10000;
            max-width: 350px;
            font-weight: 500;
            animation: slideInRight 0.3s ease-out;
        `;
        
        // Add animation keyframes
        if (!document.querySelector('#notification-styles')) {
            const style = document.createElement('style');
            style.id = 'notification-styles';
            style.textContent = `
                @keyframes slideInRight {
                    from {
                        transform: translateX(100%);
                        opacity: 0;
                    }
                    to {
                        transform: translateX(0);
                        opacity: 1;
                    }
                }
                
                @keyframes slideOutRight {
                    from {
                        transform: translateX(0);
                        opacity: 1;
                    }
                    to {
                        transform: translateX(100%);
                        opacity: 0;
                    }
                }
            `;
            document.head.appendChild(style);
        }
        
        document.body.appendChild(notification);
        
        // Auto remove after 4 seconds
        setTimeout(() => {
            notification.style.animation = 'slideOutRight 0.3s ease-out';
            setTimeout(() => {
                if (notification.parentNode) {
                    notification.remove();
                }
            }, 300);
        }, 4000);
        
        // Remove on click
        notification.addEventListener('click', () => {
            notification.style.animation = 'slideOutRight 0.3s ease-out';
            setTimeout(() => {
                if (notification.parentNode) {
                    notification.remove();
                }
            }, 300);
        });
    }
    
    // Add mobile menu toggle functionality (basic)
    const createMobileMenu = () => {
        if (window.innerWidth <= 768) {
            const nav = document.querySelector('.nav-menu');
            const logo = document.querySelector('.nav-logo');
            
            if (!document.querySelector('.mobile-menu-toggle')) {
                const toggleButton = document.createElement('button');
                toggleButton.className = 'mobile-menu-toggle';
                toggleButton.innerHTML = '<i class="fas fa-bars"></i>';
                toggleButton.style.cssText = `
                    background: none;
                    border: none;
                    font-size: 1.5rem;
                    color: #6366f1;
                    cursor: pointer;
                    display: none;
                `;
                
                logo.parentNode.appendChild(toggleButton);
                
                if (window.innerWidth <= 768) {
                    toggleButton.style.display = 'block';
                    nav.style.display = 'none';
                }
            }
        }
    };
    
    createMobileMenu();
    window.addEventListener('resize', createMobileMenu);
    
    // Add loading animation for page elements
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };
    
    const fadeInObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
                fadeInObserver.unobserve(entry.target);
            }
        });
    }, observerOptions);
    
    // Observe elements for fade-in animation
    const elementsToAnimate = document.querySelectorAll('.feature-card, .insights-text, .stats-card, .referral-card');
    elementsToAnimate.forEach(el => {
        el.style.opacity = '0';
        el.style.transform = 'translateY(30px)';
        el.style.transition = 'opacity 0.6s ease-out, transform 0.6s ease-out';
        fadeInObserver.observe(el);
    });
});

// Add some console fun for developers
console.log(`
🧠 Baddie AI Journal Hustle Landing Page
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✨ Features:
• Responsive design
• Smooth scrolling
• Interactive animations
• Modern gradient aesthetics
• Mobile-friendly

🚀 Built with vanilla HTML, CSS, and JavaScript
💜 Designed for the AI journaling community

Have feedback? We'd love to hear from you!
`);