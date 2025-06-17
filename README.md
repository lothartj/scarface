# Scarface Website Path Scanner.

![Scarface poster](https://image.tmdb.org/t/p/original/iQ5ztdjvteGeboxtmRdXEChJOHh.jpg)

An advanced Python-based website path scanner with a modern web interface that discovers accessible paths, endpoints, and potential security issues.

## Features

- Modern, draggable web interface
- Real-time scanning results
- Path limit controls for each wordlist
- Live scanning progress counters
- Copy-to-clipboard functionality
- Multiple HTTP methods (GET, POST, HEAD, OPTIONS)
- Common file extension checking
- HTML parsing to discover additional paths
- Colored console output
- Results saving
- Rate limiting to prevent server overload
- Immediate scan stopping capability

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/scarface.git
   cd scarface
   ```

2. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. Start the web interface:
   ```bash
   python app.py
   ```

2. Open your browser and go to:
   ```
   http://localhost:5000
   ```

3. In the web interface:
   - Enter the target URL
   - Select which wordlists to use (Common, Admin, API)
   - Set path limits for each wordlist (optional)
   - Click "Start Scan" to begin
   - Use "Stop Scan" to immediately halt the scanning process

## Features Explained

### Wordlist Selection
- Common Paths: General website endpoints
- Admin Paths: Administrative and backend paths
- API Paths: API endpoints and routes

### Path Limiting
Set the number of paths to scan from each wordlist:
- Leave empty to scan all paths
- Enter a number to limit paths (e.g., "10" to scan only first 10 paths)

### Real-time Results
- Live counter for each wordlist's progress
- Instant display of found paths
- Copy button for each discovered URL
- Status updates during scanning

### Interface Controls
- Draggable window interface
- Start/Stop scanning controls
- Clear status indicators
- Progress tracking

## Wordlists

The scanner uses three wordlist files in the `wordlists` directory:
- `common_paths.txt`: General website paths
- `admin_paths.txt`: Administrative paths
- `api_paths.txt`: API endpoints

You can customize these files to add or remove paths as needed.

## Important Notes

- Only scan websites you own or have permission to test
- Be mindful of rate limiting and server load
- Some websites may block automated scanning
- Use responsibly and ethically
- The scanner respects robots.txt and rate limits by default

## License

MIT License

## Contributing

Feel free to submit issues, fork the repository, and create pull requests for any improvements.
