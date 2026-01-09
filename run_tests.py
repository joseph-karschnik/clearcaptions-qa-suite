#!/usr/bin/env python3
"""
Test execution script with options
"""
import sys
import subprocess
import argparse
from pathlib import Path


def run_tests(test_type=None, marker=None, browser=None, verbose=False, 
              parallel=False, report=True):
    """Run tests with specified options"""
    
    cmd = ["pytest"]
    
    # Add test path
    if test_type:
        cmd.append(f"tests/{test_type}/")
    else:
        cmd.append("tests/")
    
    # Add marker filter
    if marker:
        cmd.extend(["-m", marker])
    
    # Add browser option
    if browser:
        cmd.extend(["--browser", browser])
    
    # Verbose output
    if verbose:
        cmd.append("-v")
    else:
        cmd.append("-q")
    
    # Parallel execution
    if parallel:
        cmd.extend(["-n", "auto"])
    
    # Reporting
    if report:
        cmd.extend([
            "--html=reports/report.html",
            "--self-contained-html",
            "--json-report",
            "--json-report-file=reports/report.json"
        ])
    
    # Run tests
    print(f"Running command: {' '.join(cmd)}")
    result = subprocess.run(cmd)
    return result.returncode


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(description="Run ClearCaptions QA tests")
    
    parser.add_argument(
        "-t", "--type",
        choices=["web", "api", "accessibility", "caption_quality", "compliance"],
        help="Test type to run"
    )
    
    parser.add_argument(
        "-m", "--marker",
        choices=["smoke", "regression", "accessibility", "caption_quality", 
                 "compliance", "api", "web"],
        help="Test marker to filter"
    )
    
    parser.add_argument(
        "-b", "--browser",
        choices=["chrome", "firefox"],
        help="Browser to use"
    )
    
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Verbose output"
    )
    
    parser.add_argument(
        "-p", "--parallel",
        action="store_true",
        help="Run tests in parallel"
    )
    
    parser.add_argument(
        "--no-report",
        action="store_true",
        help="Skip report generation"
    )
    
    args = parser.parse_args()
    
    # Create reports directory
    Path("reports").mkdir(exist_ok=True)
    
    # Run tests
    exit_code = run_tests(
        test_type=args.type,
        marker=args.marker,
        browser=args.browser,
        verbose=args.verbose,
        parallel=args.parallel,
        report=not args.no_report
    )
    
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
