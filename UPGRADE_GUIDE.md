# Upgrade Guide: v1.x to v2.0

This guide will help you upgrade from vscan v1.x to v2.0 and take advantage of the new features.

## Breaking Changes

### 1. Python Version Requirement

**Old**: Python 2.7 / 3.5+
**New**: Python 3.9+

```bash
# Check your Python version
python --version

# If you need to upgrade
# Ubuntu/Debian
sudo apt update
sudo apt install python3.9

# macOS (using Homebrew)
brew install python@3.9
```

### 2. Dependency Changes

All dependencies have been updated to modern versions. You must reinstall:

```bash
# Uninstall old version
pip uninstall vscan

# Install new version
cd vscan
pip install -r requirements.txt
python setup.py install
```

### 3. Docker Base Image

If you're using Docker, rebuild your images:

```bash
# Remove old image
docker rmi vscan

# Build new image
docker build -t vscan .
```

## New Features & How to Use Them

### 1. Async Scanning (MAJOR PERFORMANCE BOOST)

Async scanning is now **enabled by default**, providing up to 10x performance improvement.

```bash
# Old way (still works with --no-async)
vscan -t example.com

# New way (default, much faster)
vscan -t example.com --concurrency 20

# Disable async if needed
vscan -t example.com --no-async
```

**Performance Comparison**:
- Old: ~100 hosts/minute
- New: ~1000+ hosts/minute (with concurrency 10)

### 2. Beautiful Progress Bars

Progress tracking is now automatic with rich UI:

```bash
# Just run normally, progress bar appears automatically
vscan -t example.com -w large-wordlist.txt
```

Output now includes:
- Real-time progress bar
- Elapsed time
- Percentage complete
- Colored output

### 3. Previously Hidden Features Now Available

#### Rate Limiting
```bash
# Was commented out in v1.x
# Now available:
vscan -t example.com --rate-limit 2
```

#### WAF Bypass Headers
```bash
# Was commented out in v1.x
# Now available:
vscan -t example.com --waf
```

#### First Hit Mode
```bash
# Was commented out in v1.x
# Now available:
vscan -t example.com --first-hit
```

#### JSON Output
```bash
# Was commented out in v1.x
# Now available:
vscan -t example.com -oJ output.json
```

### 4. Proxy Support

New feature in v2.0:

```bash
# HTTP proxy
vscan -t example.com --proxy http://127.0.0.1:8080

# SOCKS5 proxy
vscan -t example.com --proxy socks5://127.0.0.1:1080
```

### 5. Configurable Timeout

```bash
# Default is now 10 seconds, but configurable
vscan -t example.com --timeout 30
```

### 6. Concurrency Control

```bash
# Control how many concurrent requests
vscan -t example.com --concurrency 50
```

## Command Migration Examples

### Example 1: Basic Scan

**Old v1.x**:
```bash
vscan -t example.com -w wordlist.txt -v
```

**New v2.0** (same command works, but faster):
```bash
vscan -t example.com -w wordlist.txt -v
# Now runs with async by default!
```

### Example 2: HTTPS Scan with Fuzzy Logic

**Old v1.x**:
```bash
vscan -t example.com --ssl -p 443 --fuzzy-logic -oN output.txt
```

**New v2.0** (enhanced with progress):
```bash
vscan -t example.com --ssl -p 443 --fuzzy-logic -oN output.txt
# Now includes progress bar and faster performance
```

### Example 3: High-Performance Scan

**Old v1.x** (no concurrency option):
```bash
vscan -t example.com -w large-wordlist.txt
# Would take hours
```

**New v2.0** (with concurrency):
```bash
vscan -t example.com -w large-wordlist.txt --concurrency 50
# Now takes minutes!
```

### Example 4: Through Proxy (NEW)

**Old v1.x** (not possible):
```bash
# Not supported
```

**New v2.0**:
```bash
vscan -t example.com --proxy http://127.0.0.1:8080
```

## Troubleshooting Upgrade Issues

### Issue 1: Import Errors

**Problem**: `ModuleNotFoundError` or import errors

