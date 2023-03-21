import json
import requests

# Add your Microsoft Account Key to a file called bing.key
def read_bing_key():
    # reads the BING API key from a file called 'bing.key
    # returns a string which is either None, i.e. no key found, or with a key.
    bing_api_key = None
    try:
        with open('bing.key','r') as f:
            bing_api_key = f.readline().strip()
    except:
        try:
            with open('../bing.key') as f:
                bing_api_key = f.readline().strip()
        except:
            raise IOError('bing.key file not found')
    
    if not bing_api_key:
        raise KeyError('Bing key not found')
    
    return bing_api_key

def run_query(search_terms):
    bing_key = read_bing_key()
    search_url = "https://api.bing.microsoft.com/v7.0/search"
    headers ={'Ocp-Apim-Subscription-Key': bing_key}
    params = {'q': search_terms, 'textDecorations':True, 'textFormat': 'HTML'}
    
    # Issue the request, given the details above.
    response = requests.get(search_url, headers=headers, params=params)
    response.raise_for_status()
    search_results = response.json()
    
    # With the response now in play, build up a Python list
    results = []
    for result in search_results['webPages']['value']:
        # Append a dictionary containing the title, link and summary to results
        results.append({
            'title': result['name'],
            'link': result['url'],
        })
    return results

def main():
    query = input("Please enter your query: ")
    results = run_query(query)
    for result in results:
        print(result['title'], result['link'], result['summary'])
    
if __name__ == '__main__':
    main()