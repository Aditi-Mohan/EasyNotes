import requests

def get_summary(text, num_of_lines):

    url = "https://textanalysis-text-summarization.p.rapidapi.com/text-summarizer-text"

    payload = "text={}&sentnum={}".format(text, str(num_of_lines))
    headers = {
        'content-type': "application/x-www-form-urlencoded",
        'x-rapidapi-key': "fbf8373238mshf30e078860ce444p121010jsn7136cdda2dbc",
        'x-rapidapi-host': "textanalysis-text-summarization.p.rapidapi.com"
        }

    response = requests.request("POST", url, data=payload, headers=headers)
    response = response.json()
    print(type(response['sentences']))
    print(response['sentences'])
    return response['sentences']