**Solution**:
```bash
# Reinstall all dependencies
pip install -r requirements.txt --upgrade
pip install -e .
```

### Issue 2: NumPy Build Errors

**Problem**: Error building numpy wheels

**Solution**:
```bash
# Install pre-built binaries
pip install --upgrade pip
pip install numpy --only-binary :all:
pip install -r requirements.txt
```

### Issue 3: Slower Performance After Upgrade

**Problem**: Scans seem slower than before

**Solution**: Check if async is disabled
```bash
# Ensure async is enabled (default)
vscan -t example.com -v

# Check output - should show progress bar
# If not, you may have --no-async flag set
```

### Issue 4: Docker Build Fails

**Problem**: Docker build fails with old instructions

**Solution**:
```bash
# Use new Dockerfile
docker build -t vscan .

# If build fails, try with no cache
docker build --no-cache -t vscan .
```

### Issue 5: SSL/TLS Warnings

**Problem**: Warnings about SSL verification

**Solution**: This is intentional for security testing. SSL verification is disabled to test hosts with self-signed certificates. This is documented behavior.

## Configuration Changes

### Wordlist Files

Wordlist files location remains the same:
```
vscan/wordlists/
```

But you can now use multiple wordlists:
```bash
vscan -t example.com -w "wordlist1.txt,wordlist2.txt"
```

### User Agents

Random user agents are still supported:
```bash
vscan -t example.com --random-agent
```

User agent list location:
```
vscan/lib/ua-random-list.txt
```

## Performance Tuning for v2.0

### For Local Testing
```bash
vscan -t localhost --concurrency 100 --timeout 5
```

### For Remote Targets
```bash
vscan -t example.com --concurrency 20 --timeout 15 --rate-limit 1
```

### For Stealth Scanning
```bash
vscan -t example.com --concurrency 2 --rate-limit 5 --random-agent
```

### For Maximum Speed
```bash
vscan -t example.com --concurrency 100 --timeout 5 -w top-1000.txt
```

## New Output Formats

### JSON Output (NEW)
```bash
vscan -t example.com -oJ output.json

# Example JSON structure:
{
  "Your Target": "example.com",
  "Your Port": 80,
  "SSL": false,
  "Start Time": "20/05/2026 14:30:45",
  "Result": {
    "dev.example.com": {
      "Code": 200,
      "Hash": "abc123...",
      "Headers": {
        "Server": "nginx",
        "Content-Type": "text/html"
      }
    }
  }
}
```

### Grepable Output (NEW)
```bash
vscan -t example.com -oG output.grep

# Format: hostname\tstatus_code\thash
dev.example.com	200	abc123...
staging.example.com	200	def456...
```

## Best Practices for v2.0

1. **Use async mode** (default) for better performance
2. **Adjust concurrency** based on target and network
3. **Enable verbose mode** (`-v`) for troubleshooting
4. **Use JSON output** for parsing results programmatically
5. **Use rate limiting** to be respectful and avoid detection
6. **Use proxy** when testing through corporate networks
7. **Use timeouts** appropriate for your network conditions

## Reverting to Old Behavior

If you need the old synchronous behavior:

```bash
vscan -t example.com --no-async
```

However, we recommend embracing the new async features for better performance.

## Getting Help

If you encounter issues during upgrade:

1. Check this guide first
2. Review the [README.md](README.md) for new features
3. Check [CHANGELOG.md](CHANGELOG.md) for detailed changes
4. Open an issue on GitHub with:
   - Your Python version
   - Full error message
   - Command you're trying to run
   - Output of `pip list | grep -E "(vscan|requests|numpy|pandas)"`

## Summary of Benefits

✅ **10x faster** scanning with async
✅ **Better UX** with progress bars and colors
✅ **More features** (proxy, timeout, rate limiting)
✅ **Secure dependencies** (all CVEs patched)
✅ **Modern codebase** (Python 3.9+, type hints)
✅ **Better error handling** (comprehensive logging)
✅ **Multiple output formats** (JSON, grepable)
✅ **Docker improvements** (multi-stage, smaller image)

---

**Happy Upgrading! 🚀**

For questions or issues, please open a GitHub issue.
