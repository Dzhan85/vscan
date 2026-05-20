#!/usr/bin/env python3

import sys
import asyncio
import dns.resolver
from argparse import ArgumentParser
from socket import gethostbyaddr
from importlib.resources import files
from .lib.core.virtual_host_scanner import virtual_host_scanner
from .lib.core.async_scanner import async_virtual_host_scanner
from .lib.helpers.output_helper import output_helper
from .lib.helpers.file_helper import load_random_user_agents
from .lib.helpers.wordlist_helper import WordList
from .lib.helpers.port_helper import parse_ports, format_port_list, get_common_ports
from .lib.core.__version__ import __version__
from .lib.input import cli_argument_parser
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn, TimeElapsedColumn
from rich.panel import Panel
from rich import print as rprint
from rich.table import Table

try:
    # Python 3.9+
    DEFAULT_WORDLIST_FILE = str(files('vscan').joinpath('wordlists/virtual-host-wordlist_updated.txt'))
except (TypeError, AttributeError):
    # Fallback for older Python versions
    import pkg_resources
    DEFAULT_WORDLIST_FILE = pkg_resources.resource_filename(
        'vscan', 'wordlists/virtual-host-wordlist_updated.txt'
    )


def print_banner():
    console = Console()
    banner = """
[bold cyan]╔═══════════════════════════════════════╗
║      Virtual Host Scanner v2.0        ║
║         Enhanced Edition              ║
╚═══════════════════════════════════════╝[/bold cyan]
    """
    console.print(banner)


def perform_dns_lookup(target, wordlist, verbose=False):
    """Perform DNS lookup and add results to wordlist"""
    try:
        console = Console()
        console.print("[cyan][+] Resolving DNS for additional wordlist entries[/cyan]")
        for ip in dns.resolver.resolve(target, 'A'):
            host, aliases, _ = gethostbyaddr(str(ip))
            wordlist.append(str(ip))
            wordlist.append(host)
            wordlist.extend(aliases)
            if verbose:
                console.print(f"[yellow][!] Discovered {host}/{ip}. Adding...[/yellow]")
    except dns.resolver.NXDOMAIN:
        console.print("[red][!] Couldn't find any records (NXDOMAIN)[/red]")
    except dns.resolver.NoAnswer:
        console.print("[red][!] Couldn't find any records (NoAnswer)[/red]")
    except Exception as e:
        console.print(f"[red][!] DNS lookup error: {e}[/red]")

    return wordlist


def setup_user_agents(arguments):
    """Setup user agents based on arguments"""
    console = Console()
    user_agents = []

    if arguments.user_agent:
        console.print('[cyan][>] User-Agent specified, using it.[/cyan]')
        user_agents = [arguments.user_agent]
    elif arguments.random_agent:
        console.print('[cyan][>] Random User-Agent flag set.[/cyan]')
        user_agents = load_random_user_agents()

    return user_agents


async def scan_single_port(port, arguments, wordlist, user_agents, console):
    """Scan a single port and return results"""
    scanner_args = vars(arguments).copy()
    scanner_args.update({
        'target': arguments.target_hosts,
        'port': port,
        'wordlist': wordlist,
        'user_agents': user_agents
    })

    # Use async scanner if enabled
    if getattr(arguments, 'async_scan', True):
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
            TimeElapsedColumn(),
            console=console
        ) as progress:
            task = progress.add_task(
                f"[cyan]Scanning port {port}...",
                total=len(wordlist)
            )

            def update_progress(current, total):
                progress.update(task, completed=current)

            scanner_args['progress_callback'] = update_progress
            scanner = async_virtual_host_scanner(**scanner_args)
            await scanner.scan()
    else:
        console.print(f"\n[cyan]Scanning port {port}...[/cyan]")
        scanner = virtual_host_scanner(**scanner_args)
        scanner.scan()

    return scanner


def display_scan_config(console, target, ports_to_scan, ssl, wordlist_types, wordlist):
    """Display scan configuration panel"""
    console.print(Panel.fit(
        f"[bold green]Target:[/bold green] {target}\n"
        f"[bold green]Ports:[/bold green] {format_port_list(ports_to_scan)}\n"
        f"[bold green]SSL:[/bold green] {ssl}\n"
        f"[bold green]Wordlist:[/bold green] {', '.join(wordlist_types)}\n"
        f"[bold green]Total Hosts:[/bold green] {len(wordlist)}\n"
        f"[bold green]Total Scans:[/bold green] {len(wordlist) * len(ports_to_scan)}",
        title="Scan Configuration"
    ))


def display_scan_settings(console, arguments):
    """Display scan settings"""
    if arguments.ssl:
        console.print("[cyan][>] SSL enabled, using HTTPS[/cyan]")

    console.print(f"[cyan][>] Ignoring HTTP codes: {arguments.ignore_http_codes}[/cyan]")

    if arguments.ignore_content_length > 0:
        console.print(f"[cyan][>] Ignoring content length: {arguments.ignore_content_length}[/cyan]")


