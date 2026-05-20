"""Async Virtual Host Scanner for improved performance"""
import asyncio
import hashlib
import random
import ssl
from typing import List, Optional

import aiohttp
from .discovered_host import discovered_host

DEFAULT_USER_AGENT = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) '\
                     'AppleWebKit/537.36 (KHTML, like Gecko) '\
                     'Chrome/120.0.0.0 Safari/537.36'


class async_virtual_host_scanner:
    """Async virtual host scanner for concurrent scanning

    Attributes:
        wordlist: list of hostnames to scan
        target: the target server address
        port: the port to scan
        ssl: whether to use HTTPS
        concurrency: number of concurrent requests
        timeout: request timeout in seconds
    """

    def __init__(self, target, wordlist, **kwargs):
        self.target = target
        self.wordlist = wordlist
        self.base_host = kwargs.get('base_host')
        self.rate_limit = int(kwargs.get('rate_limit', 0))
        self.port = int(kwargs.get('port', 80))
        self.real_port = int(kwargs.get('real_port', 80))
        self.ssl = kwargs.get('ssl', False)
        self.fuzzy_logic = kwargs.get('fuzzy_logic', False)
        self.unique_depth = int(kwargs.get('unique_depth', 1))
        self.ignore_http_codes = kwargs.get('ignore_http_codes', '404')
        self.first_hit = kwargs.get('first_hit', False)
        self.verbose = kwargs.get('verbose', False)
        self.concurrency = int(kwargs.get('concurrency', 10))
        self.timeout = int(kwargs.get('timeout', 10))
        self.proxy = kwargs.get('proxy')
        self.add_waf_bypass_headers = kwargs.get('add_waf_bypass_headers', False)

        self.ignore_content_length = int(
            kwargs.get('ignore_content_length', 0)
        )

        self.completed_scan = False
        self.results = []
        self.hosts = []

        self.user_agents = list(kwargs.get('user_agents', [])) \
            or [DEFAULT_USER_AGENT]

        self.progress_callback = kwargs.get('progress_callback')
        self.scanned_count = 0

    @property
    def ignore_http_codes(self):
        return self._ignore_http_codes

    @ignore_http_codes.setter
    def ignore_http_codes(self, codes):
        if isinstance(codes, str):
            self._ignore_http_codes = [
                int(code) for code in codes.replace(' ', '').split(',')
            ]
        else:
            self._ignore_http_codes = codes

    async def scan_host(self, session: aiohttp.ClientSession,
                       hostname: str, semaphore: asyncio.Semaphore) -> Optional[discovered_host]:
        """Scan a single virtual host"""
        async with semaphore:
            try:
                if self.verbose:
                    print(f"[*] Scanning {hostname}")

                if self.real_port == 80:
                    host_header = hostname
                else:
                    host_header = f'{hostname}:{self.real_port}'

                headers = {
                    'User-Agent': random.choice(self.user_agents),
                    'Host': host_header,
                    'Accept': '*/*'
                }

                if self.add_waf_bypass_headers:
                    headers.update({
                        'X-Originating-IP': '127.0.0.1',
                        'X-Forwarded-For': '127.0.0.1',
                        'X-Remote-IP': '127.0.0.1',
                        'X-Remote-Addr': '127.0.0.1'
                    })

                dest_url = f"{'https' if self.ssl else 'http'}://{self.target}:{self.port}/"

                timeout = aiohttp.ClientTimeout(total=self.timeout)

                async with session.get(
                    dest_url,
                    headers=headers,
                    timeout=timeout,
                    ssl=False
                ) as response:

                    if response.status in self.ignore_http_codes:
                        return None

                    content_length = int(response.headers.get('content-length', 0))
                    if self.ignore_content_length and \
                       self.ignore_content_length == content_length:
                        return None

                    text = await response.text()
                    page_hash = hashlib.sha256(text.encode('utf-8')).hexdigest()

                    host = discovered_host()
                    host.hostname = hostname
                    host.response_code = response.status
                    host.hash = page_hash
                    host.content = text.encode('utf-8')

                    output = f'[#] Found: {hostname} (code: {response.status}, ' \
                            f'content-length: {content_length}, page-hash: {page_hash})\n'

                    for key, val in response.headers.items():
                        output += f'  {key}: {val}\n'
                        host.keys.append(f'{key}: {val}')

                    print(output)

                    self.results.append(f'{hostname},{page_hash}')

                    if self.rate_limit > 0:
                        await asyncio.sleep(self.rate_limit)

                    return host

            except asyncio.TimeoutError:
                if self.verbose:
                    print(f"[!] Timeout scanning {hostname}")
            except aiohttp.ClientError as e:
                if self.verbose:
                    print(f"[!] Error scanning {hostname}: {e}")
            except Exception as e:
                if self.verbose:
                    print(f"[!] Unexpected error scanning {hostname}: {e}")
            finally:
                self.scanned_count += 1
                if self.progress_callback:
                    self.progress_callback(self.scanned_count, len(self.wordlist))

            return None

    async def scan(self):
        """Perform async scan of all hosts in wordlist"""
        if not self.base_host:
            self.base_host = self.target

        if not self.real_port:
            self.real_port = self.port

        # Prepare wordlist with substitutions
        prepared_wordlist = [
            word.replace('%s', self.base_host) for word in self.wordlist
        ]

        # Create SSL context that doesn't verify certificates
        ssl_context = ssl.create_default_context()
        ssl_context.check_hostname = False
        ssl_context.verify_mode = ssl.CERT_NONE

        # Configure connector
        connector = aiohttp.TCPConnector(
            ssl=ssl_context,
            limit=self.concurrency,
            limit_per_host=self.concurrency
        )

        timeout = aiohttp.ClientTimeout(total=self.timeout)

        async with aiohttp.ClientSession(
            connector=connector,
            timeout=timeout
        ) as session:
            semaphore = asyncio.Semaphore(self.concurrency)

            tasks = [
                self.scan_host(session, hostname, semaphore)
                for hostname in prepared_wordlist
            ]

            results = await asyncio.gather(*tasks, return_exceptions=True)

            # Filter out None results and exceptions
            self.hosts = [
                host for host in results
                if host is not None and isinstance(host, discovered_host)
            ]

            if self.first_hit and len(self.hosts) >= 1:
                self.hosts = self.hosts[:1]

        self.completed_scan = True
        return self.hosts

    def likely_matches(self):
        """Get likely matches based on unique depth"""
        if not self.completed_scan:
            print("[!] Likely matches cannot be printed as scan has not completed.")
            return []

        import pandas as pd

        segmented_data = {}
        for item in self.results:
            parts = item.split(",")
            if len(parts) == 2:
                segmented_data[parts[0]] = parts[1]

        if not segmented_data:
            return []

        dataframe = pd.DataFrame([
            [key, value] for key, value in segmented_data.items()],
            columns=["key_col", "val_col"]
        )

        filtered = dataframe.groupby("val_col").filter(
            lambda x: len(x) <= self.unique_depth
        )

        return filtered["key_col"].values.tolist()
