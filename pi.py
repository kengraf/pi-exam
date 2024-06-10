import json
import datetime
import urllib.parse

# Define the initial state for the JWT cookie
state = {
    "Pi100": False,
    "SQLi": False,
    "Parameter": False,
    "Cookie": False,
    "Admin": False,
    "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1)  # Token expiration time
}

form_values = {
    "pi": "",
    "digits": 100
}

pi = "3.141592653589793238462643383279502884197169399375105820974944592307816406286208998628034825342117067"

html_header = """
    <!doctype html>
    <html lang="en">
      <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
        <title>Dynamic HTML with Flask</title>
      </head>
      <body>
        <h1>Pi hacking challenge</h1>
      """

html_body = ['<!-- there ae at least 5 different ways to show the successful login page -->\n']
html_footer = """
      </body>
    </html>
    """
    
def set_state():
    # Secret key to sign the JWT
    secret = "your_secret_key"

    # Generate the JWT
    token = json.dumps(state)
    
    return token

def load_cookie_state(cookies):
    global state
    # Split the cookies string into individual cookies
    cookie_dict = {}
    if cookies:
        for cookie in cookies.split('; '):
            name, value = cookie.split('=', 1)
            cookie_dict[name] = value

    # Use cookie state if it exists
    state = cookie_dict.get('state',state)
    return

def show_current_grade(): 
    grade_levels = [ "Anon", "n00b", "Green Hat", "Haxor", "Pwn'r", "133t"]
    grade = 0
    if x in state:
        if state[x] == True:
            grade += 1
    add_response_message("Your current level is: " + grade_levels[grade])
    return grade_levels[grade]
    
def add_response_image( image_url ):
    return 0

def add_response_message( message ):
    html_body.append("<h2>" + message + "</h2\n")

def load_from_values(body):
    # Handle base64 encoded payloads (Common for API Gateway)
    if event.get('isBase64Encoded', False):
        body = base64.b64decode(body).decode('utf-8')
    
    # Parse the form data
    form_data = urllib.parse.parse_qs(body)
    
    # Extract specific values
    form_values['pi'] = form_data.get('pi', [''])[0]
    form_values['digits'] = int(form_data.get('digits', [''])[0])

def pi_100 digits():
    # Form value is pi to 100 digits 
    add_response_message( "Yeah you know how to google pi.  Try something leet" )

def hidden_value_attack():
    # pi by reducing the hidden form value "digits"
    add_response_message( "parms not 100" )

def sqli_attack():
    # parm is SQLi = success 0X02
    add_response_message( "sqli found" )

def cookie_attack():
    # state cookie delta = success 0X08
    add_response_message( "cookie changed" )

def leet_level():
    #    Direct request, return this code as HTML 0X08
    # /champion page
    add_response_message( "tbd champion page" )

def add_success_check():
    url = "https://raw.githubusercontent.com/kengraf/pi-exam/main/images/success.png"
    add_response_message( "<a href='" + url + "'>PI exam application source</a>")
    
def lambda_handler(event, context):
    response_body = ''
    
    # Print the incoming event for debugging
    print("Event:", event)
    
    # Define the cookie attributes
    load_cookie_state(event['headers'].get('cookie', ''))
    load_form_values(event.get('body', ''))

    path = event.get('requestContext', {}).get('http', {}).get('path', '/')
    if path.endswith("admin"):
        # /admin page
        url = "https://github.com/kengraf/pi-exam/blob/main/pi.py"
        add_response_message( "<a href='" + url + "'>PI exam application source</a>")
        state['Admin'] = True
  
    elif pi_100 digits():
        # Form value is pi to 100 digits 
        add_response_message( "Yeah you know how to google pi.  Try something leet" )
        add_success_check()
        state{'Pi100'] = True
 
    elif hidden_value_attack():
        # pi by reducing the hidden form value "digits"
        add_response_message( "parms not 100" )
        add_success_check()
        state{'Parameter'] = True
 
    elif sqli_attack():
        # parm is SQLi = success 0X02
        add_response_message( "sqli found" )
        add_success_check()
        state{'SQLi'] = True

    elif cookie_attack():
        # state cookie delta = success 0X08
        add_response_message( "cookie changed" )
         add_success_check()
        state{'Cookie'] = True

    elif leet_level():
        #    Direct request, return this code as HTML 0X08
        # /champion page
        add_response_message( "tbd champion page" )
        add_success_check()
        state{'pi'] = True

    else:
        # show "login" page
        add_response_message( "Show you are worthly to join our PI party." )
        form_page = """
            <form action="/">
            <label for="pi">100 digits of PI:</label><br>
            <input type="text" id="pi" name="pi" value=""><br>
            <input type="hidden" id="digits" name="digits" value="100">
            <input type="submit" value="Submit">
            </form>
            """


    show_current_grade()
    
    # Create the Set-Cookie header
    cookie_header = f"state={state}; Max-Age=3600; Path=/; Secure; HttpOnly;"

    # Create the response
    response = {
        'statusCode': 200,
        'headers': {
            'Set-Cookie': cookie_header,
            'Content-Type': 'text/html'
        },
#        'body': json.dumps({'message': 'Cookie has been set!'})

        'body': html_header + " ".join(html_body) + html_footer
    }

    return response
