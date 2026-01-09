"""
End-to-end captioning flow tests
Tests complete flow: Call → Audio → ASR → Caption → Display
"""
import pytest
import time
from framework.utils.telephony_client import TelephonyClient
from framework.utils.asr_client import ASRClient
from framework.utils.caption_delivery import CaptionDeliveryTester
from loguru import logger


@pytest.mark.integration
@pytest.mark.captioning_flow
class TestCaptioningFlow:
    """Test cases for end-to-end captioning flow"""
    
    def setup_method(self):
        """Setup for each test"""
        self.telephony = TelephonyClient()
        self.asr = ASRClient()
        self.delivery = CaptionDeliveryTester()
        self.test_from_number = "+15551111111"
        self.test_to_number = "+15552222222"
    
    def test_complete_captioning_flow(self):
        """Test complete flow from call to caption display"""
        # Step 1: Initiate call
        call_data = self.telephony.initiate_call(
            self.test_from_number,
            self.test_to_number
        )
        call_id = call_data['call_id']
        
        # Step 2: Answer call
        self.telephony.answer_call(call_id)
        
        # Step 3: Start ASR session
        session_id = self.asr.start_session(call_id)
        assert session_id is not None
        
        # Step 4: Process audio through ASR
        reference_text = "Hello, this is a test call with captioning."
        audio_data = b'\x00' * 8000
        asr_result = self.asr.process_audio(audio_data, reference_text)
        
        assert 'transcription' in asr_result
        
        # Step 5: Deliver caption to UI
        caption = self.delivery.deliver_caption(
            call_id,
            asr_result['transcription'],
            asr_result['timestamp']
        )
        
        assert caption['call_id'] == call_id
        assert len(caption['text']) > 0
        
        # Step 6: End call
        self.telephony.end_call(call_id)
        
        logger.info("Complete captioning flow tested successfully")
    
    def test_caption_latency_end_to_end(self):
        """Test end-to-end caption latency"""
        # Initiate call
        call_data = self.telephony.initiate_call(
            self.test_from_number,
            self.test_to_number
        )
        call_id = call_data['call_id']
        self.telephony.answer_call(call_id)
        
        # Start ASR
        self.asr.start_session(call_id)
        
        # Measure total latency
        audio_start = time.time()
        audio_data = b'\x00' * 8000
        reference_text = "Testing end-to-end latency."
        
        asr_result = self.asr.process_audio(audio_data, reference_text)
        asr_latency = asr_result['latency_ms']
        
        caption = self.delivery.deliver_caption(
            call_id,
            asr_result['transcription'],
            asr_result['timestamp']
        )
        delivery_latency = caption['delivery_latency_ms']
        
        total_latency = asr_latency + delivery_latency
        
        assert total_latency > 0, "Total latency should be positive"
        assert total_latency < 3000, "Total latency should be under 3 seconds (FCC requirement)"
        
        logger.info(f"End-to-end latency: {total_latency:.2f}ms "
                   f"(ASR: {asr_latency:.2f}ms, Delivery: {delivery_latency:.2f}ms)")
    
    def test_streaming_caption_flow(self):
        """Test streaming caption flow with multiple audio chunks"""
        # Setup
        call_data = self.telephony.initiate_call(
            self.test_from_number,
            self.test_to_number
        )
        call_id = call_data['call_id']
        self.telephony.answer_call(call_id)
        self.asr.start_session(call_id)
        
        # Process multiple audio chunks
        test_phrases = [
            "First phrase",
            "Second phrase",
            "Third phrase"
        ]
        
        captions_delivered = []
        
        for phrase in test_phrases:
            audio_data = b'\x00' * 2000
            asr_result = self.asr.process_audio(audio_data, phrase)
            
            caption = self.delivery.deliver_caption(
                call_id,
                asr_result['transcription'],
                asr_result['timestamp']
            )
            captions_delivered.append(caption)
        
        assert len(captions_delivered) == len(test_phrases)
        
        # Verify ordering
        timestamps = [c['timestamp'] for c in captions_delivered]
        is_ordered = all(timestamps[i] <= timestamps[i+1] 
                         for i in range(len(timestamps)-1))
        assert is_ordered, "Captions should be delivered in order"
        
        logger.info(f"Streaming flow: {len(captions_delivered)} captions delivered in order")
    
    def test_caption_accuracy_end_to_end(self):
        """Test caption accuracy through complete flow"""
        call_data = self.telephony.initiate_call(
            self.test_from_number,
            self.test_to_number
        )
        call_id = call_data['call_id']
        self.telephony.answer_call(call_id)
        self.asr.start_session(call_id)
        
        reference_text = "ClearCaptions provides real-time phone captioning for individuals with hearing loss."
        audio_data = b'\x00' * 10000
        
        asr_result = self.asr.process_audio(audio_data, reference_text)
        
        if 'quality' in asr_result:
            accuracy = asr_result['quality']['accuracy']
            assert accuracy >= 0.95, f"Accuracy {accuracy:.4f} should meet 95% threshold"
            
            logger.info(f"End-to-end accuracy: {accuracy:.4f}")
    
    def test_multiple_concurrent_calls(self):
        """Test handling multiple concurrent calls"""
        call_ids = []
        
        # Initiate multiple calls
        for i in range(3):
            call_data = self.telephony.initiate_call(
                f"+1555111111{i}",
                self.test_to_number
            )
            call_ids.append(call_data['call_id'])
            self.telephony.answer_call(call_data['call_id'])
        
        # Process audio for each call
        for call_id in call_ids:
            self.asr.start_session(call_id)
            audio_data = b'\x00' * 4000
            asr_result = self.asr.process_audio(audio_data, f"Test call {call_id}")
            
            caption = self.delivery.deliver_caption(
                call_id,
                asr_result['transcription']
            )
            assert caption['call_id'] == call_id
        
        # End all calls
        for call_id in call_ids:
            self.telephony.end_call(call_id)
        
        logger.info(f"Handled {len(call_ids)} concurrent calls successfully")
