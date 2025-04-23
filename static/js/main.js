document.addEventListener('DOMContentLoaded', function() {
    const socket = io();
    const container = document.getElementById('scannerContainer');
    const header = container.querySelector('.scanner-header');
    const urlInput = document.getElementById('urlInput');
    const startButton = document.getElementById('startScan');
    const resultsArea = document.getElementById('resultsArea');
    const scanStatus = document.getElementById('scanStatus');
    const pathCount = document.getElementById('pathCount');
    const stopButton = document.getElementById('stopScan');

    // Make the container draggable
    let isDragging = false;
    let currentX;
    let currentY;
    let initialX;
    let initialY;
    let xOffset = 0;
    let yOffset = 0;

    header.addEventListener('mousedown', dragStart);
    document.addEventListener('mousemove', drag);
    document.addEventListener('mouseup', dragEnd);

    function dragStart(e) {
        initialX = e.clientX - xOffset;
        initialY = e.clientY - yOffset;

        if (e.target === header || e.target.parentNode === header) {
            isDragging = true;
        }
    }

    function drag(e) {
        if (isDragging) {
            e.preventDefault();
            currentX = e.clientX - initialX;
            currentY = e.clientY - initialY;

            xOffset = currentX;
            yOffset = currentY;

            setTranslate(currentX, currentY, container);
        }
    }

    function dragEnd(e) {
        initialX = currentX;
        initialY = currentY;
        isDragging = false;
    }

    function setTranslate(xPos, yPos, el) {
        el.style.transform = `translate(${xPos}px, ${yPos}px)`;
    }

    // Handle scanning with wordlist selection
    let foundPaths = 0;

    startButton.addEventListener('click', function() {
        const url = urlInput.value.trim();
        if (!url) {
            alert('Please enter a URL');
            return;
        }

        // Get wordlist selections and limits
        const wordlists = {
            common: {
                enabled: document.getElementById('commonPaths').checked,
                limit: parseInt(document.getElementById('commonLimit').value) || 0
            },
            admin: {
                enabled: document.getElementById('adminPaths').checked,
                limit: parseInt(document.getElementById('adminLimit').value) || 0
            },
            api: {
                enabled: document.getElementById('apiPaths').checked,
                limit: parseInt(document.getElementById('apiLimit').value) || 0
            }
        };

        // Reset UI
        resultsArea.innerHTML = '';
        foundPaths = 0;
        pathCount.textContent = 'Paths: 0';
        scanStatus.textContent = 'Scanning...';
        startButton.disabled = true;
        stopButton.disabled = false;

        // Start scan with wordlist config
        socket.emit('start_scan', { 
            url: url,
            wordlists: wordlists
        });
    });

    stopButton.addEventListener('click', function() {
        socket.emit('stop_scan');
        stopButton.disabled = true;
    });

    // Copy functionality
    function copyToClipboard(text) {
        navigator.clipboard.writeText(text).then(() => {
            // Success handling is in the click handler
        }).catch(err => {
            console.error('Failed to copy:', err);
        });
    }

    socket.on('scan_update', function(data) {
        if (data.status === 'found') {
            foundPaths++;
            pathCount.textContent = `Paths: ${foundPaths}`;
            
            const resultDiv = document.createElement('div');
            resultDiv.className = 'result-item result-found';
            
            const fullUrl = new URL(data.path, data.baseUrl).href;
            
            resultDiv.innerHTML = `
                <span class="result-path">✓ ${fullUrl}</span>
                <button class="copy-button" title="Copy URL">
                    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24">
                        <path fill="currentColor" d="M16 1H4C3 1 2 2 2 3v14h2V3h12V1zm3 4H8C7 5 6 6 6 7v14c0 1 1 2 2 2h11c1 0 2-1 2-2V7c0-1-1-2-2-2zm0 16H8V7h11v14z"/>
                    </svg>
                </button>
            `;

            const copyButton = resultDiv.querySelector('.copy-button');
            copyButton.addEventListener('click', function() {
                copyToClipboard(fullUrl);
                this.classList.add('copied');
                setTimeout(() => this.classList.remove('copied'), 1000);
            });

            resultsArea.appendChild(resultDiv);
            resultsArea.scrollTop = resultsArea.scrollHeight;
        } else if (data.status === 'complete' || data.status === 'stopped') {
            scanStatus.textContent = data.status === 'complete' ? 'Complete' : 'Stopped';
            startButton.disabled = false;
            stopButton.disabled = true;
        }
    });
});
