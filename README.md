# Scarface Website Path Scanner

An advanced Python-based website path scanner that discovers accessible paths, endpoints, and potential security issues.

## Features

- Multi-threaded scanning for faster results
- Multiple HTTP methods (GET, POST, HEAD, OPTIONS)
- Common file extension checking
- HTML parsing to discover additional paths
- Colored console output
- Progress tracking
- Results saving
- Rate limiting to prevent server overload

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

Basic usage:
```bash
python scanner.py http://example.com
```

Advanced usage:
```bash
python scanner.py http://example.com --delay 0.2 --workers 10
```

Options:
- `--delay`: Delay between requests in seconds (default: 0.1)
- `--workers`: Number of concurrent workers (default: 5)

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

## License

MIT License