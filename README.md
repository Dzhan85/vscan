# Virtual Host Scan


## Feature

* Works over HTTP and HTTPS
* Ability to set the real port of the webserver
* Identify new targets by using reverse lookups and append to wordlist

## Comparisons between applications in search of virtual hosts:


 

# Install Requirements

## Running on VM 



The setup.py file needs setuptools. Some Python packages used to use distutils for distribution, but most now use setuptools, a more complete package. Here is a question about the differences between them.


Install these dependecies:

To install setuptools on Debian:
```bash
sudo apt-get install python-setuptools
```
For Python 3.x:
```bash
sudo apt-get install python3-setuptools
```




Install requirements packages for python:

```bash
pip install -r test-requirements.txt
```

Run script to compile application:

```bash
$ python3 setup.py install 

or 

$ python setup.py install

```

Dependencies will then be installed and 'vscan' will be added to your path. If there is an issue regarding
running `python3 setup.py build_ext`, you will need to reinstall `numpy` using `pip uninstall numpy` and `pip install numpy==1.12.0`. This should resolve the issue as there are sometimes issues with numpy being installed through setup.py.


## Running in container

Run Dockerfile in command line:

```bash
$ docker build -t vscan .
```

Enter to bash in container:

```bash
$ docker run -it vscan /bin/bash
```

Inside you can go to directory which was specified in Dockerfile:


Send commands to docker container, we have already specified entrypoint to command 'vscan':

```bash
$ docker 
```



# Usage

| Argument        | Description |
| ------------- |:-------------|
| -t TARGET_HOSTS | Set the target host. |
| -w WORDLISTS | Set the wordlist(s) to use. You may specify multiple wordlists in comma delimited format (e.g. -w "./wordlists/simple.txt, ./wordlists/hackthebox.txt" (default ./wordlists/virtual-host-scanning.txt). |
| -p PORT  | Set the port to use (default 80). |
| --ignore-http-codes IGNORE_HTTP_CODES | Comma separated list of http codes to ignore with virtual host scans (default 404). |
| --ignore-content-length IGNORE_CONTENT_LENGTH | Ignore content lengths of specificed amount. |
| --ssl | If set then connections will be made over HTTPS instead of HTTP. |
| --fuzzy-logic | If set then all unique content replies are compared and a similarity ratio is given for each pair. This helps to isolate vhosts in situations where a default page isn't static (such as having the time on it). |
| --no-lookups | Disbale reverse lookups (identifies new targets and append to wordlist, on by default). | 
| --random-agent | If set, each scan will use a random user-agent from a predefined list. |
| --user-agent | Specify a user agent to use for scans. |
| -oN OUTPUT_NORMAL | Normal output printed to a file when the -oN option is specified with a filename argument. |
| -v VERBOSE | Increase the output of the tool to show progress |



###  Running on http port

The most straightforward example runs the default wordlist against example.com using the default of port 80:

```bash
$ vscan -t example.com
```

### Running on https(SSL)
If your connection requires SSL, you can use:

```bash
$ vscan -t example.com --ssl
```


### Port forwarding
Say you have an SSH port forward listening on port 4444 fowarding traffic to port 80 on example.com's development machine. You could use the following to make VHostScan connect through your SSH tunnel via localhost:4444 but format the header requests to suit connecting straight to port 80:

```bash
$ vscan -t localhost -b example.com -p 4444 -r 80
```


### Scan with wordList
You can still specify a wordlist to use along with stdin. In these cases wordlist information will be appended to stdin. For example:

```bash
$  vscan -t localhost -w ./wordlists/wordlist.txt
```
### Fuzzy Logic
Here is an example with fuzzy logic enabled. You can see the last comparison is much more similar than the first two (it is comparing the content not the actual hashes):

```python
vscan -t innopolis.ru --ssl -p 443 --fuzzy-logic -oN https_sub4.txt -w vscan/wordlists/subdomain3.txt
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

[+] Writing normal ouptut to https_sub4.txt

```


