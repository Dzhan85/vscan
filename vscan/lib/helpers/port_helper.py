"""Port parsing and handling utilities"""
import re


def parse_ports(port_string):
    """
    Parse port string and return list of ports to scan.

    Supports:
    - Single port: "80"
    - Multiple ports: "80,443,8080"
    - Port ranges: "8000-9000"
    - Combination: "80,443,8000-8010"

    Args:
        port_string (str): Port specification string

    Returns:
        list: List of unique port integers

    Raises:
        ValueError: If port string is invalid or contains invalid ports

    Examples:
        >>> parse_ports("80,443")
        [80, 443]

        >>> parse_ports("80-82")
        [80, 81, 82]

        >>> parse_ports("80,443,8000-8002")
        [80, 443, 8000, 8001, 8002]
    """
    if not port_string:
        return []

    ports = set()

    # Split by comma
    parts = port_string.split(',')

    for part in parts:
        part = part.strip()

        # Check if it's a range (e.g., "80-100")
        if '-' in part:
            try:
                start, end = part.split('-', 1)
                start = int(start.strip())
                end = int(end.strip())

                if start < 1 or start > 65535:
                    raise ValueError(f"Invalid port range start: {start}")
                if end < 1 or end > 65535:
                    raise ValueError(f"Invalid port range end: {end}")
                if start > end:
                    raise ValueError(f"Invalid port range: {start}-{end} (start > end)")

                # Add all ports in range
                for port in range(start, end + 1):
                    ports.add(port)

            except ValueError as e:
                if "invalid literal" in str(e):
                    raise ValueError(f"Invalid port range format: {part}")
                raise
        else:
            # Single port
            try:
                port = int(part)
                if port < 1 or port > 65535:
                    raise ValueError(f"Invalid port number: {port}")
                ports.add(port)
            except ValueError:
                raise ValueError(f"Invalid port number: {part}")

    return sorted(list(ports))


def get_common_ports():
    """
    Return list of commonly scanned web server ports.

    Returns:
        list: Common web server ports
    """
    return [80, 443, 8000, 8080, 8443, 8888, 3000, 5000]


def get_all_web_ports():
    """
    Return comprehensive list of web-related ports.

    Returns:
        list: Extended list of web server ports
    """
    return [
        80, 81, 443, 591, 2082, 2087, 2095, 2096,
        3000, 5000, 5104, 5800, 6543, 7000, 7396,
        7474, 8000, 8001, 8008, 8014, 8042, 8069,
        8080, 8081, 8088, 8090, 8091, 8118, 8123,
        8172, 8222, 8243, 8280, 8281, 8333, 8443,
        8500, 8834, 8880, 8888, 8983, 9000, 9043,
        9060, 9080, 9090, 9091, 9200, 9443, 9800,
        9981, 12443, 16080, 18091, 18092, 20720,
        28017
    ]


def format_port_list(ports):
    """
    Format a list of ports into a human-readable string.

    Args:
        ports (list): List of port numbers

    Returns:
        str: Formatted port list

    Examples:
        >>> format_port_list([80, 443])
        "80, 443"

        >>> format_port_list([80, 81, 82])
        "80-82"
    """
    if not ports:
        return ""

    if len(ports) == 1:
        return str(ports[0])

    # Sort ports
    sorted_ports = sorted(ports)

    # Try to find ranges
    ranges = []
    start = sorted_ports[0]
    end = sorted_ports[0]

    for i in range(1, len(sorted_ports)):
        if sorted_ports[i] == end + 1:
            # Continue range
            end = sorted_ports[i]
        else:
            # End current range
            if start == end:
                ranges.append(str(start))
            elif end == start + 1:
                ranges.append(f"{start}, {end}")
            else:
                ranges.append(f"{start}-{end}")
            start = sorted_ports[i]
            end = sorted_ports[i]

    # Add last range
    if start == end:
        ranges.append(str(start))
    elif end == start + 1:
        ranges.append(f"{start}, {end}")
    else:
        ranges.append(f"{start}-{end}")

    return ", ".join(ranges)
