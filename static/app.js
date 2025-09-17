// Mobile-responsive Penguin Classifier Application
// Enhanced with touch interactions and accessibility features

document.addEventListener('DOMContentLoaded', function () {
    const classifierForm = document.getElementById('classifier-form');
    const processBtn = document.getElementById('process-btn');
    const outputValue = document.getElementById('output-value');
    const loading = document.getElementById('loading');
    const resultContainer = document.getElementById('result-container');

    // Mobile detection and optimization
    const isMobile = /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent);
    const isTouchDevice = 'ontouchstart' in window || navigator.maxTouchPoints > 0;

    // Initialize mobile-specific features
    if (isMobile || isTouchDevice) {
        initializeMobileFeatures();
    }

    // Initialize info card keyboard accessibility
    initializeInfoCardAccessibility();

    // Initially hide the loading indicator
    loading.style.display = 'none';

    // Enhanced form submission with mobile feedback
    classifierForm.addEventListener('submit', function (e) {
        e.preventDefault();

        // Provide immediate visual feedback for mobile users
        if (isTouchDevice) {
            processBtn.style.transform = 'scale(0.95)';
            setTimeout(() => {
                processBtn.style.transform = 'scale(1)';
            }, 150);
        }

        // Show loading indicator with accessibility
        loading.style.display = 'block';
        loading.setAttribute('aria-live', 'polite');
        resultContainer.style.opacity = '0.5';
        processBtn.disabled = true;
        processBtn.innerHTML = '🔄 Processing...';

        // Get form values
        const culmenLength = document.getElementById('culmen-length').value;
        const culmenDepth = document.getElementById('culmen-depth').value;
        const flipperLength = document.getElementById('flipper-length').value;
        const bodyMass = document.getElementById('body-mass').value;

        // Create payload for API - normalize the input values to match training data
        const payload = {
            features: [
                parseFloat(culmenLength),
                parseFloat(culmenDepth),
                parseFloat(flipperLength) / 10,  // Normalize flipper length by dividing by 10
                parseFloat(bodyMass) / 100       // Normalize body mass by dividing by 100
            ]
        };

        console.log('Sending request payload:', payload);

        // API Configuration - Point to dedicated Azure Functions App
        const API_CONFIG = {
            classify: 'https://penguin-classifier-consumption-dngqgqbga0g2eqgy.northeurope-01.azurewebsites.net/api/ClassifyPenguinSimple',
            xai: 'https://penguin-classifier-consumption-dngqgqbga0g2eqgy.northeurope-01.azurewebsites.net/api/XAI'
        };

        // In production, this would be the actual API call
        const useMockData = false; // Set to false when actual API is available

        if (useMockData) {
            // Simulate API delay
            setTimeout(() => {
                const mockResponse = {
                    prediction: "Adelie",
                    confidence: 0.00,
                    top_features: [
                        { "name": "culmen-depth", "impact": 0.0 },
                        { "name": "flipper-length", "impact": -0.0 }
                    ],
                    force_plot_url: "https://via.placeholder.com/600x200/e3f2fd/2196f3?text=SHAP+Force+Plot+%28Demo%29"
                };
                handleResponse(mockResponse);
            }, 1500);
        } else {
            // Make the actual API call
            fetch(API_CONFIG.classify, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(payload)
            })
                .then(response => {
                    console.log(`${API_CONFIG.classify} response status:`, response.status);

                    if (!response.ok) {
                        throw new Error(`HTTP error! Status: ${response.status}`);
                    }
                    return response.json();
                })
                .then(handleResponse)
                .catch(error => {
                    console.error('Prediction failed:', error);
                    let errorMessage = 'Unable to get prediction. Please try again.';

                    // More specific error messages
                    if (error.name === 'TypeError' && error.message.includes('fetch')) {
                        errorMessage = 'Network error. Please check your connection and try again.';
                    } else if (error.message.includes('XAI')) {
                        errorMessage = 'Prediction successful, but explainable AI analysis is currently unavailable.';
                    }

                    outputValue.innerHTML = `
                    <div class="alert alert-danger mb-0">
                        <div class="h5">Prediction Failed</div>
                        <p>${errorMessage}</p>
                        <small class="text-muted">Error: ${error.message}</small>
                    </div>
                `;
                    resetFormState();
                });
        }
    });

    // Function to handle a successful response
    function handleResponse(data) {
        console.log('Response data:', data);

        // Handle error in the response data
        if (data.error || data.success === false) {
            let errorMessage = data.error || data.message || "Unknown error";

            outputValue.innerHTML = `
                <div class="alert alert-warning mb-0">
                    <div class="h5">API Message</div>
                    <p>${errorMessage}</p>
                </div>
            `;
            resetFormState();
            return;
        }

        // Extract response data
        const speciesName = data.species_name || data.prediction || data.class || "Unknown";
        const confidence = data.confidence || 0.52;
        const confidenceHtml = `<div class="mt-2">Confidence: ${(confidence * 100).toFixed(2)}%</div>`;

        // Check for XAI data availability with proper validation
        const hasXAIData = data.top_features &&
            Array.isArray(data.top_features) &&
            data.top_features.length >= 2 &&
            data.top_features.every(f => f.name && typeof f.impact === 'number');

        let xaiContent = '';

        if (hasXAIData) {
            // Use real XAI data from backend
            const topFeatures = data.top_features;

            xaiContent = `
                <!-- Explainable AI Card with Real Data -->
                <div class="xai-card mt-3" id="xai-card">
                    <div class="xai-card-header" id="xai-card-header" tabindex="0" role="button" aria-expanded="false">
                        <span class="xai-card-title">🧠 Explainable AI Analysis</span>
                        <span class="xai-card-arrow" id="xai-arrow">▼</span>
                    </div>
                    <div class="xai-card-body" id="xai-body" style="display: none;">
                        <h6>Why This Prediction?</h6>
                        <p>The model analyzed your penguin's features using <strong>SHAP (SHapley Additive exPlanations)</strong> values to explain this <strong>${speciesName}</strong> prediction.</p>
                        <p><strong>Top 2 Most Influential Features:</strong></p>
                        <ul>
                            <li><strong>${topFeatures[0].name}:</strong> Impact score of <strong>${topFeatures[0].impact > 0 ? '+' : ''}${topFeatures[0].impact.toFixed(4)}</strong></li>
                            <li><strong>${topFeatures[1].name}:</strong> Impact score of <strong>${topFeatures[1].impact > 0 ? '+' : ''}${topFeatures[1].impact.toFixed(4)}</strong></li>
                        </ul>
                        <p><strong>Interpretation:</strong> Positive values increase the likelihood of this species, while negative values decrease it. Final confidence score: <strong>${(confidence * 100).toFixed(2)}%</strong>.</p>
                    </div>
                </div>
            `;
        } else {
            // Simple failure message when XAI is unavailable
            xaiContent = `
                <div class="alert alert-warning mt-3">
                    <strong>⚠️ XAI Analysis Failed</strong><br>
                    Explainable AI analysis is currently unavailable.
                </div>
            `;
        }

        outputValue.innerHTML = `
            <div class="alert alert-success mb-0">
                <div class="h3">Predicted Species: ${speciesName}</div>
                ${confidenceHtml}
            </div>
            ${xaiContent}
        `;

        // Add event listeners for XAI card interaction
        const xaiHeader = document.getElementById('xai-card-header');
        if (xaiHeader) {
            xaiHeader.addEventListener('click', toggleXAICard);
            xaiHeader.addEventListener('keypress', function (e) {
                if (e.key === 'Enter' || e.key === ' ') {
                    e.preventDefault();
                    toggleXAICard();
                }
            });
        }

        resetFormState();
    }

    // Reset form state function for mobile UX
    function resetFormState() {
        loading.style.display = 'none';
        resultContainer.style.opacity = '1';
        processBtn.disabled = false;
        processBtn.innerHTML = '🔍 Classify Penguin Species';
        processBtn.setAttribute('aria-live', 'polite');
    }

    // Mobile-specific initialization
    function initializeMobileFeatures() {
        // Add touch feedback to all interactive elements
        const interactiveElements = document.querySelectorAll('button, .species-card, .form-control');

        interactiveElements.forEach(element => {
            element.addEventListener('touchstart', function () {
                this.style.opacity = '0.7';
            }, { passive: true });

            element.addEventListener('touchend', function () {
                this.style.opacity = '1';
            }, { passive: true });
        });

        // Optimize form inputs for mobile
        const inputs = document.querySelectorAll('input[type="number"]');
        inputs.forEach(input => {
            // Set appropriate inputmode based on field type
            if (input.id === 'body-mass' || input.id === 'flipper-length') {
                // Integer fields - use numeric keyboard
                input.setAttribute('inputmode', 'numeric');
                input.setAttribute('pattern', '[0-9]*');
            } else {
                // Decimal fields (culmen measurements) - use decimal keyboard
                input.setAttribute('inputmode', 'decimal');
                input.setAttribute('pattern', '[0-9]*(\.[0-9]*)?');
            }

            // Add visual feedback on focus
            input.addEventListener('focus', function () {
                this.parentElement.style.transform = 'scale(1.02)';
            });

            input.addEventListener('blur', function () {
                this.parentElement.style.transform = 'scale(1)';
            });
        });

        // Add haptic feedback for supported devices
        if ('vibrate' in navigator) {
            processBtn.addEventListener('click', function () {
                navigator.vibrate(50); // Subtle haptic feedback
            });
        }

        // Prevent zoom on input focus (iOS Safari)
        const meta = document.createElement('meta');
        meta.name = 'viewport';
        meta.content = 'width=device-width, initial-scale=1, maximum-scale=1, user-scalable=no';

        // Only apply if not already set
        if (!document.querySelector('meta[name="viewport"]')) {
            document.getElementsByTagName('head')[0].appendChild(meta);
        }
    }
});

