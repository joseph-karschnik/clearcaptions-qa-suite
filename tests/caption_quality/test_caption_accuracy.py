"""
Caption quality and accuracy tests
Tests WER, latency, accuracy, and readability
"""
import pytest
import time
from framework.base.base_test import BaseTest
from framework.pages.caption_page import CaptionPage
from framework.utils.caption_quality import CaptionQualityAnalyzer
from framework.utils.config_loader import ConfigLoader
from loguru import logger


@pytest.mark.caption_quality
@pytest.mark.compliance
class TestCaptionAccuracy(BaseTest):
    """Test cases for caption accuracy and quality"""
    
    def setup_method(self):
        """Setup for each test"""
        super().setup_method()
        self.config = ConfigLoader().load_config()
        self.quality_analyzer = CaptionQualityAnalyzer(
            wer_threshold=self.config['caption_quality']['wer_threshold'],
            latency_threshold_ms=self.config['caption_quality']['latency_threshold_ms'],
            accuracy_threshold=self.config['caption_quality']['accuracy_threshold']
        )
    
    def test_wer_calculation(self):
        """Test Word Error Rate calculation"""
        reference = "Hello, this is a test of the captioning system."
        hypothesis = "Hello, this is a test of the caption system."
        
        wer = self.quality_analyzer.calculate_wer(reference, hypothesis)
        
        assert wer >= 0, "WER should be non-negative"
        assert wer <= 1, "WER should be between 0 and 1"
        logger.info(f"WER calculated: {wer:.4f}")
    
    def test_caption_latency(self):
        """Test caption latency measurement"""
        caption_page = CaptionPage(self.driver)
        caption_page.load()
        
        # Simulate call initiation and measure latency
        start_time = time.time()
        
        # In real scenario, would initiate call and wait for caption
        # For now, simulate with a delay
        time.sleep(0.5)  # Simulated processing time
        
        end_time = time.time()
        latency_ms = self.quality_analyzer.measure_latency(start_time, end_time)
        
        assert latency_ms >= 0, "Latency should be non-negative"
        logger.info(f"Latency measured: {latency_ms:.2f}ms")
        
        # Check against threshold
        threshold = self.config['caption_quality']['latency_threshold_ms']
        assert latency_ms < threshold, \
            f"Latency {latency_ms}ms exceeds threshold {threshold}ms"
    
    def test_caption_accuracy(self):
        """Test caption accuracy calculation"""
        reference = "The quick brown fox jumps over the lazy dog."
        hypothesis = "The quick brown fox jumps over the lazy dog."
        
        accuracy = self.quality_analyzer.calculate_accuracy(reference, hypothesis)
        
        assert 0 <= accuracy <= 1, "Accuracy should be between 0 and 1"
        assert accuracy > 0.9, "Perfect match should have high accuracy"
        logger.info(f"Accuracy calculated: {accuracy:.4f}")
    
    def test_readability_score(self):
        """Test readability score calculation"""
        test_text = "This is a simple sentence. It has good readability."
        
        score = self.quality_analyzer.calculate_readability_score(test_text)
        
        assert 0 <= score <= 1, "Readability score should be between 0 and 1"
        logger.info(f"Readability score: {score:.4f}")
    
    def test_comprehensive_quality_analysis(self):
        """Test comprehensive caption quality analysis"""
        reference = "ClearCaptions provides real-time phone captioning for individuals with hearing loss."
        hypothesis = "ClearCaptions provides real-time phone captioning for individuals with hearing loss."
        
        # Simulate latency
        latency_ms = 1500  # 1.5 seconds
        
        results = self.quality_analyzer.analyze_caption_quality(
            reference, hypothesis, latency_ms
        )
        
        assert 'wer' in results, "Results should include WER"
        assert 'accuracy' in results, "Results should include accuracy"
        assert 'latency_ms' in results, "Results should include latency"
        assert 'readability' in results, "Results should include readability"
        assert 'passed' in results, "Results should include pass/fail status"
        
        logger.info(f"Quality analysis completed. Passed: {results['passed']}")
        if results['issues']:
            logger.warning(f"Issues found: {results['issues']}")
    
    def test_batch_quality_analysis(self):
        """Test batch analysis of multiple caption test cases"""
        test_cases = [
            ("Hello world", "Hello world", 1000),
            ("Testing caption accuracy", "Testing caption accuracy", 1200),
            ("ClearCaptions service", "ClearCaptions service", 1500),
        ]
        
        results = self.quality_analyzer.batch_analyze(test_cases)
        
        assert 'summary' in results, "Results should include summary"
        assert 'individual_results' in results, "Results should include individual results"
        
        summary = results['summary']
        assert summary['total_tests'] == len(test_cases), \
            "Total tests should match input"
        
        logger.info(f"Batch analysis: {summary['passed']}/{summary['total_tests']} passed")
        logger.info(f"Average WER: {summary['avg_wer']:.4f}")
        logger.info(f"Average latency: {summary['avg_latency_ms']:.2f}ms")
