document.addEventListener('DOMContentLoaded', function() {
    // Get DOM elements
    const plaintext = document.getElementById('plaintext');
    const key1 = document.getElementById('key1');
    const key2 = document.getElementById('key2');
    const key3 = document.getElementById('key3');
    const key4 = document.getElementById('key4');
    const ciphertext = document.getElementById('ciphertext');
    const decryptedText = document.getElementById('decryptedText');
    const encryptBtn = document.getElementById('encryptBtn');
    const decryptBtn = document.getElementById('decryptBtn');
    const clearBtn = document.getElementById('clearBtn');

    // Visualization elements
    const dkssInput = document.getElementById('dkss-input');
    const dkssOutput = document.getElementById('dkss-output');
    const nrpeInput = document.getElementById('nrpe-input');
    const nrpeOutput = document.getElementById('nrpe-output');
    const vbmdInput = document.getElementById('vbmd-input');
    const vbmdOutput = document.getElementById('vbmd-output');
    const kdppInput = document.getElementById('kdpp-input');
    const kdppOutput = document.getElementById('kdpp-output');

    // API base URL - adjust this based on where your backend is running
    // For local development: 'http://localhost:5000'
    // For deployment: your deployed backend URL
    // Example deployed backend URLs:
    // - Render: 'https://your-app-name.onrender.com'
    // - Railway: 'https://your-app-name.up.railway.app'
    // - Heroku: 'https://your-app-name.herokuapp.com'
    const API_BASE_URL = window.location.hostname === 'localhost' ?
        'http://localhost:5000' :
        'https://aqimc-encryption-backend.onrender.com'; // Update this to your actual deployed backend URL

    // Encrypt button event listener
    encryptBtn.addEventListener('click', async function() {
        const text = plaintext.value.trim();
        const k1 = key1.value.trim();
        const k2 = key2.value.trim();
        const k3 = key3.value.trim();
        const k4 = key4.value.trim();

        if (!text) {
            showError('Please enter plaintext to encrypt');
            return;
        }

        if (!k1 || !k2 || !k3 || !k4) {
            showError('Please enter all four keys');
            return;
        }

        try {
            showLoading(encryptBtn, 'Encrypting...');
            const response = await fetch(`${API_BASE_URL}/encrypt`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    plaintext: text,
                    key1: k1,
                    key2: k2,
                    key3: k3,
                    key4: k4
                })
            });

            const result = await response.json();

            if (result.success) {
                ciphertext.value = result.encrypted_text;

                // Update visualization if steps are available
                if (result.steps) {
                    updateVisualization(result.steps);
                }

                showSuccess('Encryption successful!');
            } else {
                showError(result.error || 'Encryption failed');
            }
        } catch (error) {
            showError('Error connecting to server: ' + error.message);
        } finally {
            hideLoading(encryptBtn, 'Encrypt');
        }
    });

    // Decrypt button event listener
    decryptBtn.addEventListener('click', async function() {
        const text = ciphertext.value.trim();
        const k1 = key1.value.trim();
        const k2 = key2.value.trim();
        const k3 = key3.value.trim();
        const k4 = key4.value.trim();

        if (!text) {
            showError('Please enter ciphertext to decrypt');
            return;
        }

        if (!k1 || !k2 || !k3 || !k4) {
            showError('Please enter all four keys');
            return;
        }

        try {
            showLoading(decryptBtn, 'Decrypting...');
            const response = await fetch(`${API_BASE_URL}/decrypt`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    ciphertext: text,
                    key1: k1,
                    key2: k2,
                    key3: k3,
                    key4: k4
                })
            });

            const result = await response.json();

            if (result.success) {
                decryptedText.value = result.decrypted_text;
                showSuccess('Decryption successful!');
            } else {
                showError(result.error || 'Decryption failed');
            }
        } catch (error) {
            showError('Error connecting to server: ' + error.message);
        } finally {
            hideLoading(decryptBtn, 'Decrypt');
        }
    });

    // Clear button event listener
    clearBtn.addEventListener('click', function() {
        plaintext.value = '';
        key1.value = '';
        key2.value = '';
        key3.value = '';
        key4.value = '';
        ciphertext.value = '';
        decryptedText.value = '';
        clearVisualization();
        clearMessages();
    });

    // Helper functions
    function showLoading(button, text) {
        button.innerHTML = '<span class="loading"></span>';
        button.disabled = true;
    }

    function hideLoading(button, originalText) {
        button.innerHTML = originalText;
        button.disabled = false;
    }

    function showError(message) {
        clearMessages();
        const errorDiv = document.createElement('div');
        errorDiv.className = 'error';
        errorDiv.textContent = message;
        document.querySelector('.input-section').insertAdjacentElement('afterbegin', errorDiv);

        // Remove error after 5 seconds
        setTimeout(() => {
            if (errorDiv.parentNode) {
                errorDiv.parentNode.removeChild(errorDiv);
            }
        }, 5000);
    }

    function showSuccess(message) {
        clearMessages();
        const successDiv = document.createElement('div');
        successDiv.className = 'success';
        successDiv.textContent = message;
        document.querySelector('.input-section').insertAdjacentElement('afterbegin', successDiv);

        // Remove success after 3 seconds
        setTimeout(() => {
            if (successDiv.parentNode) {
                successDiv.parentNode.removeChild(successDiv);
            }
        }, 3000);
    }

    function clearMessages() {
        const existingMessages = document.querySelectorAll('.error, .success');
        existingMessages.forEach(msg => msg.remove());
    }

    function updateVisualization(steps) {
        // Update DKSS step
        if (steps.DKSS) {
            dkssInput.textContent = steps.DKSS.input || '-';
            dkssOutput.textContent = steps.DKSS.output || '-';
        }

        // Update NRPE step
        if (steps.NRPE) {
            nrpeInput.textContent = steps.NRPE.input || '-';
            nrpeOutput.textContent = steps.NRPE.output || '-';
        }

        // Update VBMD step
        if (steps.VBMD) {
            vbmdInput.textContent = steps.VBMD.input || '-';
            vbmdOutput.textContent = steps.VBMD.output || '-';
        }

        // Update KDPP step
        if (steps.KDPP) {
            kdppInput.textContent = steps.KDPP.input || '-';
            kdppOutput.textContent = steps.KDPP.output || '-';
        }
    }

    function clearVisualization() {
        dkssInput.textContent = '-';
        dkssOutput.textContent = '-';
        nrpeInput.textContent = '-';
        nrpeOutput.textContent = '-';
        vbmdInput.textContent = '-';
        vbmdOutput.textContent = '-';
        kdppInput.textContent = '-';
        kdppOutput.textContent = '-';
    }

    // Add example text for testing
    document.querySelector('header').insertAdjacentHTML('afterend',
        `<div class="example">
            <p><strong>Example:</strong> Try encrypting "HELLO" with keys "KEY1", "KEY2", "MATRIXKEY", "PERMUTE"</p>
        </div>`
    );

    // Add some styling for the example text
    const style = document.createElement('style');
    style.textContent = `
        .example {
            background: #e3f2fd;
            padding: 10px;
            border-radius: 5px;
            margin-bottom: 20px;
            text-align: center;
            border: 1px solid #bbdefb;
        }
        .example strong {
            color: #1976d2;
        }
    `;
    document.head.appendChild(style);
});