// Function to toggle XAI card visibility
function toggleXAICard() {
    const xaiBody = document.getElementById('xai-body');
    const xaiArrow = document.getElementById('xai-arrow');

    if (xaiBody.style.display === 'none') {
        xaiBody.style.display = 'block';
        xaiArrow.textContent = '▲';
        xaiArrow.setAttribute('aria-label', 'Collapse explanation');
    } else {
        xaiBody.style.display = 'none';
        xaiArrow.textContent = '▼';
        xaiArrow.setAttribute('aria-label', 'Expand explanation');
    }
}

// Function to set species reference values
function setSpeciesValues(species) {
    const speciesData = {
        'adelie': {
            culmenLength: 38.8,
            culmenDepth: 18.3,
            flipperLength: 190,
            bodyMass: 3701
        },
        'chinstrap': {
            culmenLength: 47.5,
            culmenDepth: 15.0,
            flipperLength: 217,
            bodyMass: 5076
        },
        'gentoo': {
            culmenLength: 48.8,
            culmenDepth: 18.4,
            flipperLength: 196,
            bodyMass: 3733
        }
    };

    const data = speciesData[species];
    if (data) {
        document.getElementById('culmen-length').value = data.culmenLength;
        document.getElementById('culmen-depth').value = data.culmenDepth;
        document.getElementById('flipper-length').value = data.flipperLength;
        document.getElementById('body-mass').value = data.bodyMass;

        // Add visual feedback
        const form = document.getElementById('classifier-form');
        form.style.backgroundColor = '#e8f5e8';
        setTimeout(() => {
            form.style.backgroundColor = '';
        }, 500);

        // Show which species was selected
        const outputValue = document.getElementById('output-value');
        outputValue.innerHTML = `
            <div class="alert alert-info mb-0">
                <div class="h5">🐧 ${species.charAt(0).toUpperCase() + species.slice(1)} penguin values loaded</div>
                <p>Click "Classify Penguin Species" to test the prediction</p>
            </div>
        `;
    }
}

