"""
Data flow tests
Tests data integrity and flow through the captioning system
"""
import pytest
import time
from framework.utils.telephony_client import TelephonyClient
from framework.utils.asr_client import ASRClient
from framework.utils.caption_delivery import CaptionDeliveryTester
from loguru import logger


@pytest.mark.integration
@pytest.mark.data_flow
class TestDataFlows:
    """Test cases for data flow validation"""
    
    def setup_method(self):
        """Setup for each test"""
        self.telephony = TelephonyClient()
        self.asr = ASRClient()
        self.delivery = CaptionDeliveryTester()
        self.test_from_number = "+15551111111"
        self.test_to_number = "+15552222222"
    
    def test_audio_to_text_flow(self):
        """Test data flow: Audio → ASR → Text"""
        call_data = self.telephony.initiate_call(
            self.test_from_number,
            self.test_to_number
        )
        call_id = call_data['call_id']
        self.telephony.answer_call(call_id)
        
        # Start ASR session
        session_id = self.asr.start_session(call_id)
        
        # Simulate audio input
        audio_data = b'\x00' * 8000
        reference_text = "Testing audio to text conversion."
        
        # Process through ASR
        asr_result = self.asr.process_audio(audio_data, reference_text)
        
        # Verify data flow
        assert 'transcription' in asr_result, "ASR should produce transcription"
        assert len(asr_result['transcription']) > 0, "Transcription should not be empty"
        assert asr_result['session_id'] == session_id, "Should maintain session ID"
        
        logger.info("Audio to text flow verified")
    
    def test_text_to_display_flow(self):
        """Test data flow: Text → Delivery → Display"""
        call_id = "test_call_123"
        transcription = "This is a test caption for display."
        
        # Deliver caption
        caption = self.delivery.deliver_caption(call_id, transcription)
        
        # Verify delivery
        assert caption['call_id'] == call_id, "Should maintain call ID"
        assert caption['text'] == transcription, "Text should be preserved"
        assert 'timestamp' in caption, "Should have timestamp"
        assert 'delivered_at' in caption, "Should have delivery timestamp"
        
        # Verify display data
        display_test = self.delivery.test_caption_display(caption)
        assert display_test['valid'], "Caption should be valid for display"
        
        logger.info("Text to display flow verified")
    
    def test_complete_data_flow(self):
        """Test complete data flow: Audio → ASR → Text → Delivery → Display"""
        # Setup call
        call_data = self.telephony.initiate_call(
            self.test_from_number,
            self.test_to_number
        )
        call_id = call_data['call_id']
        self.telephony.answer_call(call_id)
        
        # Audio capture
        audio_data = b'\x00' * 8000
        reference_text = "Complete data flow test."
        
        # ASR processing
        self.asr.start_session(call_id)
        asr_result = self.asr.process_audio(audio_data, reference_text)
        
        # Caption delivery
        caption = self.delivery.deliver_caption(
            call_id,
            asr_result['transcription'],
            asr_result['timestamp']
        )
        
        # Verify complete flow
        assert asr_result['transcription'] == caption['text'], \
            "Text should flow through unchanged"
        assert caption['call_id'] == call_id, "Call ID should be preserved"
        
        # Verify timestamps are sequential
        assert asr_result['timestamp'] <= caption['delivered_at'], \
            "Timestamps should be sequential"
        
        logger.info("Complete data flow verified")
    
    def test_data_integrity(self):
        """Test data integrity through the flow"""
        call_data = self.telephony.initiate_call(
            self.test_from_number,
            self.test_to_number
        )
        call_id = call_data['call_id']
        self.telephony.answer_call(call_id)
        
        original_text = "Testing data integrity preservation."
        audio_data = b'\x00' * 8000
        
        self.asr.start_session(call_id)
        asr_result = self.asr.process_audio(audio_data, original_text)
        
        # Verify text integrity
        if 'quality' in asr_result:
            # High accuracy means text integrity is maintained
            accuracy = asr_result['quality']['accuracy']
            assert accuracy >= 0.95, "Data integrity requires high accuracy"
        
        caption = self.delivery.deliver_caption(
            call_id,
            asr_result['transcription']
        )
        
        # Verify caption text matches ASR output
        assert caption['text'] == asr_result['transcription'], \
            "Text should be preserved through delivery"
        
        logger.info("Data integrity verified")
    
    def test_streaming_data_flow(self):
        """Test streaming data flow with multiple chunks"""
        call_data = self.telephony.initiate_call(
            self.test_from_number,
            self.test_to_number
        )
        call_id = call_data['call_id']
        self.telephony.answer_call(call_id)
        self.asr.start_session(call_id)
        
        # Multiple audio chunks
        chunks = [
            ("First part", b'\x00' * 2000),
            ("Second part", b'\x00' * 2000),
            ("Third part", b'\x00' * 2000)
        ]
        
        captions = []
        for text, audio in chunks:
            asr_result = self.asr.process_audio(audio, text)
            caption = self.delivery.deliver_caption(
                call_id,
                asr_result['transcription']
            )
            captions.append(caption)
        
        # Verify all chunks processed
        assert len(captions) == len(chunks), "All chunks should be processed"
        
        # Verify ordering
        timestamps = [c['timestamp'] for c in captions]
        is_ordered = all(timestamps[i] <= timestamps[i+1] 
                         for i in range(len(timestamps)-1))
        assert is_ordered, "Streaming data should maintain order"
        
        logger.info(f"Streaming data flow: {len(captions)} chunks processed in order")
    
    def test_concurrent_data_flows(self):
        """Test multiple concurrent data flows"""
        call_ids = []
        
        # Create multiple concurrent calls
        for i in range(3):
            call_data = self.telephony.initiate_call(
                f"+1555111111{i}",
                self.test_to_number
            )
            call_ids.append(call_data['call_id'])
            self.telephony.answer_call(call_data['call_id'])
        
        # Process data for each call
        results = {}
        for call_id in call_ids:
            self.asr.start_session(call_id)
            audio_data = b'\x00' * 4000
            asr_result = self.asr.process_audio(audio_data, f"Call {call_id}")
            
            caption = self.delivery.deliver_caption(
                call_id,
                asr_result['transcription']
            )
            
            results[call_id] = {
                'asr': asr_result,
                'caption': caption
            }
        
        # Verify all flows completed
        assert len(results) == len(call_ids), "All concurrent flows should complete"
        
        # Verify data isolation (each call has its own data)
        for call_id in call_ids:
            assert results[call_id]['caption']['call_id'] == call_id, \
                "Data should be isolated per call"
        
        logger.info(f"Concurrent data flows: {len(call_ids)} flows processed successfully")
    
    def test_data_flow_latency(self):
        """Test data flow latency at each stage"""
        call_data = self.telephony.initiate_call(
            self.test_from_number,
            self.test_to_number
        )
        call_id = call_data['call_id']
        self.telephony.answer_call(call_id)
        
        # Measure latency at each stage
        audio_start = time.time()
        
        self.asr.start_session(call_id)
        audio_data = b'\x00' * 8000
        asr_result = self.asr.process_audio(audio_data, "Latency test")
        asr_latency = asr_result['latency_ms']
        
        caption = self.delivery.deliver_caption(
            call_id,
            asr_result['transcription']
        )
        delivery_latency = caption['delivery_latency_ms']
        
        total_latency = asr_latency + delivery_latency
        
        # Log latency breakdown
        logger.info(f"Data flow latency breakdown:")
        logger.info(f"  ASR: {asr_latency:.2f}ms")
        logger.info(f"  Delivery: {delivery_latency:.2f}ms")
        logger.info(f"  Total: {total_latency:.2f}ms")
        
        assert total_latency < 3000, "Total latency should meet requirements"
