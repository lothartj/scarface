import requests
import time
import concurrent.futures
import argparse
from urllib.parse import urljoin
from bs4 import BeautifulSoup
import colorama
from colorama import Fore, Style

# Initialize colorama for colored output
colorama.init()

class WebsitePathScanner:
    def __init__(self, base_url, delay=0.1, max_workers=5):
        # Ensure URL has proper scheme
        if not base_url.startswith(('http://', 'https://')):
            base_url = 'https://' + base_url
        
        self.base_url = base_url.rstrip('/')
        self.delay = delay
        self.max_workers = max_workers
        self.found_paths = set()
        self.session = requests.Session()
        self.extensions = ['', '.php', '.html', '.json', '.aspx', '.jsp', '.txt', '.bak', '.old']
        self.methods = ['GET', 'HEAD', 'POST', 'OPTIONS']
        self.callback = None
        self.wordlists = {}
        self.is_scanning = False

    def set_callback(self, callback):
        self.callback = callback

    def notify(self, status, message, path=None, code=None, counts=None):
        """
        Updated notify method to handle count updates
        """
        if self.callback:
            self.callback(status, message, path, code, counts)

    def load_wordlist(self, file_path):
        try:
            with open(file_path, 'r') as file:
                return [line.strip() for line in file if line.strip() and not line.startswith('#')]
        except FileNotFoundError:
            print(f"{Fore.RED}[ERROR] Wordlist not found: {file_path}{Style.RESET_ALL}")
            return []

    def scan_path(self, path, method='GET'):
        full_path = urljoin(self.base_url, path)
        try:
            response = self.session.request(method, full_path, allow_redirects=False)
            status = response.status_code
            
            if status < 400:
                self.found_paths.add(path)
                self.notify('found', f'Found path: {path}', path, status)
            
            return True
        except requests.RequestException as e:
            self.notify('error', f'Error scanning {path}: {str(e)}', path)
            return False
        finally:
            time.sleep(self.delay)

    def extract_paths_from_html(self, html_content):
        try:
            soup = BeautifulSoup(html_content, 'html.parser')
            # Extract links from various HTML elements
            for element in soup.find_all(['a', 'script', 'link', 'img']):
                for attr in ['href', 'src']:
                    path = element.get(attr)
                    if path and path.startswith('/'):
                        self.found_paths.add(path)
        except Exception as e:
            print(f"{Fore.RED}[ERROR] Failed to parse HTML: {str(e)}{Style.RESET_ALL}")

    def stop_scan(self):
        self.is_scanning = False
        self.notify('stopped', 'Scan stopped by user')

    def scan_website(self):
        self.is_scanning = True
        self.notify('status', f'Starting scan of {self.base_url}')
        
        all_paths = set()
        scanned_counts = {'common': 0, 'admin': 0, 'api': 0}
        
        # Load and limit paths based on user selection
        if self.wordlists.get('common', {}).get('enabled', True):
            limit = self.wordlists.get('common', {}).get('limit', 0)
            paths = self.load_wordlist('wordlists/common_paths.txt')
            if limit > 0:
                paths = paths[:limit]
            all_paths.update(paths)
        
        if self.wordlists.get('admin', {}).get('enabled', True):
            limit = self.wordlists.get('admin', {}).get('limit', 0)
            paths = self.load_wordlist('wordlists/admin_paths.txt')
            if limit > 0:
                paths = paths[:limit]
            all_paths.update(paths)
        
        if self.wordlists.get('api', {}).get('enabled', True):
            limit = self.wordlists.get('api', {}).get('limit', 0)
            paths = self.load_wordlist('wordlists/api_paths.txt')
            if limit > 0:
                paths = paths[:limit]
            all_paths.update(paths)

        total_paths = len(all_paths)
        
        for path in all_paths:
            if not self.is_scanning:
                self.notify('stopped', 'Scan stopped by user')
                return
            
            # Update counts based on which wordlist the path is from
            if path in self.load_wordlist('wordlists/common_paths.txt'):
                scanned_counts['common'] += 1
            elif path in self.load_wordlist('wordlists/admin_paths.txt'):
                scanned_counts['admin'] += 1
            elif path in self.load_wordlist('wordlists/api_paths.txt'):
                scanned_counts['api'] += 1
            
            # Send count updates
            self.notify('counts', 'Path counts updated', counts=scanned_counts)
            
            for ext in self.extensions:
                if not self.is_scanning:
                    return
                    
                full_path = f"{path}{ext}"
                
                for method in self.methods:
                    if not self.is_scanning:
                        return
                        
                    self.scan_path(full_path, method)
        
        if self.is_scanning:
            self.notify('complete', 'Scan Complete!')
        self.is_scanning = False
        
        print(f"Found {len(self.found_paths)} accessible paths")
        
        # Save results to file
        with open('scan_results.txt', 'w') as f:
            for path in sorted(self.found_paths):
                f.write(f"{path}\n")
        print(f"{Fore.GREEN}Results saved to scan_results.txt{Style.RESET_ALL}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Website Path Scanner')
    parser.add_argument('url', help='Base URL to scan (e.g., http://example.com)')
    parser.add_argument('--delay', type=float, default=0.1, help='Delay between requests in seconds')
    parser.add_argument('--workers', type=int, default=5, help='Number of concurrent workers')
    
    args = parser.parse_args()
    scanner = WebsitePathScanner(args.url, args.delay, args.workers)
    scanner.scan_website()