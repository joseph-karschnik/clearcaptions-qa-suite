"""
ASR (Automatic Speech Recognition) integration tests
Tests speech-to-text conversion accuracy and performance
"""
import pytest
from framework.utils.asr_client import ASRClient
from loguru import logger


@pytest.mark.integration
@pytest.mark.asr
class TestASRIntegration:
    """Test cases for ASR system integration"""
    
    def setup_method(self):
        """Setup for each test"""
        self.asr = ASRClient()
        self.test_call_id = "test_call_123"
    
    def test_asr_session_start(self):
        """Test ASR session initialization"""
        session_id = self.asr.start_session(self.test_call_id)
        
        assert session_id is not None, "Session ID should be generated"
        assert session_id.startswith("asr_session"), "Session ID should have correct prefix"
        assert self.test_call_id in session_id, "Session should include call ID"
        
        logger.info(f"ASR session started: {session_id}")
    
    def test_asr_audio_processing(self):
        """Test audio processing through ASR"""
        self.asr.start_session(self.test_call_id)
        
        reference_text = "Hello, this is a test of the ASR system."
        audio_data = b'\x00' * 8000  # Simulated audio
        
        result = self.asr.process_audio(audio_data, reference_text)
        
        assert 'transcription' in result, "Should return transcription"
        assert 'latency_ms' in result, "Should return latency"
        assert 'confidence' in result, "Should return confidence score"
        assert result['latency_ms'] > 0, "Latency should be positive"
        
        logger.info(f"ASR processing completed: {result['transcription']}")
    
    def test_asr_accuracy_calculation(self):
        """Test ASR accuracy calculation"""
        self.asr.start_session(self.test_call_id)
        
        reference_text = "ClearCaptions provides real-time phone captioning."
        audio_data = b'\x00' * 8000
        
        result = self.asr.process_audio(audio_data, reference_text)
        
        assert 'quality' in result, "Should include quality metrics"
        assert 'wer' in result['quality'], "Should calculate WER"
        assert 'accuracy' in result['quality'], "Should calculate accuracy"
        assert 0 <= result['quality']['wer'] <= 1, "WER should be between 0 and 1"
        assert 0 <= result['quality']['accuracy'] <= 1, "Accuracy should be between 0 and 1"
        
        logger.info(f"ASR accuracy: {result['quality']['accuracy']:.4f}")
    
    def test_asr_latency(self):
        """Test ASR processing latency"""
        self.asr.start_session(self.test_call_id)
        
        audio_data = b'\x00' * 8000
        latency_results = self.asr.test_asr_latency(audio_data, iterations=5)
        
        assert 'average_latency_ms' in latency_results
        assert 'min_latency_ms' in latency_results
        assert 'max_latency_ms' in latency_results
        assert latency_results['average_latency_ms'] > 0
        
        logger.info(f"ASR average latency: {latency_results['average_latency_ms']:.2f}ms")
    
    def test_asr_batch_accuracy(self):
        """Test ASR accuracy with multiple test cases"""
        self.asr.start_session(self.test_call_id)
        
        test_cases = [
            ("Hello world", b'\x00' * 2000),
            ("Testing ASR accuracy", b'\x00' * 3000),
            ("ClearCaptions service", b'\x00' * 2500),
        ]
        
        results = self.asr.test_asr_accuracy(test_cases)
        
        assert 'total_tests' in results
        assert 'average_wer' in results
        assert 'average_latency_ms' in results
        assert results['total_tests'] == len(test_cases)
        
        logger.info(f"Batch ASR test: {results['total_tests']} tests, "
                   f"avg WER: {results['average_wer']:.4f}")
    
    def test_asr_streaming_processing(self):
        """Test streaming audio processing"""
        self.asr.start_session(self.test_call_id)
        
        audio_chunks = [b'\x00' * 1000 for _ in range(5)]
        reference_texts = [f"Chunk {i}" for i in range(5)]
        
        results = self.asr.process_streaming_audio(audio_chunks, reference_texts)
        
        assert len(results) == len(audio_chunks), "Should process all chunks"
        for result in results:
            assert 'transcription' in result
            assert 'latency_ms' in result
        
        logger.info(f"Streaming ASR processed {len(results)} chunks")
    
    def test_asr_session_end(self):
        """Test ASR session termination"""
        session_id = self.asr.start_session(self.test_call_id)
        assert session_id is not None
        
        self.asr.end_session()
        assert self.asr.session_id is None, "Session should be cleared"
        
        logger.info("ASR session ended successfully")
