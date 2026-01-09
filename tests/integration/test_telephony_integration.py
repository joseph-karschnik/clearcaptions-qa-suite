"""
Telephony integration tests
Tests call routing, audio capture, and call lifecycle
"""
import pytest
import time
from framework.utils.telephony_client import TelephonyClient
from loguru import logger


@pytest.mark.integration
@pytest.mark.telephony
class TestTelephonyIntegration:
    """Test cases for telephony system integration"""
    
    def setup_method(self):
        """Setup for each test"""
        self.telephony = TelephonyClient()
        self.test_from_number = "+15551111111"
        self.test_to_number = "+15552222222"
    
    def test_call_initiation(self):
        """Test call initiation"""
        call_data = self.telephony.initiate_call(
            self.test_from_number,
            self.test_to_number
        )
        
        assert 'call_id' in call_data, "Call should have call_id"
        assert call_data['status'] == 'ringing', "Call should be in ringing state"
        assert call_data['from_number'] == self.test_from_number
        assert call_data['to_number'] == self.test_to_number
        
        logger.info(f"Call initiated successfully: {call_data['call_id']}")
    
    def test_call_answer(self):
        """Test call answer functionality"""
        call_data = self.telephony.initiate_call(
            self.test_from_number,
            self.test_to_number
        )
        call_id = call_data['call_id']
        
        answered = self.telephony.answer_call(call_id)
        
        assert answered['status'] == 'active', "Call should be active after answer"
        assert 'answered_at' in answered, "Should have answered timestamp"
        
        logger.info("Call answered successfully")
    
    def test_call_end(self):
        """Test call termination"""
        call_data = self.telephony.initiate_call(
            self.test_from_number,
            self.test_to_number
        )
        call_id = call_data['call_id']
        
        self.telephony.answer_call(call_id)
        time.sleep(0.1)  # Simulate call duration
        
        ended = self.telephony.end_call(call_id)
        
        assert ended['status'] == 'ended', "Call should be ended"
        assert 'ended_at' in ended, "Should have ended timestamp"
        assert 'duration' in ended, "Should have call duration"
        assert ended['duration'] > 0, "Duration should be positive"
        
        logger.info(f"Call ended successfully, duration: {ended['duration']:.2f}s")
    
    def test_call_lifecycle(self):
        """Test complete call lifecycle"""
        # Initiate
        call_data = self.telephony.initiate_call(
            self.test_from_number,
            self.test_to_number
        )
        call_id = call_data['call_id']
        assert call_data['status'] == 'ringing'
        
        # Answer
        answered = self.telephony.answer_call(call_id)
        assert answered['status'] == 'active'
        
        # Active call
        status = self.telephony.get_call_status(call_id)
        assert status['status'] == 'active'
        
        # End
        ended = self.telephony.end_call(call_id)
        assert ended['status'] == 'ended'
        
        logger.info("Complete call lifecycle tested successfully")
    
    def test_audio_stream_during_call(self):
        """Test audio streaming during active call"""
        call_data = self.telephony.initiate_call(
            self.test_from_number,
            self.test_to_number
        )
        call_id = call_data['call_id']
        self.telephony.answer_call(call_id)
        
        # Simulate audio data
        audio_data = b'\x00' * 1600  # Simulated audio chunk
        
        result = self.telephony.send_audio_stream(call_id, audio_data)
        assert result, "Audio stream should be accepted during active call"
        
        logger.info("Audio streaming works correctly")
    
    def test_audio_stream_before_answer(self):
        """Test that audio cannot be sent before call is answered"""
        call_data = self.telephony.initiate_call(
            self.test_from_number,
            self.test_to_number
        )
        call_id = call_data['call_id']
        
        audio_data = b'\x00' * 1600
        result = self.telephony.send_audio_stream(call_id, audio_data)
        
        assert not result, "Audio should not be accepted before call is answered"
        logger.info("Audio stream correctly rejected before answer")
    
    def test_emergency_call(self):
        """Test emergency call (911) handling"""
        emergency_call = self.telephony.simulate_emergency_call(self.test_from_number)
        
        assert emergency_call['to_number'] == "911", "Should call 911"
        assert emergency_call['call_type'] == 'emergency', "Should be emergency call"
        assert emergency_call['emergency'] is True, "Should be marked as emergency"
        assert emergency_call['priority'] == 'high', "Should have high priority"
        
        logger.info("Emergency call handled correctly")
    
    def test_call_metrics(self):
        """Test call metrics collection"""
        call_data = self.telephony.initiate_call(
            self.test_from_number,
            self.test_to_number
        )
        call_id = call_data['call_id']
        
        self.telephony.answer_call(call_id)
        time.sleep(0.1)
        self.telephony.end_call(call_id)
        
        metrics = self.telephony.get_call_metrics(call_id)
        
        assert 'call_id' in metrics
        assert 'status' in metrics
        assert 'duration' in metrics
        assert metrics['duration'] > 0
        
        logger.info(f"Call metrics collected: {metrics}")