// Function to initialize info card keyboard accessibility
function initializeInfoCardAccessibility() {
    const infoCardHeaders = document.querySelectorAll('.info-card-header');
    const isTouchDevice = 'ontouchstart' in window || navigator.maxTouchPoints > 0;

    infoCardHeaders.forEach(header => {
        header.addEventListener('keydown', function (e) {
            // Handle Enter and Space key presses
            if (e.key === 'Enter' || e.key === ' ') {
                e.preventDefault();
                // Extract card type from the header's parent id
                const cardId = this.parentElement.id;
                const cardType = cardId.replace('-card', '');
                toggleInfoCard(cardType);
            }
        });

        // Add touch feedback for mobile
        if (isTouchDevice) {
            header.addEventListener('touchstart', function () {
                this.style.opacity = '0.8';
            }, { passive: true });

            header.addEventListener('touchend', function () {
                this.style.opacity = '1';
            }, { passive: true });
        }
    });
}

// Function to toggle information card visibility
function toggleInfoCard(cardType) {
    const cardBody = document.getElementById(`${cardType}-body`);
    const cardArrow = document.getElementById(`${cardType}-arrow`);
    const cardHeader = document.querySelector(`#${cardType}-card .info-card-header`);

    if (cardBody.style.display === 'none') {
        cardBody.style.display = 'block';
        cardArrow.textContent = '▲';
        cardArrow.setAttribute('aria-label', `Collapse ${cardType} explanation`);
        cardHeader.setAttribute('aria-expanded', 'true');
    } else {
        cardBody.style.display = 'none';
        cardArrow.textContent = '▼';
        cardArrow.setAttribute('aria-label', `Expand ${cardType} explanation`);
        cardHeader.setAttribute('aria-expanded', 'false');
    }
}
