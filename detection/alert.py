from django.http import HttpResponse
from django.http.response import StreamingHttpResponse
from .camera import que

def alertstream(request):
    def event_stream():
        while True:
            data = ''
            if not que.empty():
                data = que.get()
            yield 'data: %s\n\n' % data
    return StreamingHttpResponse(event_stream(), content_type='text/event-stream')

