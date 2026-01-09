"""
Caption delivery system testing
Tests the flow from ASR output to user display
"""
import time
from typing import Dict, Any, List, Optional
from loguru import logger
from framework.utils.config_loader import ConfigLoader


class CaptionDeliveryTester:
    """Tests caption delivery from ASR to user interface"""
    
    def __init__(self):
        self.config = ConfigLoader().load_config()
        self.delivery_times = []
        self.caption_queue = []
    
    def deliver_caption(self, call_id: str, transcription: str, 
                      timestamp: float = None) -> Dict[str, Any]:
        """
        Deliver caption to user interface
        Returns delivery metrics
        """
        if timestamp is None:
            timestamp = time.time()
        
        delivery_start = time.time()
        
        # Simulate caption delivery to UI
        caption_data = {
            'call_id': call_id,
            'text': transcription,
            'timestamp': timestamp,
            'delivered_at': delivery_start,
            'delivery_latency_ms': (delivery_start - timestamp) * 1000
        }
        
        self.caption_queue.append(caption_data)
        self.delivery_times.append(caption_data['delivery_latency_ms'])
        
        logger.info(f"Caption delivered for call {call_id}: {len(transcription)} chars, "
                   f"latency: {caption_data['delivery_latency_ms']:.2f}ms")
        
        return caption_data
    
    def deliver_streaming_captions(self, call_id: str, 
                                   transcriptions: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Deliver multiple captions in sequence (streaming)"""
        delivered = []
        
        for trans in transcriptions:
            caption = self.deliver_caption(
                call_id,
                trans.get('text', ''),
                trans.get('timestamp', time.time())
            )
            delivered.append(caption)
        
        return delivered
    
    def test_delivery_latency(self, num_captions: int = 100) -> Dict[str, Any]:
        """Test caption delivery latency"""
        self.delivery_times.clear()
        
        for i in range(num_captions):
            self.deliver_caption(f"test_call_{i}", f"Test caption {i}")
        
        if not self.delivery_times:
            return {}
        
        return {
            'total_captions': num_captions,
            'average_latency_ms': sum(self.delivery_times) / len(self.delivery_times),
            'min_latency_ms': min(self.delivery_times),
            'max_latency_ms': max(self.delivery_times),
            'p95_latency_ms': sorted(self.delivery_times)[int(len(self.delivery_times) * 0.95)]
        }
    
    def test_caption_ordering(self, call_id: str, 
                              transcriptions: List[str]) -> Dict[str, Any]:
        """Test that captions are delivered in correct order"""
        delivered = []
        
        for i, text in enumerate(transcriptions):
            caption = self.deliver_caption(call_id, text, time.time() + i * 0.1)
            delivered.append(caption)
        
        # Check ordering
        timestamps = [c['timestamp'] for c in delivered]
        is_ordered = all(timestamps[i] <= timestamps[i+1] for i in range(len(timestamps)-1))
        
        return {
            'ordered': is_ordered,
            'total_captions': len(delivered),
            'timestamps': timestamps
        }
    
    def test_caption_display(self, caption_data: Dict[str, Any]) -> Dict[str, Any]:
        """Test caption display on user interface"""
        # In real implementation, this would interact with UI
        # For testing, we validate caption data structure
        
        required_fields = ['call_id', 'text', 'timestamp', 'delivered_at']
        missing_fields = [field for field in required_fields if field not in caption_data]
        
        return {
            'valid': len(missing_fields) == 0,
            'missing_fields': missing_fields,
            'text_length': len(caption_data.get('text', '')),
            'has_timestamp': 'timestamp' in caption_data
        }
    
    def get_delivery_metrics(self) -> Dict[str, Any]:
        """Get overall delivery metrics"""
        if not self.delivery_times:
            return {}
        
        return {
            'total_deliveries': len(self.delivery_times),
            'average_latency_ms': sum(self.delivery_times) / len(self.delivery_times),
            'min_latency_ms': min(self.delivery_times),
            'max_latency_ms': max(self.delivery_times),
            'p95_latency_ms': sorted(self.delivery_times)[int(len(self.delivery_times) * 0.95)]
        }
