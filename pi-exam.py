import json

def lambda_handler(event, context):
    # Define the cookie attributes
    cookie_value = 'my_cookie_value'
    cookie_name = 'my_cookie'
    max_age = 3600  # 1 hour in seconds
    path = '/'
    secure = True
    http_only = True

    # Create the Set-Cookie header
    set_cookie_header = f"{cookie_name}={cookie_value}; Max-Age={max_age}; Path={path};"
    if secure:
        set_cookie_header += ' Secure;'
    if http_only:
        set_cookie_header += ' HttpOnly;'

    # Create the response
    response = {
        'statusCode': 200,
        'headers': {
            'Set-Cookie': set_cookie_header,
            'Content-Type': 'application/json'
        },
        'body': json.dumps({'message': 'Cookie has been set!'})
    }

    return response
