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
    response_body += "<p>" + message + "</p>
    return 0
    
def lambda_handler(event, context):
    # Define the cookie attributes
    load_cookie_state(event['headers'].get('cookie', ''))

    # / 
    # parm is pi =  page success 
    add_response_message( "yeah you know how to google pi" )
    # pi by reducing digits PARMS DIGITS<100 =  success 0x01
    add_response_message( "parms not 100" )
    # parm is SQLi = success 0X02
    add_response_message( "sqli found" )
    # AUTH==TRUE header  = success 0X04
    add_response_message( "auth header" )
    # state cookie delta = success 0X08
    add_response_message( "cookie changed" )
    # show "login" page
    add_response_message( "show initial login form" )
    # /admin page
    add_response_message( "tbd admin page" )
    #    Direct request, return this code as HTML 0X08
    # /champion page
    add_response_message( "tbd champion page" )
    # Create the Set-Cookie header
    cookie_header = f"state={state}; Max-Age=3600; Path=/; Secure; HttpOnly;"

    # Create the response
    response = {
        'statusCode': 200,
        'headers': {
            'Set-Cookie': cookie_header,
            'Content-Type': 'application/json'
        },
#        'body': json.dumps({'message': 'Cookie has been set!'})
        'body': response_body
    }

    return response
