import json
import datetime

from uuid import uuid4 as uuid

# Define the initial_state for the state to become the JWT cookie
state = {}
initial_state= {
        "Pi100": False,
        "SQLi": False,
        "Parameter": False,
        "Cookie": False,
        "Admin": False,
        "Level": 0,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1)  # Token expiration time
    }

# Progress levels as different hacks are completed
levels = [ "n00b", "Green Hat", "Haxor", "Pwn'r", "1337", "Champion"]

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
        <title>Pi Exam</title>
      </head>
      <body>
        <h1 style="text-align: center">Pi hacking challenge</h1>
      """

html_body = ['']

html_footer = """
        <h2 style='text-align: center'>
        <a href="/prod/login" style='text-align: center'>HOME</a></h2>
      </body>
    </html>
    """

def reset_html_body():
    global html_body
    html_body = [""]
    html_body.append("<!-- There are at least 5 different ways to show the success page.-->\n")
    html_body.append("<!-- Try the admin page for hints -->\n")

def load_form_values(form_data):
    #  values
    form_values['pi'] = "".join(form_data.get('pi', ['']))
    form_values['digits'] = int(form_data.get('digits', 100))

def load_cookie_state(cookies):
    global state

    # Split the cookies string into individual cookies
    cookie_dict = {}
    for cookie in cookies:
        name, value = cookie.split('=', 1)
        cookie_dict[name] = value

    # Use the initial state if no cookie
    cookie = cookie_dict.get('state',0)
    state = initial_state if cookie ==0 else eval(cookie)
    return

def get_current_level(): 
    global state
    grade = 0
    x = 0
    for x in state:
        if state[x] == True:
            grade += 1

    state['Level'] = grade
    return grade
    
def add_response_message( message ):
    html_body.append("<h2 style='text-align: center'>" + message + "</h2>\n")

def pi_100_digits():
    # Success by setting form value 'pi' to 100 digits 
    return form_values['pi'] == pi

def hidden_value_attack():
    # Success by reducing the hidden form value 'digits' to something less than 100
    n = form_values['digits']
    return form_values['pi'][:n] == pi[:n]

def sqli_attack():
    # Strickly a python eval injection not a  SQLi attack (no DB)
    # When this is called the form value is not pi, so pass if an injection attack
    if pi[:10] in form_values['pi']:
        # We are looking for something that is not Pi
        return False
    try:
        result = eval(pi + '==' + form_values['pi'])
    except SyntaxError:
        result = False
    return result
        
def cookie_attack():
    # Success by altering state cookie to any invalid level value
    return state['Level'] not in range(0,5)

def show_image(image):
    url = "https://raw.githubusercontent.com/kengraf/pi-exam/main/images/"
    if image == "success.png" and get_current_level() == 5:
        image = "trophy.png"
    add_response_message( "<img src='" + url + image + "' style='text-align: center;width:200px'>")
    
def lambda_handler(event, context):
    global html_body
    global html_header

    # Print the incoming event for debugging
    print("Event:", event)
    
    # Reset the global body variable, global variable values can persist between lamdba invocations
    reset_html_body()

    # Define the cookie attributes
    load_cookie_state(event.get('cookies', []))

    path = event.get('requestContext', {}).get('http', {}).get('path', '/')
    if cookie_attack():
        # state level set to invalid value
        state['Cookie'] = True
        add_response_message( "Successfully changed state cookie" )
        show_image( "success.png" )

    elif "admin" in path:
        # /admin page
        state['Admin'] = True
        url = "https://github.com/kengraf/pi-exam/blob/main/pi.py"
        add_response_message( "<a href='" + url + "'>PI exam application source</a>")
  
    elif "champion" in path:
        # /champion page
        add_response_message( "You don't advance your knowledge by faking it!" )
        show_image( "trophy.png" )
       
    elif "join" in path:
        load_form_values(event.get('queryStringParameters', {}))
        if pi_100_digits():
            # Form value is pi to 100 digits 
            state['Pi100'] = True
            add_response_message( "Yeah, you know how to google pi.<br/> Try something more leet" )
            show_image( "success.png" )
     
        elif hidden_value_attack():
            # pi by reducing the hidden form value "digits"
            state['Parameter'] = True
            add_response_message( "Successfully altered hidden form field submission" )
            show_image( "success.png" )
     
        elif sqli_attack():
            # parm is SQLi = success 0X02
            state['SQLi'] = True
            add_response_message( "Successful code injection attempt" )
            show_image( "success.png" )
    
        else:
            add_response_message( "Hack Failed" )
            show_image( "failure.png" )
    
    else:
        # show "login" page for all other paths
        show_image( "pi.png" )
        add_response_message( "Show you are worthly to join the Pi party." )
        form_page = """
            <form style="text-align: center" action="/prod/join">
            <label for="pi">Enter the first 100 digits of Pi:</label><br>
            <input type="text" id="pi" name="pi" value="" style="width:90%"><br>
            <input type="hidden" id="digits" name="digits" value="100">
            <input type="submit" value="Submit">
            </form>
            """
        add_response_message(form_page)

    add_response_message("Your current level is: " + levels[get_current_level()])
    add_response_message(str(uuid()))
    
    # Create the Set-Cookie header
    cookie_header = f"state={state}; Max-Age=3600; Path=/; Secure; HttpOnly;"

    # Create the response
    response = {
        'statusCode': 200,
        'headers': {
            'Set-Cookie': cookie_header,
            'Content-Type': 'text/html'
        },
        'body': html_header + " ".join(html_body) + html_footer
    }

    return response
