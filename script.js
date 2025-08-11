function initializeMobileNav(){const e=document.querySelector(".nav-toggle"),t=document.querySelector(".site-nav");e&&t&&e.addEventListener("click",(()=>{const n=t.classList.toggle("open");e.setAttribute("aria-expanded",String(n))}))}function initializeNewsletterForm(){
  const form = document.getElementById("newsletter-form");
  if (!form) return;
  
  form.addEventListener("submit", async (e) => {
    // Don't prevent default - let Netlify handle the submission
    // e.preventDefault();
    
    const nameInput = form.querySelector('input[name="name"]');
    const emailInput = form.querySelector('input[name="email"]');
    
    const name = nameInput?.value?.trim();
    const email = emailInput?.value?.trim();
    
    if (!name || !email) {
      e.preventDefault();
      return;
    }
    
    // Store in localStorage
    localStorage.setItem("newsletter-optin", email);
    
    // Let the form submit naturally to Netlify
    // The success page will handle the user experience
  });
}function setCurrentYear(){const e=document.getElementById("year");e&&(e.textContent=String((new Date).getFullYear()))}document.addEventListener("DOMContentLoaded",(()=>{initializeMobileNav(),initializeNewsletterForm(),setCurrentYear()}));

// Contact form handling
document.addEventListener('DOMContentLoaded', function() {
  const contactForm = document.getElementById('contact-form');
  if (contactForm) {
    contactForm.addEventListener('submit', handleContactForm);
  }
});

function handleContactForm(e) {
  e.preventDefault();
  
  const form = e.target;
  const formData = new FormData(form);
  const submitButton = form.querySelector('button[type="submit"]');
  const messageDiv = document.getElementById('form-message');
  
  // Disable submit button and show loading state
  submitButton.disabled = true;
  submitButton.textContent = 'Sending...';
  
  // Convert FormData to JSON
  const data = {};
  formData.forEach((value, key) => {
    data[key] = value;
  });
  
  // Submit form
  fetch('/', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(data)
  })
  .then(response => response.json())
  .then(data => {
    if (data.success) {
      showFormMessage('success', data.message);
      form.reset();
    } else {
      showFormMessage('error', 'Something went wrong. Please try again.');
    }
  })
  .catch(error => {
    console.error('Error:', error);
    showFormMessage('error', 'Something went wrong. Please try again.');
  })
  .finally(() => {
    // Re-enable submit button
    submitButton.disabled = false;
    submitButton.textContent = 'Send message';
  });
}

function showFormMessage(type, message) {
  const messageDiv = document.getElementById('form-message');
  if (messageDiv) {
    messageDiv.textContent = message;
    messageDiv.className = `form-message ${type}`;
    messageDiv.style.display = 'block';
    
    // Hide message after 5 seconds
    setTimeout(() => {
      messageDiv.style.display = 'none';
    }, 5000);
  }
}
