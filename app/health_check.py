import time
from typing import Dict, Any
from datetime import datetime, timedelta
import psutil
import json

class HealthMonitor:
    def __init__(self):
        self.metrics = {
            'memory_usage': [],
            'api_latency': [],
            'request_count': 0,
            'errors': [],
            'last_memory_optimization': None
        }
        
        self.thresholds = {
            'memory_warning': 85.0,  # percentage
            'memory_critical': 95.0,
            'api_latency_warning': 2.0,  # seconds
            'api_latency_critical': 5.0,
            'error_rate_warning': 0.1,  # 10% error rate
            'error_rate_critical': 0.2
        }

    async def check_health(self) -> Dict[str, Any]:
        """Perform comprehensive health check"""
        return {
            'status': self._get_overall_status(),
            'memory': self._check_memory(),
            'api': self._check_api_health(),
            'system': self._check_system_health()
        }

    def _get_overall_status(self) -> str:
        """Calculate overall system status"""
        memory_usage = psutil.virtual_memory().percent
        error_rate = self._calculate_error_rate()
        
        if (memory_usage > self.thresholds['memory_critical'] or 
            error_rate > self.thresholds['error_rate_critical']):
            return 'critical'
        elif (memory_usage > self.thresholds['memory_warning'] or 
              error_rate > self.thresholds['error_rate_warning']):
            return 'warning'
        return 'healthy'

    def _check_memory(self) -> Dict[str, Any]:
        """Check memory usage and optimization status"""
        memory = psutil.virtual_memory()
        needs_optimization = (
            not self.metrics['last_memory_optimization'] or 
            datetime.now() - self.metrics['last_memory_optimization'] > timedelta(days=1)
        )
        
        return {
            'usage_percent': memory.percent,
            'available_mb': memory.available / (1024 * 1024),
            'needs_optimization': needs_optimization,
            'status': self._get_memory_status(memory.percent)
        }

    def _check_api_health(self) -> Dict[str, Any]:
        """Check API health metrics"""
        avg_latency = (
            sum(self.metrics['api_latency'][-100:]) / len(self.metrics['api_latency'][-100:])
            if self.metrics['api_latency'] else 0
        )
        
        return {
            'average_latency': avg_latency,
            'request_count': self.metrics['request_count'],
            'error_rate': self._calculate_error_rate(),
            'status': self._get_api_status(avg_latency)
        }

    def _check_system_health(self) -> Dict[str, Any]:
        """Check overall system health"""
        cpu_usage = psutil.cpu_percent(interval=1)
        disk_usage = psutil.disk_usage('/').percent
        
        return {
            'cpu_usage': cpu_usage,
            'disk_usage': disk_usage,
            'uptime': self._get_uptime(),
            'status': self._get_system_status(cpu_usage, disk_usage)
        }

    def _calculate_error_rate(self) -> float:
        """Calculate error rate from recent requests"""
        recent_errors = len([e for e in self.metrics['errors'] 
                           if datetime.now() - e['timestamp'] < timedelta(hours=1)])
        if self.metrics['request_count'] == 0:
            return 0.0
        return recent_errors / self.metrics['request_count']

    def _get_memory_status(self, usage: float) -> str:
        """Determine memory status based on usage"""
        if usage > self.thresholds['memory_critical']:
            return 'critical'
        elif usage > self.thresholds['memory_warning']:
            return 'warning'
        return 'healthy'

    def _get_api_status(self, latency: float) -> str:
        """Determine API status based on latency"""
        if latency > self.thresholds['api_latency_critical']:
            return 'critical'
        elif latency > self.thresholds['api_latency_warning']:
            return 'warning'
        return 'healthy'

    def _get_system_status(self, cpu_usage: float, disk_usage: float) -> str:
        """Determine system status based on CPU and disk usage"""
        if cpu_usage > 90 or disk_usage > 90:
            return 'critical'
        elif cpu_usage > 75 or disk_usage > 75:
            return 'warning'
        return 'healthy'

    def _get_uptime(self) -> str:
        """Get system uptime"""
        uptime = time.time() - psutil.boot_time()
        days = int(uptime // (24 * 3600))
        hours = int((uptime % (24 * 3600)) // 3600)
        return f"{days}d {hours}h"

    def record_request(self, latency: float, error: bool = False, error_details: str = None):
        """Record API request metrics"""
        self.metrics['request_count'] += 1
        self.metrics['api_latency'].append(latency)
        
        # Keep only last 1000 latency measurements
        if len(self.metrics['api_latency']) > 1000:
            self.metrics['api_latency'] = self.metrics['api_latency'][-1000:]
            
        if error:
            self.metrics['errors'].append({
                'timestamp': datetime.now(),
                'details': error_details
            })
            # Keep only last 1000 errors
            if len(self.metrics['errors']) > 1000:
                self.metrics['errors'] = self.metrics['errors'][-1000:]

    def record_memory_optimization(self):
        """Record memory optimization event"""
        self.metrics['last_memory_optimization'] = datetime.now()
