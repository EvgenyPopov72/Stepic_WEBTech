import urlparse


def app(environ, start_response):
    status = '200 OK'
    response_headers = [('Content-type', 'text/plain')]
    start_response(status, response_headers)
    list_query = urlparse.parse_qs(environ["QUERY_STRING"], keep_blank_values=True)
    body = ''
    for key, values in list_query.items():
        for value in values:
            # print '<' + key + '=' + str(value) + '>'
            body = body + key + '=' + value + '\n'
    return [body]
