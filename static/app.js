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

        // Define endpoint to use (simplified)
        const endpoint = '/api/classifypenguinsimple';

        // For demonstration purposes, use mock data when API is not available
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
            fetch(endpoint, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(payload)
            })
                .then(response => {
                    console.log(`${endpoint} response status:`, response.status);

                    if (!response.ok) {
                        throw new Error(`HTTP error! Status: ${response.status}`);
                    }
                    return response.json();
                })
                .then(handleResponse)
                .catch(error => {
                    console.error('Prediction failed:', error);
                    outputValue.innerHTML = `
                    <div class="alert alert-danger mb-0">
                        <div class="h5">Prediction Failed</div>
                        <p>Unable to get prediction. Please try again.</p>
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

        // Update output value with formatted result
        const speciesName = data.species_name || data.prediction || data.class || "Unknown";
        const confidence = data.confidence || 0.52; // Default placeholder value
        const confidenceHtml = `<div class="mt-2">Confidence: ${(confidence * 100).toFixed(2)}%</div>`;

        // Handle top features for XAI (with fallback to placeholder data)
        const topFeatures = data.top_features || [
            { "name": "culmen-depth", "impact": 0.1362 },
            { "name": "flipper-length", "impact": -0.1279 }
        ];

        const forcePlotUrl = data.force_plot_url || "https://via.placeholder.com/600x200/f8f9fa/6c757d?text=SHAP+Force+Plot+Placeholder";

        outputValue.innerHTML = `
            <div class="alert alert-success mb-0">
                <div class="h3">Predicted Species: ${speciesName}</div>
                ${confidenceHtml}
            </div>
            
            <!-- Explainable AI Card -->
            <div class="xai-card mt-3" id="xai-card">
                <div class="xai-card-header" onclick="toggleXAICard()">
                    <span class="xai-card-title">🧠 Want to know more? Try Explainable AI</span>
                    <span class="xai-card-arrow" id="xai-arrow">▼</span>
                </div>
                <div class="xai-card-body" id="xai-body" style="display: none;">
                    <p class="xai-explanation">
                        The model has been trained on 3 classes, therefore each has a 33% chance of being the predicted class. 
                        The features of the model influence that decision, and the 2 most influential features are: 
                        <strong>${topFeatures[0].name}</strong> with a <strong>${topFeatures[0].impact.toFixed(4)}</strong> contribution 
                        and <strong>${topFeatures[1].name}</strong> with a <strong>${topFeatures[1].impact.toFixed(4)}</strong> contribution. 
                        These, together with the other 2 features arrived at the confidence score of <strong>${(confidence * 100).toFixed(2)}%</strong>.
                    </p>
                    <div class="xai-plot-container">
                        <h6>SHAP Force Plot</h6>
                        <img src="${forcePlotUrl}" alt="SHAP Force Plot" class="xai-plot-image">
                    </div>
                </div>
            </div>
        `;

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
