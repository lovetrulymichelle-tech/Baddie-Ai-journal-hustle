// Baddie AI Journal Hustle - Interactive JavaScript
// Luxury functionality for the pink-themed journal application

document.addEventListener('DOMContentLoaded', function() {
    
    // ===== NAVIGATION MOBILE TOGGLE =====
    const navToggle = document.querySelector('.nav-toggle');
    const navLinks = document.querySelector('.nav-links');
    
    if (navToggle && navLinks) {
        navToggle.addEventListener('click', function() {
            navLinks.classList.toggle('nav-open');
            navToggle.classList.toggle('nav-toggle-active');
        });
    }
    
    // ===== SMOOTH SCROLLING FOR ANCHOR LINKS =====
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
    
    // ===== SPARKLE ANIMATION ON SCROLL =====
    const sparkles = document.querySelectorAll('.sparkle');
    if (sparkles.length > 0) {
        window.addEventListener('scroll', function() {
            const scrolled = window.pageYOffset;
            sparkles.forEach((sparkle, index) => {
                const speed = 0.5 + (index * 0.2);
                sparkle.style.transform = `translateY(${scrolled * speed}px)`;
            });
        });
    }
    
    // ===== ENTRY CARD HOVER EFFECTS =====
    const entryCards = document.querySelectorAll('.entry-card');
    entryCards.forEach(card => {
        card.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-8px) scale(1.02)';
        });
        
        card.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0) scale(1)';
        });
    });
    
    // ===== MOOD CHART ANIMATIONS =====
    const moodBars = document.querySelectorAll('.mood-fill');
    const observerOptions = {
        threshold: 0.5,
        rootMargin: '0px 0px -100px 0px'
    };
    
    const observer = new IntersectionObserver(function(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const moodBar = entry.target;
                const finalWidth = moodBar.style.width;
                moodBar.style.width = '0%';
                
                setTimeout(() => {
                    moodBar.style.transition = 'width 1.5s ease-out';
                    moodBar.style.width = finalWidth;
                }, 300);
            }
        });
    }, observerOptions);
    
    moodBars.forEach(bar => observer.observe(bar));
    
    // ===== FLOATING LABELS FOR FORM INPUTS =====
    const formInputs = document.querySelectorAll('.form-input, .form-textarea, .form-select');
    formInputs.forEach(input => {
        // Add focus and blur effects
        input.addEventListener('focus', function() {
            this.parentElement.classList.add('input-focused');
        });
        
        input.addEventListener('blur', function() {
            this.parentElement.classList.remove('input-focused');
            if (this.value.trim() !== '') {
                this.parentElement.classList.add('input-filled');
            } else {
                this.parentElement.classList.remove('input-filled');
            }
        });
        
        // Check initial state
        if (input.value.trim() !== '') {
            input.parentElement.classList.add('input-filled');
        }
    });
    
    // ===== DYNAMIC GREETING BASED ON TIME =====
    const greetingElements = document.querySelectorAll('.dynamic-greeting');
    if (greetingElements.length > 0) {
        const now = new Date();
        const hour = now.getHours();
        let greeting = 'Hello';
        let emoji = '👋';
        
        if (hour >= 5 && hour < 12) {
            greeting = 'Good Morning';
            emoji = '🌅';
        } else if (hour >= 12 && hour < 17) {
            greeting = 'Good Afternoon';
            emoji = '☀️';
        } else if (hour >= 17 && hour < 22) {
            greeting = 'Good Evening';
            emoji = '🌆';
        } else {
            greeting = 'Good Night';
            emoji = '🌙';
        }
        
        greetingElements.forEach(element => {
            element.textContent = `${greeting}, Queen! ${emoji}`;
        });
    }
    
    // ===== MOTIVATIONAL QUOTES ROTATION =====
    const quotes = [
        "You are the CEO of your own life. Start acting like it and build your empire! ✨",
        "Queens don't compete with others, they compete with themselves to become better. 👑",
        "Your journal is your safe space. Write your truth and watch yourself grow. 💕",
        "Every entry is a step closer to understanding your incredible mind. 🧠",
        "Document your journey, celebrate your wins, and learn from your challenges. 🚀",
        "You're not just writing words, you're creating your legacy. 📝",
        "Your thoughts have power. Use them to manifest your dreams. ✨",
        "Progress, not perfection. Every day you journal is a victory. 🏆"
    ];
    
    const quoteElement = document.querySelector('.motivational-quote blockquote');
    if (quoteElement) {
        // Rotate quotes every 10 seconds
        let currentQuoteIndex = 0;
        setInterval(() => {
            currentQuoteIndex = (currentQuoteIndex + 1) % quotes.length;
            quoteElement.style.opacity = '0';
            
            setTimeout(() => {
                quoteElement.textContent = quotes[currentQuoteIndex];
                quoteElement.style.opacity = '1';
            }, 500);
        }, 10000);
    }
    
    // ===== FORM VALIDATION ENHANCEMENTS =====
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            const requiredFields = form.querySelectorAll('[required]');
            let isValid = true;
            
            requiredFields.forEach(field => {
                if (field.value.trim() === '') {
                    isValid = false;
                    field.classList.add('error');
                    field.addEventListener('input', function() {
                        this.classList.remove('error');
                    }, { once: true });
                }
            });
            
            if (!isValid) {
                e.preventDefault();
                showNotification('Please fill in all required fields ✨', 'error');
            }
        });
    });
    
    // ===== NOTIFICATION SYSTEM =====
    function showNotification(message, type = 'info') {
        const notification = document.createElement('div');
        notification.className = `notification notification-${type}`;
        notification.innerHTML = `
            <div class="notification-content">
                <i class="fas fa-crown"></i>
                <span>${message}</span>
                <button class="notification-close">
                    <i class="fas fa-times"></i>
                </button>
            </div>
        `;
        
        document.body.appendChild(notification);
        
        // Animate in
        setTimeout(() => notification.classList.add('notification-show'), 100);
        
        // Auto remove
        setTimeout(() => {
            notification.classList.remove('notification-show');
            setTimeout(() => notification.remove(), 300);
        }, 5000);
        
        // Manual close
        notification.querySelector('.notification-close').addEventListener('click', () => {
            notification.classList.remove('notification-show');
            setTimeout(() => notification.remove(), 300);
        });
    }
    
    // ===== STREAK CELEBRATION =====
    const streakElements = document.querySelectorAll('[data-streak]');
    streakElements.forEach(element => {
        const streak = parseInt(element.dataset.streak);
        if (streak > 0 && streak % 7 === 0) {
            // Celebrate weekly milestones
            element.classList.add('streak-celebration');
            
            // Add confetti effect (simplified)
            for (let i = 0; i < 10; i++) {
                const confetti = document.createElement('div');
                confetti.className = 'confetti';
                confetti.style.left = Math.random() * 100 + '%';
                confetti.style.animationDelay = Math.random() * 2 + 's';
                element.appendChild(confetti);
                
                setTimeout(() => confetti.remove(), 3000);
            }
        }
    });
    
    // ===== TYPING ANIMATION FOR HERO TEXT =====
    const heroTitle = document.querySelector('.hero-title');
    if (heroTitle && !heroTitle.classList.contains('typing-complete')) {
        const text = heroTitle.textContent;
        heroTitle.textContent = '';
        heroTitle.classList.add('typing-animation');
        
        let i = 0;
        const typingSpeed = 100;
        
        function typeWriter() {
            if (i < text.length) {
                heroTitle.textContent += text.charAt(i);
                i++;
                setTimeout(typeWriter, typingSpeed);
            } else {
                heroTitle.classList.remove('typing-animation');
                heroTitle.classList.add('typing-complete');
            }
        }
        
        setTimeout(typeWriter, 1000);
    }
    
    // ===== MOOD SELECTOR ENHANCEMENT =====
    const moodSelects = document.querySelectorAll('select[name="mood"]');
    moodSelects.forEach(select => {
        select.addEventListener('change', function() {
            const selectedOption = this.options[this.selectedIndex];
            const emoji = selectedOption.text.split(' ')[0];
            
            // Add visual feedback
            this.style.background = getGradientForMood(this.value);
            this.style.color = 'white';
            
            // Show mood feedback
            let feedback = getMoodFeedback(this.value);
            showMoodFeedback(feedback, emoji);
        });
    });
    
    function getGradientForMood(mood) {
        const moodGradients = {
            'ecstatic': 'linear-gradient(135deg, #FFD700, #FFA500)',
            'happy': 'linear-gradient(135deg, #FFB6C1, #FF69B4)',
            'grateful': 'linear-gradient(135deg, #98FB98, #32CD32)',
            'excited': 'linear-gradient(135deg, #FF6347, #FF4500)',
            'motivated': 'linear-gradient(135deg, #87CEEB, #4682B4)',
            'focused': 'linear-gradient(135deg, #DDA0DD, #9370DB)',
            'peaceful': 'linear-gradient(135deg, #B0E0E6, #87CEEB)',
            'contemplative': 'linear-gradient(135deg, #F0E68C, #DAA520)',
            'confident': 'linear-gradient(135deg, #FF1493, #C71585)',
            'ambitious': 'linear-gradient(135deg, #DC143C, #B22222)',
            'empowered': 'linear-gradient(135deg, #8A2BE2, #4B0082)'
        };
        
        return moodGradients[mood] || 'linear-gradient(135deg, #FF69B4, #FF1493)';
    }
    
    function getMoodFeedback(mood) {
        const feedback = {
            'ecstatic': 'You\'re absolutely glowing today! ✨',
            'happy': 'Your positive energy is contagious! 😊',
            'grateful': 'Gratitude is the foundation of abundance! 🙏',
            'excited': 'Channel that excitement into action! 🔥',
            'motivated': 'You\'re unstoppable when motivated! 💪',
            'focused': 'Laser focus leads to success! 🎯',
            'peaceful': 'Inner peace is true luxury! 😌',
            'contemplative': 'Deep thoughts lead to wisdom! 🤔',
            'confident': 'Confidence is your crown! 👑',
            'ambitious': 'Dream big and make it happen! 🚀',
            'empowered': 'You hold all the power! 💎'
        };
        
        return feedback[mood] || 'Every feeling is valid! 💕';
    }
    
    function showMoodFeedback(message, emoji) {
        // Remove existing feedback
        const existingFeedback = document.querySelector('.mood-feedback');
        if (existingFeedback) {
            existingFeedback.remove();
        }
        
        // Create new feedback
        const feedback = document.createElement('div');
        feedback.className = 'mood-feedback';
        feedback.innerHTML = `
            <div class="mood-feedback-content">
                <span class="mood-emoji">${emoji}</span>
                <span class="mood-message">${message}</span>
            </div>
        `;
        
        const moodSelect = document.querySelector('select[name="mood"]');
        if (moodSelect) {
            moodSelect.parentElement.appendChild(feedback);
            
            setTimeout(() => {
                feedback.classList.add('mood-feedback-show');
            }, 100);
            
            setTimeout(() => {
                feedback.classList.remove('mood-feedback-show');
                setTimeout(() => feedback.remove(), 300);
            }, 3000);
        }
    }
    
    // ===== LAZY LOADING FOR IMAGES =====
    const images = document.querySelectorAll('img[data-src]');
    const imageObserver = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const img = entry.target;
                img.src = img.dataset.src;
                img.classList.remove('lazy');
                observer.unobserve(img);
            }
        });
    });
    
    images.forEach(img => imageObserver.observe(img));
    
    // ===== KEYBOARD SHORTCUTS =====
    document.addEventListener('keydown', function(e) {
        // Ctrl/Cmd + Enter to submit forms
        if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
            const activeForm = document.querySelector('form:focus-within');
            if (activeForm) {
                const submitButton = activeForm.querySelector('button[type="submit"]');
                if (submitButton) {
                    submitButton.click();
                }
            }
        }
        
        // Escape to close modals/notifications
        if (e.key === 'Escape') {
            const notifications = document.querySelectorAll('.notification');
            notifications.forEach(notification => {
                notification.querySelector('.notification-close').click();
            });
        }
    });
    
    // ===== WELCOME MESSAGE FOR NEW USERS =====
    if (localStorage.getItem('first-visit') === null) {
        setTimeout(() => {
            showNotification('Welcome to your royal journal experience! ✨👑', 'success');
            localStorage.setItem('first-visit', 'false');
        }, 2000);
    }
    
    // ===== THEME PERSISTENCE =====
    const themeSelect = document.querySelector('select[value*="pink-luxe"]');
    if (themeSelect) {
        themeSelect.addEventListener('change', function() {
            document.body.className = `theme-${this.value}`;
            localStorage.setItem('preferred-theme', this.value);
        });
    }
    
    // Load saved theme
    const savedTheme = localStorage.getItem('preferred-theme');
    if (savedTheme) {
        document.body.className = `theme-${savedTheme}`;
    }
    
    console.log('🌸 Baddie AI Journal Hustle loaded successfully! 👑✨');
});

