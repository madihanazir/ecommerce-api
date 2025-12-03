import json
import time
from django.utils.deprecation import MiddlewareMixin
from django.http import JsonResponse

class ResponseWrapperMiddleware(MiddlewareMixin):
    def process_response(self, request, response):
       
        if request.path.startswith('/api/v1/'):
            
            # Skip for(auth, docs)
            if any(path in request.path for path in ['/docs/', '/schema/', '/admin/']):
                return response
            
            # Handle JSON responses
            if hasattr(response, 'data'):
                # DRF Response
                original_data = response.data
                status = response.status_code
            elif isinstance(response, JsonResponse):
                # Django JsonResponse
                original_data = json.loads(response.content)
                status = response.status_code
            else:
                return response
            
            # Build wrapped response
            is_success = 200 <= status < 300
            
            wrapped_data = {
                "success": is_success,
                "data": original_data if is_success else None,
                "error": None if is_success else original_data,
                "meta": {
                    "timestamp": time.time(),
                    "status_code": status
                }
            }
            
            # Handle pagination
            if isinstance(original_data, dict) and 'results' in original_data:
                wrapped_data['data'] = original_data['results']
                wrapped_data['meta'].update({
                    'count': original_data.get('count', len(original_data['results'])),
                    'next': original_data.get('next'),
                    'previous': original_data.get('previous')
                })
            
            response.data = wrapped_data
            response._is_rendered = False
            response.render()
        
        return response