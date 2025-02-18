# example
import requests
import FormRetriever

eric_values = {
    "name": "Eric Reinke",
    "playWith": "Kaly Long",
}

kaly_values = {
    "name": "Kaly Long",
    "playWith": "Eric Reinke",
}

# Takes in a list of parsed form entries and returns a dictionary suitable for submitting via post request
def fill_form(form_entries: list, preset: dict = None):
    
    value = {}
    print('\n====================\nForm responses.  Sanity check this\n====================')
    for entry in form_entries:
        entry_key = "entry." + str(entry['id'])

        #The following code lazily selects the first option for multiple choice questions.
        #This can easily be made better
        if 'which gym' in entry['container_name'].lower():
            value[entry_key] = entry['options'][0]
            print(entry['container_name'] + ': ' + value[entry_key] +"\n")
        elif 'play with' in entry['container_name'].lower():
            value[entry_key] = ' ' if preset == None else preset['playWith']
            print(entry['container_name'] + ': ' + value[entry_key]+"\n")
        elif 'waitlist' in entry['container_name'].lower() or 'wailist' in entry['container_name'].lower(): # BRUH why is there a permanent typo in the Tuesday form
            value[entry_key] = entry['options'][0]
            print(entry['container_name'] + ': ' + value[entry_key]+"\n")
        elif 'waiver' in entry['container_name'].lower():
            value[entry_key] = entry['options'][0]
            print(entry['container_name'] + ': ' + value[entry_key]+"\n")
        elif 'payment' in entry['container_name'].lower():
            value[entry_key] = entry['options'][0]
            print(entry['container_name'] + ': ' + value[entry_key]+"\n")
        elif 'full name' in entry['container_name'].lower():
            value[entry_key] = 'Eric Reinke' if preset == None else preset['name']
            print(entry['container_name'] + ': ' + value[entry_key]+"\n")
        else:
            value[entry_key] = ''
            if entry['required']:
                if entry['options']:
                    print('!!NO VALUE FOR REQUIRED QUESTION: ' + entry['container_name'] +'.  AUTO FILLING WITH FIRST OPTION: ' + entry['options'][0])
                    value[entry_key] = entry['options'][0]
                else:
                    print('!!! NO VALUE FOR REQUIRED QUESTION: ' + entry['container_name'] + '.  AUTO FILLING WITH NOTHING')
    print('====================\n')

    return value


# Given a 'formResponse' URL and a dictionary containing entry numbers and 
# their values, submit the form.
def submit(url, data):
    print(url)
    print(data)
    try:
        response = requests.post(url, data = data)
        print("Submitted successfully!")
        print(response.status_code)
    except Exception as e:
        print(e)
        print("Error!")

def complete_form(url):
    # get_form_response_url is being called twice.  Once here and then once in FormRetriever.parse_form_entries.
    # FormFiller.submit() needs the formResponse URL, and so does FormRetriever.parse_form_entries().
    # it may be confusing to remove the call from parse_form_entries, so I'm leaving it there.
    # To remove it would mean trusting that we always pass a checked URL there.
    # If we had to fix this, we would do the latter; require a valid URL be passed to parse_form_entries.
    checked_url = FormRetriever.get_form_response_url(url) # this is being called twice
    form_entries = FormRetriever.parse_form_entries(checked_url)
    
    submit(checked_url, fill_form(form_entries, eric_values))
    #submit(checked_url, fill_form(form_entries, kaly_values))