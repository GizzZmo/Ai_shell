#!/usr/bin/env python3
"""
AI Shell Audit Log Viewer

Simple utility to view and analyze AI Shell audit logs.
"""

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path

from ai_shell.audit import get_audit_logger
from ai_shell.ui import format_info, format_warning, format_error, format_success


def print_command_history(limit: int = 10):
    """Print recent command history."""
    audit_logger = get_audit_logger()
    commands = audit_logger.get_recent_commands(limit)
    
    if not commands:
        print(format_warning("No command history found"))
        return
    
    print(format_info(f"Recent Commands (last {len(commands)}):"))
    print("=" * 60)
    
    for i, cmd in enumerate(commands, 1):
        timestamp = cmd.get("timestamp", "unknown")
        command = cmd.get("command", "unknown")
        success = cmd.get("success", False)
        status_icon = "✅" if success else "❌"
        
        print(f"{i:2d}. {status_icon} [{timestamp}]")
        print(f"    Command: {command}")
        print(f"    Prompt:  {cmd.get('user_prompt', 'N/A')}")
        print(f"    User:    {cmd.get('user', 'unknown')}")
        print()


def print_security_events(hours: int = 24):
    """Print recent security events."""
    audit_logger = get_audit_logger()
    events = audit_logger.get_security_events(hours)
    
    if not events:
        print(format_info(f"No security events in the last {hours} hours"))
        return
    
    print(format_warning(f"Security Events (last {hours} hours):"))
    print("=" * 60)
    
    for i, event in enumerate(events, 1):
        timestamp = event.get("timestamp", "unknown")
        event_type = event.get("security_event_type", "unknown")
        command = event.get("command", "unknown")
        
        print(f"{i:2d}. 🔒 [{timestamp}]")
        print(f"    Event:   {event_type}")
        print(f"    Command: {command}")
        print(f"    User:    {event.get('user', 'unknown')}")
        if event.get("details"):
            print(f"    Details: {event['details']}")
        print()


def print_audit_report():
    """Print comprehensive audit report."""
    audit_logger = get_audit_logger()
    report = audit_logger.generate_audit_report()
    
    if "error" in report:
        print(format_error(f"Error generating report: {report['error']}"))
        return
    
    print(format_success("AI Shell Audit Report"))
    print("=" * 50)
    print(f"Total Commands:       {report['total_commands']}")
    print(f"Successful Commands:  {report['successful_commands']}")
    print(f"Failed Commands:      {report['failed_commands']}")
    print(f"Blocked Commands:     {report['blocked_commands']}")
    print(f"Security Events:      {report['security_events']}")
    print(f"Unique Users:         {len(report['unique_users'])}")
    
    if report['unique_users']:
        print(f"Users:                {', '.join(report['unique_users'])}")
    
    if report['most_recent_activity']:
        print(f"Last Activity:        {report['most_recent_activity']}")
    
    if report['top_commands']:
        print("\nTop Commands:")
        for cmd, count in report['top_commands'].items():
            print(f"  {cmd:15} {count:3d} times")


def export_audit_log(output_file: str, format_type: str = "json"):
    """Export audit log to different formats."""
    audit_logger = get_audit_logger()
    
    if not Path(audit_logger.audit_file).exists():
        print(format_error("No audit log file found"))
        return
    
    try:
        with open(audit_logger.audit_file, 'r') as f:
            lines = f.readlines()
        
        if format_type == "json":
            # Pretty print JSON
            with open(output_file, 'w') as f:
                f.write('[\n')
                for i, line in enumerate(lines):
                    if line.strip():
                        entry = json.loads(line.strip())
                        json.dump(entry, f, indent=2)
                        if i < len(lines) - 1:
                            f.write(',')
                        f.write('\n')
                f.write(']\n')
        
        elif format_type == "csv":
            import csv
            
            # Extract all entries and determine all possible fields
            entries = []
            all_fields = set()
            
            for line in lines:
                if line.strip():
                    entry = json.loads(line.strip())
                    entries.append(entry)
                    all_fields.update(entry.keys())
            
            # Write CSV
            with open(output_file, 'w', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=sorted(all_fields))
                writer.writeheader()
                writer.writerows(entries)
        
        print(format_success(f"Audit log exported to {output_file} ({format_type} format)"))
        
    except Exception as e:
        print(format_error(f"Failed to export audit log: {e}"))


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="AI Shell Audit Log Viewer",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  ai-shell-audit                    # Show recent commands
  ai-shell-audit --history 20      # Show last 20 commands
  ai-shell-audit --security        # Show security events
  ai-shell-audit --report          # Show full audit report
  ai-shell-audit --export audit.json  # Export to JSON
        """
    )
    
    parser.add_argument(
        '--history', '-H', type=int, metavar='N',
        help='Show last N commands (default: 10)'
    )
    
    parser.add_argument(
        '--security', '-s', action='store_true',
        help='Show security events from last 24 hours'
    )
    
    parser.add_argument(
        '--security-hours', type=int, default=24, metavar='HOURS',
        help='Hours of security events to show (default: 24)'
    )
    
    parser.add_argument(
        '--report', '-r', action='store_true',
        help='Show comprehensive audit report'
    )
    
    parser.add_argument(
        '--export', '-e', metavar='FILE',
        help='Export audit log to file'
    )
    
    parser.add_argument(
        '--format', choices=['json', 'csv'], default='json',
        help='Export format (default: json)'
    )
    
    args = parser.parse_args()
    
    # If no specific action, show recent commands
    if not any([args.security, args.report, args.export]):
        print_command_history(args.history or 10)
    
    if args.security:
        print_security_events(args.security_hours)
    
    if args.report:
        print_audit_report()
    
    if args.export:
        export_audit_log(args.export, args.format)


if __name__ == "__main__":
    main()