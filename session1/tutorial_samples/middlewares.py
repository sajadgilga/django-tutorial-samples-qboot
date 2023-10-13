from django.utils.deprecation import MiddlewareMixin


def FunctionLoggingMiddleware(get_response):
    print('middleware setup')

    def middleware(request):
        print(f'Before request execution: {request.user}')
        response = get_response(request)
        print(f'Response of request of user:{request.user} has been returned')
        return response

    return middleware


class LoggingMiddleware(MiddlewareMixin):
    def process_request(self, request):
        print(f'Before executing request with path {request.path}')

    def process_response(self, request, response):
        print(f'After executing request {request.path}')
        return response

    def process_view(self, request, view, view_args, view_kwargs):
        print(f'before entering view {view} {view_args} {view_kwargs}')
