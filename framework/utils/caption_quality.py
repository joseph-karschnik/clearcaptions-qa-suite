"""
Caption quality testing utilities
Calculates WER, latency, accuracy, and readability metrics
"""
import time
import re
from typing import List, Tuple, Dict
from jiwer import wer, cer
import numpy as np
from loguru import logger


class CaptionQualityAnalyzer:
    """Analyzes caption quality metrics"""
    
    def __init__(self, wer_threshold: float = 0.05, 
                 latency_threshold_ms: int = 2000,
                 accuracy_threshold: float = 0.95):
        self.wer_threshold = wer_threshold
        self.latency_threshold_ms = latency_threshold_ms
        self.accuracy_threshold = accuracy_threshold
    
    def calculate_wer(self, reference: str, hypothesis: str) -> float:
        """
        Calculate Word Error Rate (WER)
        WER = (S + D + I) / N
        where S = substitutions, D = deletions, I = insertions, N = total words
        """
        try:
            error_rate = wer(reference, hypothesis)
            logger.info(f"WER calculated: {error_rate:.4f}")
            return error_rate
        except Exception as e:
            logger.error(f"Error calculating WER: {e}")
            return 1.0  # Worst case
    
    def calculate_cer(self, reference: str, hypothesis: str) -> float:
        """Calculate Character Error Rate (CER)"""
        try:
            error_rate = cer(reference, hypothesis)
            logger.info(f"CER calculated: {error_rate:.4f}")
            return error_rate
        except Exception as e:
            logger.error(f"Error calculating CER: {e}")
            return 1.0
    
    def measure_latency(self, start_time: float, end_time: float) -> float:
        """Measure latency in milliseconds"""
        latency_ms = (end_time - start_time) * 1000
        logger.info(f"Latency measured: {latency_ms:.2f}ms")
        return latency_ms
    
    def calculate_accuracy(self, reference: str, hypothesis: str) -> float:
        """Calculate accuracy as (1 - WER)"""
        wer_value = self.calculate_wer(reference, hypothesis)
        accuracy = 1 - wer_value
        return accuracy
    
    def calculate_readability_score(self, text: str) -> float:
        """
        Calculate readability score based on:
        - Sentence length
        - Word complexity
        - Punctuation usage
        Returns score between 0 and 1
        """
        if not text:
            return 0.0
        
        sentences = re.split(r'[.!?]+', text)
        sentences = [s.strip() for s in sentences if s.strip()]
        
        if not sentences:
            return 0.0
        
        # Average sentence length
        avg_sentence_length = sum(len(s.split()) for s in sentences) / len(sentences)
        
        # Word complexity (average word length)
        words = text.split()
        avg_word_length = sum(len(word) for word in words) / len(words) if words else 0
        
        # Normalize scores (ideal: 10-15 words per sentence, 4-5 chars per word)
        sentence_score = 1.0 - min(abs(avg_sentence_length - 12.5) / 12.5, 1.0)
        word_score = 1.0 - min(abs(avg_word_length - 4.5) / 4.5, 1.0)
        
        readability = (sentence_score + word_score) / 2
        logger.info(f"Readability score: {readability:.4f}")
        return readability
    
    def analyze_caption_quality(self, reference: str, hypothesis: str, 
                               latency_ms: float) -> Dict[str, any]:
        """
        Comprehensive caption quality analysis
        Returns dictionary with all metrics
        """
        results = {
            'wer': self.calculate_wer(reference, hypothesis),
            'cer': self.calculate_cer(reference, hypothesis),
            'accuracy': self.calculate_accuracy(reference, hypothesis),
            'latency_ms': latency_ms,
            'readability': self.calculate_readability_score(hypothesis),
            'passed': True,
            'issues': []
        }
        
        # Check thresholds
        if results['wer'] > self.wer_threshold:
            results['passed'] = False
            results['issues'].append(f"WER {results['wer']:.4f} exceeds threshold {self.wer_threshold}")
        
        if results['latency_ms'] > self.latency_threshold_ms:
            results['passed'] = False
            results['issues'].append(f"Latency {results['latency_ms']:.2f}ms exceeds threshold {self.latency_threshold_ms}ms")
        
        if results['accuracy'] < self.accuracy_threshold:
            results['passed'] = False
            results['issues'].append(f"Accuracy {results['accuracy']:.4f} below threshold {self.accuracy_threshold}")
        
        return results
    
    def batch_analyze(self, test_cases: List[Tuple[str, str, float]]) -> Dict[str, any]:
        """
        Analyze multiple caption test cases
        test_cases: List of (reference, hypothesis, latency_ms) tuples
        """
        results = []
        for reference, hypothesis, latency_ms in test_cases:
            result = self.analyze_caption_quality(reference, hypothesis, latency_ms)
            results.append(result)
        
        # Aggregate statistics
        avg_wer = np.mean([r['wer'] for r in results])
        avg_latency = np.mean([r['latency_ms'] for r in results])
        avg_accuracy = np.mean([r['accuracy'] for r in results])
        pass_rate = sum(1 for r in results if r['passed']) / len(results)
        
        return {
            'individual_results': results,
            'summary': {
                'total_tests': len(results),
                'passed': sum(1 for r in results if r['passed']),
                'failed': sum(1 for r in results if not r['passed']),
                'pass_rate': pass_rate,
                'avg_wer': avg_wer,
                'avg_latency_ms': avg_latency,
                'avg_accuracy': avg_accuracy
            }
        }
