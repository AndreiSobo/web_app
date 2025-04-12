document.addEventListener('DOMContentLoaded', function () {
    const classifierForm = document.getElementById('classifier-form');
    const processBtn = document.getElementById('process-btn');
    const outputValue = document.getElementById('output-value');
    const loading = document.getElementById('loading');
    const resultContainer = document.getElementById('result-container');

    // Add debug mode checkbox
    const debugSection = document.createElement('div');
    debugSection.className = 'mt-3 mb-3 text-end';
    debugSection.innerHTML = `
        <div class="form-check form-switch">
            <input class="form-check-input" type="checkbox" id="debug-mode">
            <label class="form-check-label" for="debug-mode">Debug Mode</label>
        </div>
    `;
    classifierForm.appendChild(debugSection);

    const debugMode = document.getElementById('debug-mode');

    // Initially hide the loading indicator
    loading.style.display = 'none';

    // Add a test debug button that only shows in debug mode
    const debugButtonDiv = document.createElement('div');
    debugButtonDiv.className = 'd-grid mb-3';
    debugButtonDiv.style.display = 'none';
    debugButtonDiv.innerHTML = `
        <button type="button" id="debug-btn" class="btn btn-secondary">
            Test Debug Endpoint
        </button>
    `;
    classifierForm.appendChild(debugButtonDiv);
    const debugButton = document.getElementById('debug-btn');

    // Show/hide debug elements based on checkbox
    debugMode.addEventListener('change', function () {
        debugButtonDiv.style.display = debugMode.checked ? 'block' : 'none';
    });

    // Debug button handler
    debugButton.addEventListener('click', function () {
        loading.style.display = 'block';
        resultContainer.style.opacity = '0.5';

        fetch('/api/debug', {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json'
            }
        })
            .then(response => {
                if (!response.ok) {
                    throw new Error(`Debug endpoint error: ${response.status} ${response.statusText}`);
                }
                return response.json();
            })
            .then(data => {
                let debugHtml = `
                <div class="alert alert-info mb-0">
                    <h4>Debug Information</h4>
                    <pre style="max-height: 400px; overflow: auto;">${JSON.stringify(data, null, 2)}</pre>
                </div>
            `;
                outputValue.innerHTML = debugHtml;
                resultContainer.style.opacity = '1';
            })
            .catch(error => {
                outputValue.innerHTML = `
                <div class="alert alert-danger mb-0">
                    <div class="h5">Debug Error</div>
                    <p>${error.message}</p>
                </div>
            `;
                console.error('Debug Error:', error);
            })
            .finally(() => {
                loading.style.display = 'none';
            });
    });

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

        console.log('Sending request payload:', payload);

        // Define all potential endpoint variants to try
        const endpoints = [
            '/api/ClassifyPenguin',  // Standard path for Azure Static Web Apps
            '/api/classifypenguin',  // Lowercase variant (Azure Functions can be case-insensitive)
            '/ClassifyPenguin',      // Direct function name
            '/classify'              // Our custom route from staticwebapp.config.json
        ];

        // Try each endpoint one by one
        tryEndpoints(endpoints, payload, 0);
    });

    // Try multiple endpoints in sequence
    function tryEndpoints(endpoints, payload, index) {
        if (index >= endpoints.length) {
            // All endpoints failed
            outputValue.innerHTML = `
                <div class="alert alert-danger mb-0">
                    <div class="h5">All API endpoints failed</div>
                    <p>Tried: ${endpoints.join(', ')}</p>
                    ${debugMode.checked ? `
                        <hr>
                        <p>Try these troubleshooting steps:</p>
                        <ol>
                            <li>Check if the Debug endpoint works (/api/DebugEndpoint)</li>
                            <li>Ensure all environment variables are set in Azure</li>
                            <li>Check Azure Function logs in the Azure Portal</li>
                        </ol>
                    ` : ''}
                </div>
            `;
            loading.style.display = 'none';
            return;
        }

        const endpoint = endpoints[index];
        console.log(`Trying endpoint: ${endpoint}`);

        if (debugMode.checked) {
            outputValue.innerHTML = `
                <div class="alert alert-info mb-0">
                    <div class="h5">Trying endpoint ${index + 1}/${endpoints.length}</div>
                    <p>${endpoint}...</p>
                </div>
            `;
        }

        callEndpoint(endpoint, payload)
            .then(handleResponse)
            .catch(error => {
                console.error(`Endpoint ${endpoint} failed:`, error);
                // Try next endpoint
                tryEndpoints(endpoints, payload, index + 1);
            });
    }

    // Function to call an endpoint with error handling
    function callEndpoint(url, payload) {
        return fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(payload)
        })
            .then(response => {
                console.log(`${url} response status:`, response.status);

                if (!response.ok) {
                    throw new Error(`HTTP error! Status: ${response.status}, URL: ${url}`);
                }
                return response.json();
            });
    }

    // Function to handle a successful response
    function handleResponse(data) {
        console.log('Response data:', data);

        // Handle error in the response data
        if (data.error) {
            let errorDetails = '';
            if (debugMode.checked && data.details) {
                errorDetails = `<hr><div class="small mt-2"><pre>${data.details}</pre></div>`;
            }

            outputValue.innerHTML = `
                <div class="alert alert-danger mb-0">
                    <div class="h5">API Error</div>
                    <p>${data.error}</p>
                    ${errorDetails}
                </div>
            `;
            resultContainer.style.opacity = '1';
            return;
        }

        // Update output value with formatted result
        const speciesName = data.species_name || data.class;
        const confidenceHtml = data.confidence ?
            `<div class="mt-2">Confidence: ${(data.confidence * 100).toFixed(2)}%</div>` : '';

        let additionalInfo = '';
        if (debugMode.checked) {
            additionalInfo = `
                <hr>
                <div class="small text-muted mt-2">
                    <strong>Debug Info:</strong>
                    <pre>${JSON.stringify(data, null, 2)}</pre>
                </div>
            `;
        }

        outputValue.innerHTML = `
            <div class="alert alert-success mb-0">
                <div class="h3">Predicted Species: ${speciesName}</div>
                ${confidenceHtml}
                ${additionalInfo}
            </div>
        `;

        resultContainer.style.opacity = '1';
    }
});