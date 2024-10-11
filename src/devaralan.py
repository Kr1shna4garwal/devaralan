#!/usr/bin/env python3.11

# > Name: Devaralan
# > Version: 1.0
# > Url: https://github.com/kr1shna4garwal/devaralan

import typer
import asyncio
import aiohttp
import dns.resolver
import logging
from typing import List, Optional
from dataclasses import dataclass, asdict
from colorama import Fore, Style, init
import json
import csv
from fake_useragent import UserAgent


init(autoreset=True)

app = typer.Typer()

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

BANN = r"""
    ━━━━━━━━━━━━━━━━━━━━━
    /       Hey!,       \
    \/   I`m Devaralan   /
    ━━━━━━━━━━━━━━━━━━━━━
          \
        ¯\/_(ツ)_/¯

[+] github.com/kr1shna4garwal/devaralan

"""

# You can add your keywords here ->
KEYWORDS = [
    "test", "us", "uk", "design", "ca", "in", "stage", "backup", "confidential", "admin",
    "management", "db", "database", "router", "api", "service", "web", "app", "portal",
    "monitoring", "analytics", "security", "config", "log", "audit", "sandbox", "prd",
    "finance", "hr", "marketing", "inventory", "warehouse", "tools", "infra", "network",
    "k8", "prod", "dev", "saml", "sso", "secret", "kibana", "grafana", "jira", "cloud",
    "internal", "employee", "cicd", "jenkins", "github", "gitlab", "git", "localhost",
    "qa", "backend", "kube", "testing", "staging", "vpn", "firewall", "proxy", "auth",
    "login", "signup", "admin_panel", "console", "root", "sysadmin", "ssh", "ftp", "smtp",
    "dns", "mail", "mx", "support", "bug", "report", "logger", "metric", "alert", "watch",
    "scanner", "discover", "audit", "compliance", "pentest", "redteam", "blueteam", 
    "exploit", "reverseproxy", "forwardproxy", "vulnerable", "leak", "exposed", "hack", 
    "breach", "incident", "forensic", "dr", "businesscontinuity", "backup", "restore", 
    "archive", "repository", "collaboration", "team", "enterprise", "corp", "organization", 
    "ngo", "edu", "school", "library", "public", "private", "community", "global"
]

@dataclass
class ResolveResult:
    domain: str
    ip: Optional[str]
    http_status: Optional[int]
    cname: Optional[str]

class Devaralan:
    def __init__(self, domains, output_file, output_format, threads, ignore_ssl, random_agent, timeout, retries, verbose, debug, proxy):
        self.domains = domains
        self.output_file = output_file
        self.output_format = output_format
        self.threads = threads
        self.ignore_ssl = ignore_ssl
        self.random_agent = random_agent
        self.timeout = timeout
        self.retries = retries
        self.verbose = verbose
        self.debug = debug
        self.proxy = proxy
        self.results = []

        if self.debug:
            logger.setLevel(logging.DEBUG)
        elif self.verbose:
            logger.setLevel(logging.INFO)
        else:
            logger.setLevel(logging.WARNING)

    def generate_permutations(self, domain: str) -> List[str]:
        permutations = []
        domain_parts = domain.split('.')
        for keyword in KEYWORDS:
            for i in range(len(domain_parts) - 1):
                new_domain_suffix = '.'.join(domain_parts[:i + 1]) + '-' + keyword + '.' + '.'.join(domain_parts[i + 1:])
                permutations.append(new_domain_suffix)
                new_domain_prefix = keyword + '-' + '.'.join(domain_parts)
                permutations.append(new_domain_prefix)
        return list(set(permutations))

    async def resolve_domain(self, domain: str) -> ResolveResult:
        try:
            resolver = dns.resolver.Resolver()
            answers = resolver.resolve(domain, 'A')
            ip = answers[0].to_text()
            
            http_status = await self.check_http_status(domain)
            cname = await self.get_cname(domain)
            
            logger.info(f"{Fore.GREEN}[+] Resolved: {domain} -> {ip}")
            return ResolveResult(domain, ip, http_status, cname)
        except Exception as e:
            logger.debug(f"Error resolving {domain}: {str(e)}")
            return ResolveResult(domain, None, None, None)

    async def check_http_status(self, domain: str) -> Optional[int]:
        url = f"http://{domain}"
        headers = {}
        if self.random_agent:
            headers["User-Agent"] = UserAgent().random

        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url, headers=headers, ssl=not self.ignore_ssl, timeout=self.timeout) as response:
                    return response.status
        except Exception as e:
            logger.debug(f"Error checking HTTP status for {domain}: {str(e)}")
            return None

    async def get_cname(self, domain: str) -> Optional[str]:
        try:
            resolver = dns.resolver.Resolver()
            answers = resolver.resolve(domain, 'CNAME')
            return answers[0].to_text()
        except Exception:
            return None

    async def process_domain(self, domain: str):
        permutations = self.generate_permutations(domain)
        tasks = [self.resolve_domain(perm) for perm in permutations]
        results = await asyncio.gather(*tasks)
        self.results.extend([result for result in results if result.ip])

    async def run(self):
        tasks = [self.process_domain(domain) for domain in self.domains]
        await asyncio.gather(*tasks)

    def save_results(self):
        if self.output_file:
            if self.output_format == 'json':
                with open(self.output_file, 'w') as f:
                    json.dump([asdict(result) for result in self.results], f, indent=2)
            elif self.output_format == 'csv':
                with open(self.output_file, 'w', newline='') as f:
                    writer = csv.DictWriter(f, fieldnames=asdict(self.results[0]).keys() if self.results else [])
                    writer.writeheader()
                    for result in self.results:
                        writer.writerow(asdict(result))
            else:  # plain text
                with open(self.output_file, 'w') as f:
                    for result in self.results:
                        f.write(f"Domain: {result.domain}, IP: {result.ip}, HTTP Status: {result.http_status}, CNAME: {result.cname}\n")
            logger.info(f"Results saved to {self.output_file}")

    def print_summary(self):
        print(f"\n{Fore.CYAN}Enumeration Summary:{Style.RESET_ALL}")
        print(f"Total domains processed: {len(self.domains)}")
        print(f"Total subdomains found: {len(self.results)}")
        if self.results:
            print(f"\n{Fore.GREEN}Top 5 resolved subdomains:{Style.RESET_ALL}")
            for result in sorted(self.results, key=lambda x: x.domain)[:5]:
                print(f"Domain: {result.domain}, IP: {result.ip}, HTTP Status: {result.http_status}")

