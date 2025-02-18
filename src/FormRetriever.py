# This file provides the necessary functions to retrieve the IDs and form fields
# needed to be filled out.

import requests
import json


ALL_DATA_FIELDS = "FB_PUBLIC_LOAD_DATA_"
FORM_SESSION_TYPE_ID = 8
ANY_TEXT_FIELD = "ANY TEXT!!"

# Takes a URL and performs
def get_form_response_url(url: str):
    print('LOG: Given URL: ' + url)
    ''' Convert form url to form response url '''
    response = requests.get(url, allow_redirects=True) # Necessary to retrieve correct URL, if given as shortened
    print('LOG: Unshortened URL (if necessary): ' + response.url)
    q_index = response.url.find('?')
    if(q_index > 0): # Trim the parameters at the end of the URL if they exist
        url = response.url[:q_index]  
    print('LOG: URL with parameters removed: ' + url)
    url = url.replace('/viewform', '/formResponse') 
    if not url.endswith('/formResponse'): # idk wtf this is
        if not url.endswith('/'):
            url += '/'
        url += 'formResponse'
    print('LOG: URL with replaced suffix for form submitting: ' + url)
    return url

# Extract the first valid paretheses content that comes after 'FB_PUBLIC_LOAD_DATA_'
def first_valid_parentheses_content(html: str):
    stack = []
    start_idx = -1
    for i, char in enumerate(html):
        if char == '[':
            if not stack:  # First opening parenthesis
                start_idx = i
            stack.append(char)
        elif char == ']':
            stack.pop()
            if not stack:  # First valid closing parenthesis
                return html[start_idx:i + 1]  # Extract content
    return None  # No valid parentheses found

def get_fb_public_load_data(url: str):
    """ Get form data from a Google form url """
    response = requests.get(url, timeout=10)
    if response.status_code != 200:
        print("Error! Can't get form data", response.status_code)
        return None
    
    html = response.text
    """ Extract a variable from a script tag in a HTML page """
    # print(html.find(ALL_DATA_FIELDS))
    match = first_valid_parentheses_content(html[html.find(ALL_DATA_FIELDS):])
    
    # pattern = re.compile(r'var\s' + name + r'\s=\s(.*?);')
    # pattern2 = re.compile(r'\[(?:[^()]|(?R))*\]')
    # print('hi')
    # match = pattern2.search(html)
    # print(html)
    # if not match:
    #     print("Error! Can't extract form data!!!!!!!!!!")
    #     return None
    # print(match.group(0));
    # value_str = match.group(1)
    # print(value_str)
    # return json.loads(value_str)
    # print("HELLO")
    # print(match)
    # print("GOODBYE")
    return json.loads(match)
    #return extract_script_variables(ALL_DATA_FIELDS, response.text)

def parse_form_entries(url: str, only_required = False):
    """
    In window.FB_PUBLIC_LOAD_DATA_ (as v) 
    - v[1][1] is the form entries array
    - for x in v[1][1]:
        x[0] is the entry id of the entry container
        x[1] is the entry name (*)
        x[3] is the entry type 
        x[4] is the array of entry (usually length of 1, but can be more if Grid Choice, Linear Scale)
            x[4][0] is the entry id (we only need this to make request) (*)
            x[4][1] is the array of entry value (if null then text)
                x[4][1][i][0] is the i-th entry value option (*)
            x[4][2] field required (1 if required, 0 if not) (*)
            x[4][3] name of Grid Choice, Linear Scale (in array)
    - v[1][10][6]: determine the email field if the form request email
        1: Do not collect email
        2: required checkbox, get verified email
        3: required responder input
    """
    # We should guarantee that this url is the form response url when calling this and thus 
    # This should be uneeded
    #url = get_form_response_url(url)
        
    v = get_fb_public_load_data(url)
    if not v or not v[1] or not v[1][1]:
        print("Error! Can't get form entries. Login may be required.")
        return None

    def parse_entry(entry):
        entry_name = entry[1]
        entry_type_id = entry[3]
        result = []
        for sub_entry in entry[4]:
            info = {
                "id": sub_entry[0],
                "container_name": entry_name.replace("\n", ". "),
                "type": entry_type_id,
                "required": sub_entry[2] == 1,
                "name": ' - '.join(sub_entry[3]) if (len(sub_entry) > 3 and sub_entry[3]) else None,
                "options": [(x[0] or ANY_TEXT_FIELD) for x in sub_entry[1]] if sub_entry[1] else None,
            }
            if only_required and not info['required']:
                continue
            result.append(info)
        # print('parsed Entry: ')
        #print(result)
        return result

    parsed_entries = []
    page_count = 0
    for entry in v[1][1]:
        if entry[3] == FORM_SESSION_TYPE_ID:
            page_count += 1
            continue
        parsed_entries += parse_entry(entry)

    # Collect email addresses
    if v[1][10][6] > 1:
        parsed_entries.append({
            "id": "emailAddress",
            "container_name": "Email Address",
            "type": "required",
            "required": True,
            "options": "email address",
        })
    if page_count > 0:
        parsed_entries.append({
            "id": "pageHistory",
            "container_name": "Page History",
            "type": "required",
            "required": False,
            "options": "from 0 to (number of page - 1)",
            "default_value": ','.join(map(str,range(page_count + 1)))
        })
    # print(parsed_entries)
    return parsed_entries

