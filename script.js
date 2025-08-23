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
// Removed custom JS submission to allow Netlify native form handling

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