@app.command()
def main(
    domain: Optional[List[str]] = typer.Option(None, "--domain", "-d", help="Domain(s) to enumerate subdomains for."),
    file: str = typer.Option(None, "--file", "-f", help="File containing list of domains."),
    output_file: str = typer.Option(None, "--output", "-o", help="Output file to save results."),
    output_format: str = typer.Option("json", "--output-format", "-of", help="Output format: json, csv, or txt (default: json)"),
    threads: int = typer.Option(10, "--concurrent", "-c", help="Number of concurrent threads (default: 10)"),
    ignore_ssl: bool = typer.Option(False, "--ignore-ssl", "-k", help="Ignore SSL errors."),
    random_agent: bool = typer.Option(False, "--random-agent", "-ru", help="Use random User-Agent header for each request."),
    timeout: int = typer.Option(10, "--timeout", "-t", help="Request timeout in seconds (default: 10)"),
    retries: int = typer.Option(2, "--retries", "-r", help="Number of retries for failed requests (default: 2)"),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Verbose output."),
    debug: bool = typer.Option(False, "--debug", help="Debug mode, show every request and response."),
    proxy: str = typer.Option(None, "--proxy", "-p", help="Proxy server to use (e.g., http://127.0.0.1:8080).")
):
    print(Fore.CYAN + BANN + Style.RESET_ALL)


    if domain is None:
        domains = []

    if domain:
        domains.extend(domain)
    if file:
        try:
            with open(file, 'r') as f:
                domains.extend(f.read().splitlines())
        except FileNotFoundError:
            logger.error(f"Domain file not found: {file}")
            raise typer.Exit(code=1)

    if not domains:
        logger.error("No domains provided. Use --domain or --file option.")
        raise typer.Exit(code=1)

    devaralan = Devaralan(domains, output_file, output_format, threads, ignore_ssl, random_agent, timeout, retries, verbose, debug, proxy)
    
    try:
        print(f"{Fore.YELLOW}Starting subdomain enumeration and resolution...{Style.RESET_ALL}")
        asyncio.run(devaralan.run())
        devaralan.save_results()
        devaralan.print_summary()
    except KeyboardInterrupt:
        print(f"\n{Fore.RED}Process interrupted by user. Saving partial results...{Style.RESET_ALL}")
        devaralan.save_results()
        devaralan.print_summary()
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}")
        raise typer.Exit(code=1)

if __name__ == "__main__":
    app()
