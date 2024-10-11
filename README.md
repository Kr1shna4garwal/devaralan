[![Twitter](https://img.shields.io/twitter/follow/kr1shna4garwal?logo=twitter)](https://twitter.com/kr1shna4garwal)
![stars](https://img.shields.io/github/stars/kr1shna4garwal/devaralan)
[![issues](https://img.shields.io/github/issues/kr1shna4garwal/devaralan?color=%20%237fb3d5%20)](https://github.com/devaralan/devaralan/issues)


<h1 align="center">Devalaran</h1>
<h3 align="center">Devaralan is a root domain permutation tool that generates root domain variations by adding prefixes and suffixes using predefined keywords.</h3>
<p align="center"><img src=https://i.ibb.co/VgctZZY/Screenshot-2024-10-11-at-3-43-42-PM.png></p>

# Tree
- [Summary](#Summary)
- [System Requirements](#System%20Requirements)
- [Seed](#Seed)
- [Installation](#installation)
- [Usage](#usage)
- [Examples](#examples)
- [Troubleshooting & Common Issues](#Troubleshooting & Common Issues)
- [Contributing](#Contributing)
- [Author](#author)
- [Warning](#warning)
- [License](#license)

# Summary

**Devaralan** is an advanced root domain permutation generator and DNS resolver tool built in Python, I created this for my personal bug bounty activities. This tool helps you automate the generation of root domain permutations (example: apple-internal[.]com) and then check if they resolve to valid IPs.
It generates domains based on a combination of known keywords (you can add your keywords too) and existing subdomains.
The tool can also perform DNS resolution, HTTP status code checks, and WHOIS lookups, giving you detailed information about the discovered subdomains.

# System Requirements
- Python 3.10 or later
- Internet connection for DNS resolution and HTTP requests
- Compatible on Linux, macOS, and Windows systems

# Seed
> To run this tool, you'll need to save your target's root domains in a text file OR you can seed your single domain via --domain/-d flag.

Example (domains.lst) :

```
apple[.]com
google[.]com
meta[.]com
```

# Installation

**NOTE**: Please make sure python3 and pip3 is installed in your system

- Docker
    - installation
        ```bash
        git clone https://github.com/kr1shna4garwal/devaralan
        cd devaralan
        docker build -t devaralan .
        ```

- Linux
    - from releases
    - Direct run
        ```bash
        git clone https://github.com/kr1shna4garwal/devaralan
        cd devaralan
        pip3.11 install -r requirements.txt
        python3.11 src/devaralan.py --help
        ```
    - installation
        ```bash
        git clone https://github.com/kr1shna4garwal/devaralan
        cd devaralan
        python3.11 setup.py install
        ```

# Usage

```
 Usage: devaralan [OPTIONS]                                                                                                                                   
                                                                                                                                                              
╭─ Options ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --domain              -d       TEXT     Domain(s) to enumerate subdomains for. [default: None]                                                             │
│ --file                -f       TEXT     File containing list of domains. [default: None]                                                                   │
│ --output              -o       TEXT     Output file to save results. [default: None]                                                                       │
│ --output-format       -of      TEXT     Output format: json, csv, or txt (default: json) [default: json]                                                   │
│ --concurrent          -c       INTEGER  Number of concurrent threads (default: 10) [default: 10]                                                           │
│ --ignore-ssl          -k                Ignore SSL errors.                                                                                                 │
│ --random-agent        -ru               Use random User-Agent header for each request.                                                                     │
│ --timeout                      INTEGER  Request timeout in seconds (default: 10) [default: 10]                                                             │
│ --retries                      INTEGER  Number of retries for failed requests (default: 2) [default: 2]                                                    │
│ --verbose             -v                Verbose output.                                                                                                    │
│ --debug                                 Debug mode, show every request and response.                                                                       │
│ --proxy               -p       TEXT     Proxy server to use (e.g., http://127.0.0.1:8080). [default: None]                                                 │
│ --install-completion                    Install completion for the current shell.                                                                          │
│ --show-completion                       Show completion for the current shell, to copy it or customize the installation.                                   │
│ --help                                  Show this message and exit.                                                                                        │
╰────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯

```

# Examples

#### Running with a single root domain

```bash
devaralan --domain example[.]com
```

#### Running with a single root domain with verbose mode

```bash
devaralan --domain example[.]com --verbose
```

#### Running with a single root domain with verbose mode + output (json) + random user agent

```bash
devaralan --domain example[.]com --verbose --output-format json --output example-output.json --random-agent
```

#### Running with a single root domain with debug mode

```bash
devaralan --domain example[.]com --debug
```

#### Running with a text file containing line separated domains

```bash
devaralan --list domains.lst
```

#### Running with a text file containing line separated domains with verbose mode

```bash
devaralan --list domains.lst --verbose
```

# Troubleshooting & Common Issues

DNS Resolution Failing:
- Ensure you have internet access.
- Try using a different set of resolvers by specifying a custom resolver file with -r.

Whois Errors:
- Some domains may block WHOIS lookups or return incomplete data. You may encounter errors depending on the registrar's restrictions.

Tool Interruptions:
- If the process is interrupted, you can resume by rerunning with the same options or manually modifying your input list.

# Contributing
Contributions are welcome! To contribute:

```
Fork the repository.
Create a new branch (git checkout -b feature-branch).
Make your changes and test thoroughly.
Submit a pull request detailing your changes.
```

# Author
- Krishna Agarwal (kr1shna4garwal@proton.me)

# Warning 

IMPORTANT: Use this tool responsibly and only on domains you have explicit permission to test. Unauthorized use against domains without consent could be illegal and result in severe consequences. Follow the laws of your jurisdiction and adhere to ethical hacking guidelines.

# License
This project is licensed under the GPL-3.0 License. See the LICENSE file for details.
