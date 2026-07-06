document.addEventListener('DOMContentLoaded', () => {
    
    // --- 1. FIXED HEADER INTERACTIVE COLOR SHIFTING ---
    const siteHeader = document.querySelector('.site-header');
    
    const evaluateHeaderScroll = () => {
        if (window.scrollY > 50) {
            siteHeader.classList.add('scrolled');
        } else {
            siteHeader.classList.remove('scrolled');
        }
    };

    window.addEventListener('scroll', evaluateHeaderScroll);
    evaluateHeaderScroll(); // Execute instantly on boot for persistent states

    // --- 2. MOBILE NAVIGATION HAMBURGER MECHANICS ---
    const hamburgerToggle = document.getElementById('hamburgerToggle');
    const navMenu = document.getElementById('navMenu');
    const navLinks = document.querySelectorAll('.nav-link');

    const toggleMobileMenu = () => {
        hamburgerToggle.classList.toggle('active');
        navMenu.classList.toggle('active');
        const isExpanded = hamburgerToggle.classList.contains('active');
        hamburgerToggle.setAttribute('aria-expanded', isExpanded);

        // Prevent body layer background scroll leaking when mobile menu is expanded
        if (isExpanded) {
            document.body.style.overflow = 'hidden';
        } else {
            document.body.style.overflow = '';
        }
    };

    hamburgerToggle.addEventListener('click', toggleMobileMenu);

    // Dismiss overlay states when individual anchor targets are touched
    navLinks.forEach(link => {
        link.addEventListener('click', () => {
            if (navMenu.classList.contains('active')) {
                toggleMobileMenu();
            }
        });
    });

    // --- 3. INTERACTIVE ACCORDION MECHANICS (FAQ) ---
    const faqItems = document.querySelectorAll('.faq-item');

    faqItems.forEach(item => {
        const trigger = item.querySelector('.faq-trigger');
        const content = item.querySelector('.faq-content');

        trigger.addEventListener('click', () => {
            const isCurrentlyActive = item.classList.contains('active');

            // Collapse all alternate items for cleaner systemic layout control
            faqItems.forEach(alternateItem => {
                alternateItem.classList.remove('active');
                alternateItem.querySelector('.faq-content').style.maxHeight = null;
                alternateItem.querySelector('.faq-trigger').setAttribute('aria-expanded', 'false');
            });

            // Toggle computational height metrics on targeted target row
            if (!isCurrentlyActive) {
                item.classList.add('active');
                trigger.setAttribute('aria-expanded', 'true');
                content.style.maxHeight = content.scrollHeight + 'px';
            }
        });
    });

    // --- 4. SCROLL INTERSECTION REVEAL TRANSITIONS ---
    const revealElements = document.querySelectorAll('.reveal');

    const scrollRevealObserver = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('revealed');
                // Cease tracking once state has been securely instantiated
                observer.unobserve(entry.target);
            }
        });
    }, {
        root: null, // Viewport standard relative metrics
        threshold: 0.1, // Trigger transition when 10% element area surfaces
        rootMargin: '0px 0px -40px 0px' // Offset margin framework targeting human eyes
    });

    revealElements.forEach(element => {
        scrollRevealObserver.observe(element);
    });

    // --- 5. DARK MODE TOGGLE LOGIC ---
    const themeToggle = document.getElementById('themeToggle');
    const currentTheme = localStorage.getItem('theme');

    if (currentTheme === 'dark') {
        document.documentElement.setAttribute('data-theme', 'dark');
        themeToggle.querySelector('i').classList.replace('fa-moon', 'fa-sun');
    }

    themeToggle.addEventListener('click', () => {
        let theme = 'light';
        if (document.documentElement.getAttribute('data-theme') !== 'dark') {
            theme = 'dark';
            document.documentElement.setAttribute('data-theme', 'dark');
            themeToggle.querySelector('i').classList.replace('fa-moon', 'fa-sun');
        } else {
            document.documentElement.removeAttribute('data-theme');
            themeToggle.querySelector('i').classList.replace('fa-sun', 'fa-moon');
        }
        localStorage.setItem('theme', theme);
    });

    // --- 6. BOOKING ENGINE MODAL MECHANICS ---
    const openBooking = document.getElementById('openBooking');
    const closeBooking = document.getElementById('closeBooking');
    const bookingModal = document.getElementById('bookingModal');
    const reservationForm = document.getElementById('reservationForm');
    const formFeedback = document.getElementById('formFeedback');

    const toggleModal = () => {
        bookingModal.classList.toggle('active');
        document.body.style.overflow = bookingModal.classList.contains('active') ? 'hidden' : '';
    };

    openBooking?.addEventListener('click', toggleModal);
    closeBooking?.addEventListener('click', toggleModal);

    reservationForm?.addEventListener('submit', async (e) => {
        e.preventDefault();
        const formData = new FormData(reservationForm);
        const data = Object.fromEntries(formData.entries());

        formFeedback.textContent = "Processing your चर्चा reservation...";
        formFeedback.className = "form-feedback";

        try {
            const response = await fetch('/api/reserve', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(data)
            });

            const result = await response.json();
            if (result.success) {
                formFeedback.textContent = result.message;
                formFeedback.classList.add('success');
                setTimeout(() => {
                    toggleModal();
                    reservationForm.reset();
                    formFeedback.textContent = "";
                }, 3000);
            } else {
                formFeedback.textContent = result.message;
                formFeedback.classList.add('error');
            }
        } catch (err) {
            formFeedback.textContent = "Network error. Please call us directly.";
            formFeedback.classList.add('error');
        }
    });

    // Set minimum date to today
    const dateInput = document.getElementById('bookingDate');
    if(dateInput) dateInput.min = new Date().toISOString().split('T')[0];

    // --- 7. BREW CUSTOMIZER SIMULATOR ---
    const simBase = document.getElementById('simBase');
    const simMilk = document.getElementById('simMilk');
    const simFlavor = document.getElementById('simFlavor');
    const simSweet = document.getElementById('simSweet');
    const simFoam = document.getElementById('simFoam');
    const simResult = document.getElementById('simResult');

    const updateSim = () => {
        if(!simResult) return;
        const base = simBase.value;
        const milk = simMilk.value === 'None' ? 'Pure' : simMilk.value;
        
        const parts = [base, milk];
        if (simFlavor.value !== 'None') parts.push(simFlavor.value);
        if (simSweet.value !== 'None') parts.push(simSweet.value);
        parts.push(simFoam.value === 'None' ? 'No Cloud' : simFoam.value + ' Cloud');
        
        simResult.textContent = parts.join(' + ');
        
        simResult.animate([
            { opacity: 0.7, transform: 'translateY(5px)' },
            { opacity: 1, transform: 'translateY(0)' }
        ], { duration: 300, easing: 'ease-out' });
    };

    [simBase, simMilk, simFlavor, simSweet, simFoam].forEach(el => el?.addEventListener('change', updateSim));
    updateSim();
});
