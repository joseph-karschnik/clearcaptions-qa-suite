"""
Emergency services (911) integration tests
Tests emergency call handling and compliance
"""
import pytest
import time
from framework.utils.telephony_client import TelephonyClient
from framework.utils.asr_client import ASRClient
from framework.utils.caption_delivery import CaptionDeliveryTester
from loguru import logger


@pytest.mark.integration
@pytest.mark.emergency
@pytest.mark.compliance
class TestEmergencyServices:
    """Test cases for emergency services (911) integration"""
    
    def setup_method(self):
        """Setup for each test"""
        self.telephony = TelephonyClient()
        self.asr = ASRClient()
        self.delivery = CaptionDeliveryTester()
        self.test_from_number = "+15551111111"
    
    def test_emergency_call_initiation(self):
        """Test emergency call (911) initiation"""
        emergency_call = self.telephony.simulate_emergency_call(self.test_from_number)
        
        assert emergency_call['to_number'] == "911", "Should call 911"
        assert emergency_call['call_type'] == 'emergency'
        assert emergency_call['emergency'] is True
        assert emergency_call['priority'] == 'high'
        
        logger.info(f"Emergency call initiated: {emergency_call['call_id']}")
    
    def test_emergency_call_priority(self):
        """Test that emergency calls have high priority"""
        emergency_call = self.telephony.simulate_emergency_call(self.test_from_number)
        call_id = emergency_call['call_id']
        
        # Answer emergency call immediately
        answered = self.telephony.answer_call(call_id)
        assert answered['status'] == 'active'
        
        # Emergency calls should be answered quickly
        time_to_answer = answered['answered_at'] - emergency_call['timestamp']
        assert time_to_answer < 2.0, "Emergency call should be answered quickly"
        
        logger.info("Emergency call priority verified")
    
    def test_emergency_call_captioning(self):
        """Test that emergency calls receive captioning"""
        emergency_call = self.telephony.simulate_emergency_call(self.test_from_number)
        call_id = emergency_call['call_id']
        self.telephony.answer_call(call_id)
        
        # Start ASR for emergency call
        session_id = self.asr.start_session(call_id)
        assert session_id is not None
        
        # Process emergency audio
        emergency_phrase = "I need help, this is an emergency."
        audio_data = b'\x00' * 8000
        asr_result = self.asr.process_audio(audio_data, emergency_phrase)
        
        # Deliver caption
        caption = self.delivery.deliver_caption(
            call_id,
            asr_result['transcription']
        )
        
        assert caption['call_id'] == call_id
        assert len(caption['text']) > 0, "Emergency call should have captions"
        
        logger.info("Emergency call captioning verified")
    
    def test_emergency_call_latency(self):
        """Test that emergency call captioning meets latency requirements"""
        emergency_call = self.telephony.simulate_emergency_call(self.test_from_number)
        call_id = emergency_call['call_id']
        self.telephony.answer_call(call_id)
        
        self.asr.start_session(call_id)
        
        # Measure caption latency for emergency
        audio_data = b'\x00' * 8000
        reference_text = "Emergency situation, need immediate assistance."
        
        asr_result = self.asr.process_audio(audio_data, reference_text)
        caption = self.delivery.deliver_caption(
            call_id,
            asr_result['transcription']
        )
        
        total_latency = asr_result['latency_ms'] + caption['delivery_latency_ms']
        
        # Emergency calls should have low latency (even stricter than normal)
        assert total_latency < 2000, \
            f"Emergency caption latency {total_latency}ms should be under 2 seconds"
        
        logger.info(f"Emergency call latency: {total_latency:.2f}ms")
    
    def test_emergency_call_accuracy(self):
        """Test emergency call caption accuracy"""
        emergency_call = self.telephony.simulate_emergency_call(self.test_from_number)
        call_id = emergency_call['call_id']
        self.telephony.answer_call(call_id)
        self.asr.start_session(call_id)
        
        # Critical emergency phrases
        critical_phrases = [
            "I need an ambulance",
            "There's a fire",
            "I need the police",
            "Medical emergency"
        ]
        
        for phrase in critical_phrases:
            audio_data = b'\x00' * 6000
            asr_result = self.asr.process_audio(audio_data, phrase)
            
            if 'quality' in asr_result:
                accuracy = asr_result['quality']['accuracy']
                # Emergency calls need high accuracy
                assert accuracy >= 0.98, \
                    f"Emergency caption accuracy {accuracy:.4f} should be at least 98%"
        
        logger.info("Emergency call accuracy verified for critical phrases")
    
    def test_emergency_call_routing(self):
        """Test that emergency calls are routed correctly"""
        emergency_call = self.telephony.simulate_emergency_call(self.test_from_number)
        
        # Verify routing information
        assert emergency_call['to_number'] == "911"
        assert emergency_call['call_type'] == 'emergency'
        
        # Emergency calls should not be blocked or delayed
        call_id = emergency_call['call_id']
        status = self.telephony.get_call_status(call_id)
        assert status['status'] in ['ringing', 'active'], \
            "Emergency call should proceed without blocking"
        
        logger.info("Emergency call routing verified")
    
    def test_emergency_call_compliance(self):
        """Test FCC compliance for emergency calls"""
        emergency_call = self.telephony.simulate_emergency_call(self.test_from_number)
        call_id = emergency_call['call_id']
        self.telephony.answer_call(call_id)
        
        # Test compliance requirements
        # 1. Captioning must be available
        self.asr.start_session(call_id)
        audio_data = b'\x00' * 8000
        asr_result = self.asr.process_audio(audio_data, "Test emergency")
        
        assert 'transcription' in asr_result, "Captioning must be available"
        
        # 2. Latency must be acceptable
        caption = self.delivery.deliver_caption(call_id, asr_result['transcription'])
        total_latency = asr_result['latency_ms'] + caption['delivery_latency_ms']
        assert total_latency < 3000, "Must meet FCC latency requirements"
        
        # 3. Accuracy must be high
        if 'quality' in asr_result:
            accuracy = asr_result['quality']['accuracy']
            assert accuracy >= 0.99, "Must meet FCC accuracy requirements (99%)"
        
        logger.info("Emergency call FCC compliance verified")
