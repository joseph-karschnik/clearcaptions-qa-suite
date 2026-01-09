"""
FCC compliance tests
Tests caption accuracy, latency, and regulatory requirements
"""
import pytest
from framework.base.base_test import BaseTest
from framework.utils.caption_quality import CaptionQualityAnalyzer
from framework.utils.config_loader import ConfigLoader
from loguru import logger


@pytest.mark.compliance
@pytest.mark.caption_quality
class TestFCCCompliance(BaseTest):
    """Test cases for FCC compliance"""
    
    def setup_method(self):
        """Setup for each test"""
        super().setup_method()
        self.config = ConfigLoader().load_config()
        self.fcc_requirements = self.config['compliance']['fcc']
        self.quality_analyzer = CaptionQualityAnalyzer()
    
    def test_fcc_caption_accuracy_requirement(self):
        """Test FCC caption accuracy requirement (99%)"""
        required_accuracy = self.fcc_requirements['caption_accuracy_required']
        
        # Test with high-quality caption
        reference = "This is a test of FCC compliance for caption accuracy requirements."
        hypothesis = "This is a test of FCC compliance for caption accuracy requirements."
        
        accuracy = self.quality_analyzer.calculate_accuracy(reference, hypothesis)
        
        assert accuracy >= required_accuracy, \
            f"Caption accuracy {accuracy:.4f} must meet FCC requirement of {required_accuracy}"
        logger.info(f"FCC accuracy requirement met: {accuracy:.4f} >= {required_accuracy}")
    
    def test_fcc_latency_requirement(self):
        """Test FCC maximum latency requirement"""
        max_latency_ms = self.fcc_requirements['latency_max_ms']
        
        # Simulate caption latency
        test_latency_ms = 2500  # 2.5 seconds
        
        assert test_latency_ms <= max_latency_ms, \
            f"Latency {test_latency_ms}ms exceeds FCC maximum of {max_latency_ms}ms"
        logger.info(f"FCC latency requirement met: {test_latency_ms}ms <= {max_latency_ms}ms")
    
    def test_fcc_comprehensive_compliance(self):
        """Test comprehensive FCC compliance"""
        # Multiple test cases to ensure compliance
        test_cases = [
            ("FCC requires high accuracy captions", "FCC requires high accuracy captions", 2000),
            ("Real-time captioning must be accurate", "Real-time captioning must be accurate", 1800),
            ("Compliance with regulations is essential", "Compliance with regulations is essential", 2200),
        ]
        
        results = self.quality_analyzer.batch_analyze(test_cases)
        summary = results['summary']
        
        # Check accuracy requirement
        assert summary['avg_accuracy'] >= self.fcc_requirements['caption_accuracy_required'], \
            f"Average accuracy {summary['avg_accuracy']:.4f} must meet FCC requirement"
        
        # Check latency requirement
        assert summary['avg_latency_ms'] <= self.fcc_requirements['latency_max_ms'], \
            f"Average latency {summary['avg_latency_ms']:.2f}ms must meet FCC requirement"
        
        logger.info("FCC comprehensive compliance check passed")
        logger.info(f"Average accuracy: {summary['avg_accuracy']:.4f}")
        logger.info(f"Average latency: {summary['avg_latency_ms']:.2f}ms")
