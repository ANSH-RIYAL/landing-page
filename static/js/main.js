document.addEventListener('DOMContentLoaded', function() {
    // Initial interest count update
    updateInterestCount();

    // Navbar scroll effect
    const navbar = document.querySelector('.navbar');
    window.addEventListener('scroll', () => {
        if (window.scrollY > 50) {
            navbar.classList.add('scrolled');
        } else {
            navbar.classList.remove('scrolled');
        }
    });

    // Feature Slider
    const slider = document.querySelector('.feature-slider');
    const slides = document.querySelectorAll('.feature-slide');
    const dots = document.querySelectorAll('.slider-dots .dot');
    const prevBtn = document.querySelector('.prev-btn');
    const nextBtn = document.querySelector('.next-btn');
    let currentSlide = 0;

    function updateSlider() {
        slides.forEach(slide => slide.classList.remove('active'));
        dots.forEach(dot => dot.classList.remove('active'));
        
        slides[currentSlide].classList.add('active');
        dots[currentSlide].classList.add('active');
    }

    function nextSlide() {
        currentSlide = (currentSlide + 1) % slides.length;
        updateSlider();
    }

    function prevSlide() {
        currentSlide = (currentSlide - 1 + slides.length) % slides.length;
        updateSlider();
    }

    // Event Listeners
    if (prevBtn) prevBtn.addEventListener('click', prevSlide);
    if (nextBtn) nextBtn.addEventListener('click', nextSlide);
    
    dots.forEach((dot, index) => {
        dot.addEventListener('click', () => {
            currentSlide = index;
            updateSlider();
        });
    });

    // Auto slide every 5 seconds
    setInterval(nextSlide, 5000);

    // Initialize slider
    updateSlider();

    // Interest Button
    const interestBtn = document.getElementById('interestedBtn');
    const interestCount = document.getElementById('interestCount');
    const emailSubmissionSection = document.getElementById('emailSubmissionSection');

    function updateInterestCount() {
        fetch('/api/interest/count')
            .then(response => response.json())
            .then(data => {
                if (interestCount) {
                    interestCount.textContent = data.count;
                }
            })
            .catch(error => console.error('Error:', error));
    }

    if (interestBtn) {
        interestBtn.addEventListener('click', function() {
            fetch('/api/interest', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({})
            })
            .then(response => response.json())
            .then(data => {
                if (data.status === 'success') {
                    interestBtn.disabled = true;
                    interestBtn.textContent = 'Interested!';
                    updateInterestCount();
                    // Show email submission section
                    if (emailSubmissionSection) {
                        emailSubmissionSection.style.display = 'block';
                    }
                } else {
                    console.error('Error tracking interest:', data.message);
                }
            })
            .catch(error => console.error('Error:', error));
        });
    }

    // Subscription Form
    const subscribeForm = document.getElementById('subscribeForm');
    if (subscribeForm) {
        subscribeForm.addEventListener('submit', function(e) {
            e.preventDefault();
            const emailInput = this.querySelector('input[type="email"]');
            const email = emailInput ? emailInput.value : '';
            
            fetch('/api/subscribe', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ email })
            })
            .then(response => response.json())
            .then(data => {
                if (data.status === 'success') {
                    alert('Thank you for subscribing!');
                    subscribeForm.reset();
                } else {
                    alert('There was an error subscribing. Please try again.');
                }
            })
            .catch(error => {
                console.error('Error:', error);
                alert('There was an error subscribing. Please try again.');
            });
        });
    }

    // Contact Form
    const contactForm = document.getElementById('contactForm');
    if (contactForm) {
        contactForm.addEventListener('submit', function(e) {
            e.preventDefault();
            const name = document.getElementById('name').value;
            const email = document.getElementById('contact-email').value;
            const message = document.getElementById('message').value;
            
            fetch('/api/contact', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ 
                    name: name,
                    email: email,
                    message: message,
                    source: 'landing_page'
                })
            })
            .then(response => response.json())
            .then(data => {
                if (data.status === 'success') {
                    alert('Thank you for your message! We will get back to you soon.');
                    contactForm.reset();
                } else {
                    alert('There was an error sending your message. Please try again.');
                }
            })
            .catch(error => {
                console.error('Error:', error);
                alert('There was an error sending your message. Please try again.');
            });
        });
    }
}); 