"""
Test report generator
Creates comprehensive test reports with metrics
"""
import json
import os
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any
from loguru import logger


class ReportGenerator:
    """Generates comprehensive test reports"""
    
    def __init__(self, output_dir: str = "reports"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    def generate_json_report(self, test_results: Dict[str, Any], filename: str = None) -> str:
        """Generate JSON test report"""
        if not filename:
            filename = f"test_report_{self.timestamp}.json"
        
        filepath = self.output_dir / filename
        
        report = {
            'timestamp': datetime.now().isoformat(),
            'summary': {
                'total_tests': test_results.get('total', 0),
                'passed': test_results.get('passed', 0),
                'failed': test_results.get('failed', 0),
                'skipped': test_results.get('skipped', 0),
                'pass_rate': self._calculate_pass_rate(test_results)
            },
            'test_results': test_results.get('tests', []),
            'metrics': test_results.get('metrics', {})
        }
        
        with open(filepath, 'w') as f:
            json.dump(report, f, indent=2)
        
        logger.info(f"JSON report generated: {filepath}")
        return str(filepath)
    
    def generate_html_summary(self, test_results: Dict[str, Any], filename: str = None) -> str:
        """Generate HTML summary report"""
        if not filename:
            filename = f"test_summary_{self.timestamp}.html"
        
        filepath = self.output_dir / filename
        
        summary = test_results.get('summary', {})
        pass_rate = self._calculate_pass_rate(test_results)
        
        html = f"""
<!DOCTYPE html>
<html>
<head>
    <title>ClearCaptions Test Report</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; }}
        .header {{ background-color: #2c3e50; color: white; padding: 20px; border-radius: 5px; }}
        .summary {{ margin: 20px 0; padding: 20px; background-color: #ecf0f1; border-radius: 5px; }}
        .metric {{ display: inline-block; margin: 10px; padding: 15px; background-color: white; border-radius: 5px; min-width: 150px; }}
        .metric-value {{ font-size: 24px; font-weight: bold; }}
        .passed {{ color: #27ae60; }}
        .failed {{ color: #e74c3c; }}
        .skipped {{ color: #f39c12; }}
        table {{ width: 100%; border-collapse: collapse; margin-top: 20px; }}
        th, td {{ padding: 12px; text-align: left; border-bottom: 1px solid #ddd; }}
        th {{ background-color: #34495e; color: white; }}
        tr:hover {{ background-color: #f5f5f5; }}
    </style>
</head>
<body>
    <div class="header">
        <h1>ClearCaptions QA Test Report</h1>
        <p>Generated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</p>
    </div>
    
    <div class="summary">
        <h2>Test Summary</h2>
        <div class="metric">
            <div>Total Tests</div>
            <div class="metric-value">{summary.get('total', 0)}</div>
        </div>
        <div class="metric">
            <div class="passed">Passed</div>
            <div class="metric-value passed">{summary.get('passed', 0)}</div>
        </div>
        <div class="metric">
            <div class="failed">Failed</div>
            <div class="metric-value failed">{summary.get('failed', 0)}</div>
        </div>
        <div class="metric">
            <div class="skipped">Skipped</div>
            <div class="metric-value skipped">{summary.get('skipped', 0)}</div>
        </div>
        <div class="metric">
            <div>Pass Rate</div>
            <div class="metric-value">{pass_rate:.1f}%</div>
        </div>
    </div>
    
    <h2>Test Results</h2>
    <table>
        <tr>
            <th>Test Name</th>
            <th>Status</th>
            <th>Duration</th>
            <th>Category</th>
        </tr>
"""
        
        for test in test_results.get('tests', []):
            status_class = test.get('status', 'unknown').lower()
            html += f"""
        <tr>
            <td>{test.get('name', 'Unknown')}</td>
            <td class="{status_class}">{test.get('status', 'Unknown')}</td>
            <td>{test.get('duration', 0):.2f}s</td>
            <td>{test.get('category', 'N/A')}</td>
        </tr>
"""
        
        html += """
    </table>
</body>
</html>
"""
        
        with open(filepath, 'w') as f:
            f.write(html)
        
        logger.info(f"HTML report generated: {filepath}")
        return str(filepath)
    
    def generate_metrics_report(self, metrics: Dict[str, Any], filename: str = None) -> str:
        """Generate metrics report"""
        if not filename:
            filename = f"metrics_{self.timestamp}.json"
        
        filepath = self.output_dir / filename
        
        report = {
            'timestamp': datetime.now().isoformat(),
            'caption_quality': metrics.get('caption_quality', {}),
            'accessibility': metrics.get('accessibility', {}),
            'performance': metrics.get('performance', {}),
            'compliance': metrics.get('compliance', {})
        }
        
        with open(filepath, 'w') as f:
            json.dump(report, f, indent=2)
        
        logger.info(f"Metrics report generated: {filepath}")
        return str(filepath)
    
    def _calculate_pass_rate(self, test_results: Dict[str, Any]) -> float:
        """Calculate pass rate percentage"""
        total = test_results.get('total', 0)
        passed = test_results.get('passed', 0)
        
        if total == 0:
            return 0.0
        
        return (passed / total) * 100