def display_summary_table(console, all_scanners):
    """Display summary table of findings by port"""
    table = Table(title="Findings by Port")
    table.add_column("Port", style="cyan", justify="right")
    table.add_column("Hosts Found", style="green", justify="right")
    table.add_column("Unique Hashes", style="yellow", justify="right")

    for port, scanner in all_scanners:
        unique_hashes = {h.hash for h in scanner.hosts}
        table.add_row(
            str(port),
            str(len(scanner.hosts)),
            str(len(unique_hashes))
        )

    console.print(table)
    console.print()


def output_port_results(console, all_scanners, arguments):
    """Output detailed results for each port"""
    for port, scanner in all_scanners:
        if len(scanner.hosts) > 0:
            console.print(f"\n[bold cyan]Results for port {port}:[/bold cyan]")
            output = output_helper(scanner, arguments)
            console.print(output.output_normal_likely())

            if arguments.fuzzy_logic:
                console.print(output.output_fuzzy())


def save_outputs(console, all_scanners, arguments, ports_to_scan):
    """Save output files for all scanners"""
    if arguments.output_normal:
        for port, scanner in all_scanners:
            if len(scanner.hosts) > 0:
                output = output_helper(scanner, arguments)
                filename = _get_port_filename(arguments.output_normal, port, ports_to_scan)
                output.write_normal(filename)
                console.print(f"[green][+] Output written to {filename}[/green]")

    if arguments.output_json:
        for port, scanner in all_scanners:
            if len(scanner.hosts) > 0:
                output = output_helper(scanner, arguments)
                filename = _get_port_filename(arguments.output_json, port, ports_to_scan)
                output.write_json(filename)
                console.print(f"[green][+] JSON output written to {filename}[/green]")


def _get_port_filename(base_filename, port, ports_to_scan):
    """Generate filename with port suffix if scanning multiple ports"""
    if len(ports_to_scan) == 1:
        return base_filename

    parts = base_filename.rsplit('.', 1)
    if len(parts) == 2:
        return f"{parts[0]}_port{port}.{parts[1]}"
    return f"{base_filename}_port{port}"


def get_ports_to_scan(arguments, console):
    """Parse and return list of ports to scan"""
    if arguments.ports:
        try:
            ports = parse_ports(arguments.ports)
            console.print(f"[cyan][>] Scanning multiple ports: {format_port_list(ports)}[/cyan]")
            return ports
        except ValueError as e:
            console.print(f"[red][!] Error parsing ports: {e}[/red]")
            sys.exit(1)
    return [arguments.port]


async def perform_scans(ports_to_scan, arguments, wordlist, user_agents, console):
    """Perform scans on all ports and return results"""
    all_scanners = []
    for port in ports_to_scan:
        console.print(f"\n[bold cyan]{'='*50}[/bold cyan]")
        console.print(f"[bold yellow]Scanning port {port}[/bold yellow]")
        console.print(f"[bold cyan]{'='*50}[/bold cyan]\n")

        scanner = await scan_single_port(port, arguments, wordlist, user_agents, console)
        all_scanners.append((port, scanner))

    return all_scanners


async def async_main():
    """Async main function with improved UX"""
    print_banner()
    console = Console()

    parser = cli_argument_parser()
    arguments = parser.parse(sys.argv[1:])

    wordlist_helper = WordList()
    wordlist, wordlist_types = wordlist_helper.get_wordlist(
        arguments.wordlists, arguments.prefix, arguments.suffix)

    if len(wordlist) == 0:
        console.print("[red][!] No words found[/red]")
        sys.exit(1)

    # Parse ports
    ports_to_scan = get_ports_to_scan(arguments, console)

    # Display scan configuration
    display_scan_config(console, arguments.target_hosts, ports_to_scan,
                       arguments.ssl, wordlist_types, wordlist)

    user_agents = setup_user_agents(arguments)
    display_scan_settings(console, arguments)

    if not arguments.no_lookup:
        wordlist = perform_dns_lookup(arguments.target_hosts, wordlist, arguments.verbose)

    if arguments.verbose:
        console.print(f"[cyan][>] Scanning with {len(wordlist)} items in wordlist[/cyan]")

    # Scan all ports
    all_scanners = await perform_scans(ports_to_scan, arguments, wordlist, user_agents, console)

    # Display results summary
    console.print(f"\n[bold green]{'='*50}[/bold green]")
    console.print("[bold green]Scan Results Summary[/bold green]")
    console.print(f"[bold green]{'='*50}[/bold green]\n")

    if len(ports_to_scan) > 1:
        display_summary_table(console, all_scanners)

    # Output detailed results
    output_port_results(console, all_scanners, arguments)

    # Save outputs if requested
    save_outputs(console, all_scanners, arguments, ports_to_scan)


def main():
    """Entry point that runs async main"""
    try:
        asyncio.run(async_main())
    except KeyboardInterrupt:
        console = Console()
        console.print("\n[yellow][!] Scan interrupted by user[/yellow]")
        sys.exit(0)
    except Exception as e:
        console = Console()
        console.print(f"[red][!] Fatal error: {e}[/red]")
        sys.exit(1)


if __name__ == "__main__":
    main()
