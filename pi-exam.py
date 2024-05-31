import json

request_state = 0
response_body = ''

def load_cookie_state(cookie):
    # Extract the 'Cookie' header from the request
    cookies = event['headers'].get('cookie', '')

    # Split the cookies string into individual cookies
    cookie_dict = {}
    if cookies:
        for cookie in cookies.split('; '):
            name, value = cookie.split('=', 1)
            cookie_dict[name] = value

    # Get the value of 'my_cookie'
    request_state = cookie_dict.get('state',0)
    return 0

def add_response_image( image_url ):
    return 0

def add_response_message( message ):
    response_body += message
    return 0
    
def lambda_handler(event, context):
    # Define the cookie attributes
    load_cookie_state(event['headers'].get('cookie', ''))

    # / 
    # parm is pi = "yeah you know how to google pi" page success 
    # pi by reducing digits PARMS DIGITS<100 =  success 0x01
    # parm is SQLi = success 0X02
    # AUTH==TRUE header  = success 0X04
    # state cookie delta = success 0X08
    # show "login" page
    # /admin page
    #    Direct request, return this code as HTML 0X08
    # /champion page
    # Create the Set-Cookie header
    cookie_header = f"state={state}; Max-Age=3600; Path=/; Secure; HttpOnly;"

    # Create the response
    response = {
        'statusCode': 200,
        'headers': {
            'Set-Cookie': cookie_header,
            'Content-Type': 'application/json'
        },
        'body': json.dumps({'message': 'Cookie has been set!'})
    }

    return response
