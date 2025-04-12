document.addEventListener('DOMContentLoaded', function () {
    const classifierForm = document.getElementById('classifier-form');
    const processBtn = document.getElementById('process-btn');
    const outputValue = document.getElementById('output-value');
    const loading = document.getElementById('loading');
    const resultContainer = document.getElementById('result-container');

    // Initially hide the loading indicator
    loading.style.display = 'none';

    // Handle form submission
    classifierForm.addEventListener('submit', function (e) {
        e.preventDefault();

        // Show loading indicator
        loading.style.display = 'block';
        resultContainer.style.opacity = '0.5';

        // Get form values
        const culmenLength = document.getElementById('culmen-length').value;
        const culmenDepth = document.getElementById('culmen-depth').value;
        const flipperLength = document.getElementById('flipper-length').value;
        const bodyMass = document.getElementById('body-mass').value;

        // Create payload for API
        const payload = {
            features: [
                parseFloat(culmenLength),
                parseFloat(culmenDepth),
                parseFloat(flipperLength),
                parseFloat(bodyMass)
            ]
        };

        // Try different API endpoints - first try /api/ClassifyPenguin directly
        fetch('/api/ClassifyPenguin', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(payload)
        })
            .then(response => {
                if (!response.ok) {
                    console.log(`First endpoint failed with status: ${response.status}`);
                    // If first endpoint fails, try the /classify endpoint as fallback
                    return fetch('/classify', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json'
                        },
                        body: JSON.stringify(payload)
                    });
                }
                return response;
            })
            .then(response => {
                if (!response.ok) {
                    throw new Error(`HTTP error!!11 Status: ${response.status}`);
                }
                return response.json();
            })
            .then(data => {
                // Update output value with formatted result
                const speciesName = data.species_name || data.class;
                const confidenceHtml = data.confidence ?
                    `<div class="mt-2">Confidence: ${(data.confidence * 100).toFixed(2)}%</div>` : '';

                outputValue.innerHTML = `
                <div class="alert alert-success mb-0">
                    <div class="h3">Predicted Species: ${speciesName}</div>
                    ${confidenceHtml}
                </div>
            `;

                resultContainer.style.opacity = '1';
            })
            .catch(error => {
                outputValue.innerHTML = `
                <div class="alert alert-danger mb-0">
                    <div class="h5">Error</div>
                    <p>${error.message}</p>
                </div>
            `;
                console.error('Error:', error);
            })
            .finally(() => {
                // Hide loading indicator
                loading.style.display = 'none';
            });
    });
});