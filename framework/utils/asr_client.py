"""
ASR (Automatic Speech Recognition) client for testing
Tests speech-to-text conversion accuracy and latency
"""
import time
import json
from typing import Dict, Any, List, Optional, Tuple
from loguru import logger
from framework.utils.config_loader import ConfigLoader
from framework.utils.caption_quality import CaptionQualityAnalyzer


class ASRClient:
    """Client for ASR system testing"""
    
    def __init__(self, api_url: str = None):
        self.config = ConfigLoader().load_config()
        self.api_url = api_url or self.config.get('asr', {}).get('api_url', '')
        self.quality_analyzer = CaptionQualityAnalyzer()
        self.session_id = None
    
    def start_session(self, call_id: str, language: str = "en-US") -> str:
        """Start ASR session for a call"""
        self.session_id = f"asr_session_{call_id}_{int(time.time())}"
        logger.info(f"ASR session started: {self.session_id} for call {call_id}")
        return self.session_id
    
    def process_audio(self, audio_data: bytes, reference_text: str = None) -> Dict[str, Any]:
        """
        Process audio through ASR and return transcription
        In real implementation, this would call ASR API
        For testing, we simulate with reference text
        """
        start_time = time.time()
        
        # Simulate ASR processing delay
        processing_time = 0.1  # 100ms typical ASR processing
        
        # In real implementation:
        # response = requests.post(f"{self.api_url}/transcribe", 
        #                         files={'audio': audio_data})
        # transcription = response.json()['text']
        
        # For testing, use reference text if provided
        if reference_text:
            transcription = reference_text
        else:
            # Simulate transcription (would be actual ASR output)
            transcription = "Simulated transcription from ASR"
        
        end_time = time.time()
        latency_ms = (end_time - start_time) * 1000
        
        result = {
            'transcription': transcription,
            'latency_ms': latency_ms,
            'confidence': 0.95,  # Simulated confidence score
            'timestamp': time.time(),
            'session_id': self.session_id
        }
        
        # Calculate quality metrics if reference provided
        if reference_text:
            quality = self.quality_analyzer.analyze_caption_quality(
                reference_text, transcription, latency_ms
            )
            result['quality'] = quality
        
        logger.info(f"ASR processed: {len(transcription)} chars, latency: {latency_ms:.2f}ms")
        return result
    
    def process_streaming_audio(self, audio_chunks: List[bytes], 
                               reference_texts: List[str] = None) -> List[Dict[str, Any]]:
        """Process streaming audio chunks"""
        results = []
        
        for i, chunk in enumerate(audio_chunks):
            reference = reference_texts[i] if reference_texts and i < len(reference_texts) else None
            result = self.process_audio(chunk, reference)
            results.append(result)
        
        return results
    
    def test_asr_accuracy(self, test_cases: List[Tuple[str, str]]) -> Dict[str, Any]:
        """
        Test ASR accuracy with multiple test cases
        test_cases: List of (reference_text, audio_data) tuples
        """
        results = []
        total_wer = 0
        total_latency = 0
        
        for reference_text, audio_data in test_cases:
            result = self.process_audio(audio_data, reference_text)
            
            if 'quality' in result:
                results.append({
                    'reference': reference_text,
                    'transcription': result['transcription'],
                    'wer': result['quality']['wer'],
                    'accuracy': result['quality']['accuracy'],
                    'latency_ms': result['latency_ms']
                })
                total_wer += result['quality']['wer']
                total_latency += result['latency_ms']
        
        avg_wer = total_wer / len(results) if results else 0
        avg_latency = total_latency / len(results) if results else 0
        
        return {
            'total_tests': len(test_cases),
            'results': results,
            'average_wer': avg_wer,
            'average_latency_ms': avg_latency,
            'average_accuracy': 1 - avg_wer
        }
    
    def test_asr_latency(self, audio_data: bytes, iterations: int = 10) -> Dict[str, Any]:
        """Test ASR latency with multiple iterations"""
        latencies = []
        
        for _ in range(iterations):
            result = self.process_audio(audio_data)
            latencies.append(result['latency_ms'])
        
        return {
            'iterations': iterations,
            'latencies_ms': latencies,
            'average_latency_ms': sum(latencies) / len(latencies),
            'min_latency_ms': min(latencies),
            'max_latency_ms': max(latencies),
            'p95_latency_ms': sorted(latencies)[int(len(latencies) * 0.95)]
        }
    
    def test_different_accents(self, test_cases: Dict[str, Tuple[str, bytes]]) -> Dict[str, Any]:
        """
        Test ASR with different accents/dialects
        test_cases: Dict of {accent_name: (reference_text, audio_data)}
        """
        results = {}
        
        for accent, (reference, audio) in test_cases.items():
            result = self.process_audio(audio, reference)
            if 'quality' in result:
                results[accent] = {
                    'wer': result['quality']['wer'],
                    'accuracy': result['quality']['accuracy'],
                    'latency_ms': result['latency_ms']
                }
        
        return results
    
    def end_session(self):
        """End ASR session"""
        if self.session_id:
            logger.info(f"ASR session ended: {self.session_id}")
            self.session_id = None