// ===== ADDITIONAL CSS FOR DYNAMIC FEATURES =====
const dynamicStyles = `
    .nav-open {
        display: flex !important;
        flex-direction: column;
        position: absolute;
        top: 100%;
        left: 0;
        right: 0;
        background: white;
        box-shadow: var(--shadow-soft);
        border-radius: 0 0 var(--radius-md) var(--radius-md);
        padding: var(--spacing-md);
    }
    
    .nav-toggle-active span:nth-child(1) {
        transform: rotate(-45deg) translate(-5px, 6px);
    }
    
    .nav-toggle-active span:nth-child(2) {
        opacity: 0;
    }
    
    .nav-toggle-active span:nth-child(3) {
        transform: rotate(45deg) translate(-5px, -6px);
    }
    
    .input-focused .form-label {
        color: var(--primary-pink);
        transform: translateY(-2px);
    }
    
    .form-input.error,
    .form-textarea.error {
        border-color: #ff4757;
        box-shadow: 0 0 0 3px rgba(255, 71, 87, 0.1);
    }
    
    .notification {
        position: fixed;
        top: 100px;
        right: -400px;
        z-index: 1002;
        background: white;
        border-radius: var(--radius-md);
        box-shadow: var(--shadow-strong);
        border: 2px solid var(--primary-pink);
        transition: all 0.3s ease;
        max-width: 350px;
    }
    
    .notification-show {
        right: var(--spacing-md);
    }
    
    .notification-content {
        padding: var(--spacing-md);
        display: flex;
        align-items: center;
        gap: var(--spacing-sm);
    }
    
    .notification-close {
        background: none;
        border: none;
        color: var(--text-light);
        cursor: pointer;
        margin-left: auto;
        padding: var(--spacing-xs);
        border-radius: var(--radius-sm);
    }
    
    .streak-celebration {
        position: relative;
        animation: celebrate 2s ease-in-out;
    }
    
    @keyframes celebrate {
        0%, 100% { transform: scale(1); }
        50% { transform: scale(1.1); }
    }
    
    .confetti {
        position: absolute;
        width: 10px;
        height: 10px;
        background: var(--primary-pink);
        animation: confetti-fall 3s linear infinite;
        border-radius: 50%;
    }
    
    @keyframes confetti-fall {
        0% {
            transform: translateY(-100px) rotate(0deg);
            opacity: 1;
        }
        100% {
            transform: translateY(200px) rotate(360deg);
            opacity: 0;
        }
    }
    
    .typing-animation::after {
        content: '|';
        animation: blink 1s infinite;
    }
    
    @keyframes blink {
        0%, 50% { opacity: 1; }
        51%, 100% { opacity: 0; }
    }
    
    .mood-feedback {
        margin-top: var(--spacing-sm);
        opacity: 0;
        transform: translateY(-10px);
        transition: all 0.3s ease;
    }
    
    .mood-feedback-show {
        opacity: 1;
        transform: translateY(0);
    }
    
    .mood-feedback-content {
        display: flex;
        align-items: center;
        gap: var(--spacing-xs);
        padding: var(--spacing-xs) var(--spacing-sm);
        background: var(--bg-overlay);
        border-radius: var(--radius-sm);
        color: var(--primary-pink);
        font-weight: 600;
        font-size: 0.9rem;
    }
    
    .mood-emoji {
        font-size: 1.2rem;
    }
    
    @media (max-width: 768px) {
        .nav-toggle {
            display: flex;
        }
        
        .nav-links {
            display: none;
        }
        
        .notification {
            right: -100%;
            left: var(--spacing-sm);
            max-width: none;
        }
        
        .notification-show {
            right: 0;
        }
    }
`;

// Inject dynamic styles
const styleSheet = document.createElement('style');
styleSheet.textContent = dynamicStyles;
document.head.appendChild(styleSheet);