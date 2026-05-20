# Virtual Host Scanner v2.0 - Enhanced Edition

<div align="center">

**Fast, modern, and feature-rich virtual host discovery tool**

[![Python](https://img.shields.io/badge/python-3.9%2B-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

</div>

---

## Features

### Core Features
* 🚀 **Async/Concurrent Scanning** - High-performance scanning with configurable concurrency
* 🔒 **SSL/TLS Support** - Works seamlessly over HTTP and HTTPS
* 🎯 **Smart DNS Lookups** - Automatic reverse DNS lookups to expand wordlists
* 🧠 **Fuzzy Logic** - Similarity detection to identify related virtual hosts
* 🎨 **Rich UI** - Beautiful progress bars and colored output
* 📊 **Multiple Output Formats** - Normal, JSON, and grepable output

### Advanced Features
* 🎯 **Multi-Port Scanning** - Scan multiple ports simultaneously with automatic result aggregation
* ⚡ **Rate Limiting** - Control request rate to avoid overwhelming servers
* 🛡️ **WAF Bypass Headers** - Optional headers to test WAF configurations
* 🔍 **First Hit Mode** - Stop on first successful discovery (useful for CTFs)
* 🌐 **Proxy Support** - HTTP/HTTPS/SOCKS5 proxy support
* ⏱️ **Configurable Timeouts** - Fine-tune connection timeout values
* 🎭 **Custom User Agents** - Random or custom user-agent support
* 📝 **Comprehensive Logging** - Detailed logging for troubleshooting

### Performance Improvements
* Traditional synchronous scanning
* **NEW**: Async scanning with up to 10x faster performance
* Configurable concurrency levels (default: 10 concurrent requests)
* Progress tracking with real-time statistics

---

## Installation

### Prerequisites

* Python 3.9 or higher
* pip (Python package manager)

### Method 1: Using pip (Recommended)

```bash
# Clone the repository
git clone https://github.com/your-repo/vscan.git
cd vscan

# Install dependencies
pip install -r requirements.txt

# Install vscan
python setup.py install

# Verify installation
vscan --help
```

### Method 2: Development Installation

```bash
# Clone the repository
git clone https://github.com/your-repo/vscan.git
cd vscan

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install in development mode
pip install -e .
pip install -r test-requirements.txt

# Run tests
pytest
```

### Method 3: Using pip directly

```bash
pip install vscan
```


### Method 4: Docker (Containerized)

The Docker image is optimized with multi-stage builds for minimal size.

```bash
# Build the Docker image
docker build -t vscan .

# Run vscan in Docker (basic usage)
docker run --rm vscan -t example.com

# Run with custom wordlist (mount volume)
docker run --rm -v $(pwd)/wordlists:/wordlists vscan \
  -t example.com -w /wordlists/custom.txt

# Interactive mode
docker run -it --rm vscan /bin/bash
```

---

## Quick Start

### Basic Scan
```bash
# Simple HTTP scan
vscan -t example.com

# HTTPS scan
vscan -t example.com --ssl -p 443
```

### With Custom Wordlist
```bash
vscan -t example.com -w ./wordlists/custom.txt
```

### Fast Scan with High Concurrency
```bash
vscan -t example.com --concurrency 50 -v
```

---

## Usage

### Core Arguments

| Argument | Type | Default | Description |
|----------|------|---------|-------------|
| `-t TARGET_HOSTS` | Required | - | Target host to scan |
| `-w WORDLISTS` | Optional | built-in | Wordlist file(s) to use (comma-separated for multiple) |
| `-p PORT` | Optional | 80 | Port to connect to (single port) |
| `--ports PORTS` | Optional | - | **NEW** Scan multiple ports (comma-separated or ranges) |
| `-r REAL_PORT` | Optional | PORT | Real port for Host header (useful for port forwarding) |
| `-b BASE_HOST` | Optional | TARGET | Base host for %s substitution in wordlist |
| `-v, --verbose` | Flag | False | Enable verbose output |

### SSL/TLS Options

| Argument | Description |
|----------|-------------|
| `--ssl` | Use HTTPS instead of HTTP |

### Performance Options

| Argument | Type | Default | Description |
|----------|------|---------|-------------|
| `--concurrency` | Integer | 10 | Number of concurrent requests (async mode) |
| `--rate-limit` | Integer | 0 | Delay in seconds between requests |
| `--timeout` | Integer | 10 | Request timeout in seconds |
| `--no-async` | Flag | False | Disable async scanning (use traditional sequential) |

### Filtering Options

| Argument | Type | Default | Description |
|----------|------|---------|-------------|
| `--ignore-http-codes` | String | 404 | Comma-separated HTTP codes to ignore |
| `--ignore-content-length` | Integer | 0 | Ignore responses with this content length |
| `--unique-depth` | Integer | 1 | Show matches found N times or less |

### Discovery Options

| Argument | Description |
|----------|-------------|
| `--no-lookups` | Disable reverse DNS lookups |
| `--first-hit` | Stop after first successful match (CTF mode) |
| `--fuzzy-logic` | Enable fuzzy matching to compare page similarity |

### Header Options

| Argument | Description |
|----------|-------------|
| `--user-agent UA` | Specify custom user-agent string |
| `--random-agent` | Use random user-agent for each request |
| `--waf` | Add WAF bypass headers (X-Forwarded-For, etc.) |
| `--prefix PREFIX` | Add prefix to each wordlist entry |
| `--suffix SUFFIX` | Add suffix to each wordlist entry |

### Network Options

| Argument | Description |
|----------|-------------|
| `--proxy PROXY_URL` | Use proxy (http://... or socks5://...) |

### Output Options

| Argument | Description |
|----------|-------------|
| `-oN FILE` | Write normal output to file |
| `-oJ FILE` | Write JSON output to file |
| `-oG FILE` | Write grepable output to file |



---

## Examples

### Basic Examples

#### 1. Simple HTTP Scan
```bash
vscan -t example.com
```

#### 2. HTTPS Scan
```bash
vscan -t example.com --ssl -p 443
```

#### 3. Custom Wordlist
```bash
vscan -t example.com -w ./wordlists/custom.txt
```

### Multi-Port Scanning (NEW)

#### 4. Scan Multiple Specific Ports
```bash
# Scan common HTTP/HTTPS ports
vscan -t example.com --ports 80,443,8080,8443
```

#### 5. Scan Port Range
```bash
# Scan all ports from 8000 to 8100
vscan -t example.com --ports 8000-8100
```

#### 6. Combination of Ports and Ranges
```bash
# Mix specific ports and ranges
vscan -t example.com --ports 80,443,8000-8010,9000
```

#### 7. Multi-Port with SSL
```bash
# Scan multiple HTTPS ports
vscan -t example.com --ssl --ports 443,8443,9443
```

#### 8. Multi-Port with Output
```bash
# Output automatically includes port in filename
vscan -t example.com --ports 80,443,8080 -oN results.txt
# Creates: results_port80.txt, results_port443.txt, results_port8080.txt
```

### Performance Examples

#### 9. High-Speed Concurrent Scan
```bash
# Scan with 50 concurrent requests
vscan -t example.com --concurrency 50 -v
```

#### 10. Rate-Limited Scan
```bash
# Add 2 second delay between requests
vscan -t example.com --rate-limit 2
```

#### 11. Traditional Sequential Scan
```bash
# Disable async for compatibility
vscan -t example.com --no-async
```

### Advanced Filtering

#### 12. Ignore Multiple HTTP Codes
```bash
vscan -t example.com --ignore-http-codes "404,403,500"
```

#### 13. Ignore Specific Content Length
```bash
# Ignore default/error pages with length 1234
vscan -t example.com --ignore-content-length 1234
```

#### 14. CTF Mode (First Hit)
```bash
# Stop on first successful match
vscan -t ctf-challenge.com --first-hit
```

### Network Configuration

#### 15. SSH Tunnel / Port Forwarding
```bash
# Connect via SSH tunnel on localhost:4444, but set Host header for port 80
vscan -t localhost -b example.com -p 4444 -r 80
```

#### 16. HTTP Proxy
```bash
vscan -t example.com --proxy http://127.0.0.1:8080
```

#### 17. SOCKS5 Proxy
```bash
vscan -t example.com --proxy socks5://127.0.0.1:1080
```

#### 18. Custom Timeout
```bash
# Set 30 second timeout for slow servers
vscan -t example.com --timeout 30
```

### Header Manipulation

#### 19. Custom User-Agent
```bash
vscan -t example.com --user-agent "MyCustomBot/1.0"
```

#### 20. Random User-Agent
```bash
vscan -t example.com --random-agent
```

#### 21. WAF Bypass Headers
```bash
# Add X-Forwarded-For and similar headers
vscan -t example.com --waf
```

### Wordlist Manipulation

#### 22. Prefix/Suffix
```bash
# Add 'dev-' prefix to all wordlist entries
vscan -t example.com --prefix "dev-"

# Add '.backup' suffix
vscan -t example.com --suffix ".backup"
```

### Output Formats

#### 23. Save Normal Output
```bash
vscan -t example.com -oN results.txt
```

#### 24. Save JSON Output
```bash
vscan -t example.com -oJ results.json
```

#### 25. Save Grepable Output
```bash
vscan -t example.com -oG results.grep
```

### Fuzzy Logic & DNS

#### 26. Fuzzy Logic Comparison
Here is an example with fuzzy logic enabled to compare page similarity:

```bash
vscan -t innopolis.ru --ssl -p 443 --fuzzy-logic -oN results.txt -w ./wordlists/subdomain.txt
```
```bash
[#] Found: city.innopolis.ru (code: 200, content-length: 3917, page-hash: 0ce4bddb024c57a661eda4c34d3ec58cb4a7a127723d9d31ced7dcc0653f9b24)
  Server: nginx
  Date: Mon, 08 Jul 2019 10:39:12 GMT
  Content-Type: text/html; charset=UTF-8
  Content-Length: 3917
  Connection: keep-alive
  P3P: policyref="/bitrix/p3p.xml", CP="NON DSP COR CUR ADM DEV PSA PSD OUR UNR BUS UNI COM NAV INT DEM STA"
  X-Powered-CMS: Bitrix Site Manager (6745f601c5dfcb58aedada9c44bc3da3)
  Set-Cookie: PHPSESSID=i3kgmvj30e87le4fqhu748da03; path=/; HttpOnly
  Expires: Thu, 19 Nov 1981 08:52:00 GMT
  Cache-Control: no-store, no-cache, must-revalidate
  Pragma: no-cache
  Content-Encoding: gzip

[#] Found: gorod.innopolis.ru (code: 200, content-length: 3918, page-hash: 551b5bf4834bd0d532854e94cb56bdd8f121437ac7b13fa25bd674dcab95e983)
  Server: nginx
  Date: Mon, 08 Jul 2019 10:40:46 GMT
  Content-Type: text/html; charset=UTF-8
  Content-Length: 3918
  Connection: keep-alive
  P3P: policyref="/bitrix/p3p.xml", CP="NON DSP COR CUR ADM DEV PSA PSD OUR UNR BUS UNI COM NAV INT DEM STA"
  X-Powered-CMS: Bitrix Site Manager (6745f601c5dfcb58aedada9c44bc3da3)
  Set-Cookie: PHPSESSID=271fp55oi3644irmu995652fu7; path=/; HttpOnly
  Expires: Thu, 19 Nov 1981 08:52:00 GMT
  Cache-Control: no-store, no-cache, must-revalidate
  Pragma: no-cache
  Content-Encoding: gzip

[#] Found: old.innopolis.ru (code: 200, content-length: None, page-hash: daf15744d99a3cd24b7de76bd0964aa1c1dd124e18c7ab5e9a6217df8a656ccf)
  Server: nginx
  Date: Mon, 08 Jul 2019 10:42:42 GMT
  Content-Type: text/html; charset=UTF-8
  Transfer-Encoding: chunked
  Connection: keep-alive
  P3P: policyref="/bitrix/p3p.xml", CP="NON DSP COR CUR ADM DEV PSA PSD OUR UNR BUS UNI COM NAV INT DEM STA"
  X-Powered-CMS: Bitrix Site Manager (c8da0d88c5c62f53243e84c166088c07)
  Set-Cookie: PHPSESSID=hnkrc06b82ccf4bu6oc1fphh13; path=/; HttpOnly
  Expires: Thu, 19 Nov 1981 08:52:00 GMT
  Cache-Control: no-store, no-cache, must-revalidate
  Pragma: no-cache
  Content-Encoding: gzip

[#] Found: welcome.innopolis.ru (code: 200, content-length: None, page-hash: fc5b9672efafa73986628f96ca5af352bf4d6b96b26e1f62635b00cea2f4004b)
  Server: nginx
  Date: Mon, 08 Jul 2019 10:47:19 GMT
  Content-Type: text/html; charset=UTF-8
  Transfer-Encoding: chunked
  Connection: keep-alive
  P3P: policyref="/bitrix/p3p.xml", CP="NON DSP COR CUR ADM DEV PSA PSD OUR UNR BUS UNI COM NAV INT DEM STA"
  X-Powered-CMS: Bitrix Site Manager (86900c0cc7337d8a8599e8d1ddde2920)
  Set-Cookie: PHPSESSID=hfpi4j8700bu3prd3uhvth8fv7; path=/; HttpOnly
  Expires: Thu, 19 Nov 1981 08:52:00 GMT
  Cache-Control: no-store, no-cache, must-revalidate
  Pragma: no-cache
  Content-Encoding: gzip


[+] Most likely matches with a unique count of 1 or less:
        [>] old.innopolis.ru
        [>] welcome.innopolis.ru
        [>] gorod.innopolis.ru
        [>] city.innopolis.ru
        [>] brand.innopolis.ru


[+] Match similarity using fuzzy logic:
        [>] old.innopolis.ru is 27% similar to welcome.innopolis.ru
        [>] old.innopolis.ru is 12% similar to gorod.innopolis.ru
        [>] old.innopolis.ru is 12% similar to city.innopolis.ru
        [>] old.innopolis.ru is 31% similar to brand.innopolis.ru
        [>] welcome.innopolis.ru is 11% similar to gorod.innopolis.ru
        [>] welcome.innopolis.ru is 11% similar to city.innopolis.ru
        [>] welcome.innopolis.ru is 18% similar to brand.innopolis.ru
        [>] gorod.innopolis.ru is 100% similar to city.innopolis.ru
        [>] gorod.innopolis.ru is 27% similar to brand.innopolis.ru
        [>] city.innopolis.ru is 27% similar to brand.innopolis.ru

[+] Output written to results.txt
```

#### 27. Disable DNS Lookups
```bash
# Skip reverse DNS lookups for faster scanning
vscan -t example.com --no-lookups
```

### Real-World Scenarios

#### 28. Comprehensive Pentest Scan
```bash
# Full-featured scan with all options
vscan -t target.com \
  --ssl \
  -p 443 \
  --concurrency 20 \
  --fuzzy-logic \
  --random-agent \
  --waf \
  --timeout 15 \
  -w ./wordlists/comprehensive.txt \
  -oN normal_output.txt \
  -oJ json_output.json \
  -v
```

#### 29. Stealth Scan
```bash
# Low and slow to avoid detection
vscan -t target.com \
  --rate-limit 5 \
  --concurrency 2 \
  --random-agent \
  --timeout 30 \
  -v
```

#### 30. Quick Discovery
```bash
# Fast scan with common subdomains
vscan -t target.com \
  --concurrency 100 \
  --first-hit \
  -w ./wordlists/top-1000.txt
```

#### 31. Multi-Port Comprehensive Scan (NEW)
```bash
# Scan multiple ports with full features
vscan -t target.com \
  --ports 80,443,8000-8100 \
  --ssl \
  --concurrency 25 \
  --fuzzy-logic \
  --random-agent \
  -oJ multiport_results.json \
  -v
```

---

## Performance Tips

1. **Async Mode**: Default async mode is 10x faster than traditional scanning
2. **Concurrency**: Adjust `--concurrency` based on your network and target capacity
   - Local testing: 50-100
   - Remote targets: 10-30 (respect rate limits)
3. **Wordlist Size**: Use targeted wordlists for faster results
4. **Rate Limiting**: Use `--rate-limit` to avoid overwhelming servers or triggering WAF
5. **First Hit Mode**: Enable `--first-hit` when you know there's no catch-all

---

## Troubleshooting

### Common Issues

#### 1. Connection Timeouts
```bash
# Increase timeout value
vscan -t example.com --timeout 30
```

#### 2. Too Many Requests / Rate Limiting
```bash
# Reduce concurrency and add rate limit
vscan -t example.com --concurrency 5 --rate-limit 2
```

#### 3. SSL Certificate Errors
SSL verification is disabled by default for security testing purposes. This is intentional.

#### 4. Import Errors
```bash
# Ensure all dependencies are installed
pip install -r requirements.txt --upgrade
```

#### 5. Slow Performance
```bash
# Ensure async mode is enabled (it's default)
vscan -t example.com --concurrency 50 -v
```

---

## Development

### Running Tests
```bash
# Install test dependencies
pip install -r test-requirements.txt

# Run tests
pytest

# Run with coverage
pytest --cov=vscan --cov-report=html
```

### Code Quality
```bash
# Format code
black vscan/

# Lint code
flake8 vscan/

# Type checking
mypy vscan/
```

---

## Security Considerations

⚠️ **Important**: This tool is designed for authorized security testing only.

- Always obtain proper authorization before scanning
- Respect rate limits and robots.txt
- Be aware of legal implications in your jurisdiction
- Use responsibly and ethically

### Ethical Use Cases
✅ Authorized penetration testing
✅ Bug bounty programs
✅ CTF competitions
✅ Security research on owned infrastructure
✅ Educational purposes in controlled environments

### Prohibited Use Cases
❌ Unauthorized scanning of third-party systems
❌ Malicious intent
❌ Violation of terms of service
❌ Any illegal activities

---

## What's New in v2.0

### Major Improvements
- ⚡ **Async/Concurrent Scanning**: 10x performance improvement
- 🎨 **Rich UI**: Beautiful progress bars and colored output with Rich library
- 🔧 **All Features Enabled**: Rate limiting, WAF bypass, JSON output now active
- 🐳 **Modern Docker**: Multi-stage builds with Python 3.11
- 📦 **Updated Dependencies**: All packages updated to latest secure versions
- 🛡️ **Better Error Handling**: Comprehensive logging and exception handling
- 🌐 **Proxy Support**: HTTP/HTTPS/SOCKS5 proxy support
- ⏱️ **Configurable Timeouts**: Fine-tune connection timeouts
- 📝 **Multiple Output Formats**: Normal, JSON, and grepable output

### Technical Improvements
- Replaced deprecated `pkg_resources` with `importlib.resources`
- Reduced cognitive complexity through code refactoring
- Added comprehensive logging throughout
- Modern Python 3.9+ features
- Type hints and better code documentation
- Updated test framework to pytest 8.x

---

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

### Development Setup
```bash
git clone https://github.com/your-repo/vscan.git
cd vscan
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install -r test-requirements.txt
```

### Contribution Guidelines
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add/update tests
5. Ensure all tests pass
6. Submit a pull request

---

## License

This project is licensed under the MIT License - see the LICENSE file for details.

---

## Credits

Original project by RP2
Enhanced Edition with modern features and improvements

---

## Support

For issues, questions, or contributions, please open an issue on GitHub.

**Happy Scanning! 🚀**
