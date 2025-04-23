document.addEventListener('DOMContentLoaded', function() {
    const socket = io();
    const container = document.getElementById('scannerContainer');
    const header = container.querySelector('.scanner-header');
    const urlInput = document.getElementById('urlInput');
    const startButton = document.getElementById('startScan');
    const resultsArea = document.getElementById('resultsArea');
    const scanStatus = document.getElementById('scanStatus');
    const pathCount = document.getElementById('pathCount');

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

    // Handle scanning
    let foundPaths = 0;

    startButton.addEventListener('click', function() {
        const url = urlInput.value.trim();
        if (!url) {
            alert('Please enter a URL');
            return;
        }

        // Reset UI
        resultsArea.innerHTML = '';
        foundPaths = 0;
        pathCount.textContent = 'Paths: 0';
        scanStatus.textContent = 'Scanning...';
        startButton.disabled = true;

        // Start scan
        socket.emit('start_scan', { url: url });
    });

    socket.on('scan_update', function(data) {
        const resultDiv = document.createElement('div');
        resultDiv.className = 'result-item';

        switch(data.status) {
            case 'started':
                scanStatus.textContent = 'Scanning...';
                break;
            case 'found':
                foundPaths++;
                pathCount.textContent = `Paths: ${foundPaths}`;
                resultDiv.className += ' result-found';
                resultDiv.textContent = `✓ ${data.path} → ${data.code}`;
                break;
            case 'error':
                resultDiv.className += ' result-error';
                resultDiv.textContent = `✗ ${data.message}`;
                break;
            case 'complete':
                scanStatus.textContent = 'Complete';
                startButton.disabled = false;
                break;
        }

        if (data.message) {
            resultsArea.appendChild(resultDiv);
            resultsArea.scrollTop = resultsArea.scrollHeight;
        }
    });
});
