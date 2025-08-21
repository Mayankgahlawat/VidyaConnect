document.addEventListener('DOMContentLoaded', () => {
    const registerForm = document.getElementById('register-form');
    const loginForm = document.getElementById('login-form');

    if (registerForm) {
        registerForm.addEventListener('submit', async (event) => {
            event.preventDefault();
            const username = registerForm.querySelector('#username').value;
            const password = registerForm.querySelector('#password').value;
            const errorMessageDiv = registerForm.querySelector('#error-message');

            try {
                // Corrected URL
                const response = await fetch('/api/register', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ username, password })
                });
                
                const data = await response.json();

                if (!response.ok) {
                    errorMessageDiv.textContent = data.message || `Error: ${response.status}`;
                    errorMessageDiv.style.display = 'block';
                } else {
                    // On success, redirect to the login PAGE
                    window.location.href = '/login';
                }
            } catch (error) {
                errorMessageDiv.textContent = 'A network error occurred. Please try again.';
                errorMessageDiv.style.display = 'block';
            }
        });
    }

    if (loginForm) {
        loginForm.addEventListener('submit', async (event) => {
            event.preventDefault();
            const username = loginForm.querySelector('#username').value;
            const password = loginForm.querySelector('#password').value;
            const errorMessageDiv = loginForm.querySelector('#error-message');
            
            try {
                // Corrected URL
                const response = await fetch('/api/login', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ username, password })
                });

                const data = await response.json();

                if (!response.ok) {
                    errorMessageDiv.textContent = data.message || `Error: ${response.status}`;
                    errorMessageDiv.style.display = 'block';
                } else {
                    localStorage.setItem('jwt_token', data.token);
                    // On success, redirect to the main news PAGE
                    window.location.href = '/'; 
                }
            } catch (error) {
                errorMessageDiv.textContent = 'A network error occurred. Please try again.';
                errorMessageDiv.style.display = 'block';
            }
        });
    }
});