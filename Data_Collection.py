import requests
import json
import time

bearer_token = "" # Please use you own token for the X API.
search_url = "https://api.twitter.com/2/tweets/search/all"
file_number = 0

# Please use your own parameters for query. Below is the parameters we use for collecting tweets related to Hurricane Harvey.
query_params = {'query': '-is:retweet lang:en (#Harvey OR #Harvey2017 OR #HarveyStorm OR #HoustonFlood OR "Houston Flood" OR #HoustonFlooding OR "Houston Flooding" OR #HoustonFloods OR "Houston Floods" OR #HurricaneHarvey OR "Hurricane Harvey" OR "Texas Flood" OR "Texas Floods" OR "Texas Flooding") (street OR st OR st. OR avenue OR ave OR ave. OR road OR rd OR rd. OR lane OR ln OR court OR hill OR square OR park OR alley OR hall OR bayou OR river OR stream OR creek OR brook OR bridge OR boulevard OR bld OR blvd OR blvd. OR overpass OR interstate OR highway OR expressway OR freeway OR tollway OR exit OR parkway OR route OR church OR school OR center OR SH-99 OR SH-146 OR SH-225 OR SH-249 OR SH-288 OR "SH 99" OR "SH 146" OR "SH 225" OR "SH 249" OR "SH 288" OR TX-99 OR TX-146 OR TX-225 OR TX-249 OR TX-288 OR "TX 99" OR "TX 146" OR "TX 225" OR "TX 249" OR "TX 288" OR I-10 OR I-45 OR I-69 OR I-610 OR "US 59" OR "US 90" OR "US 290")',
                'max_results': 500,
                'start_time': '2017-08-18T00:00:00Z',
                'end_time': '2017-09-22T00:00:00Z',
                'tweet.fields': 'created_at,author_id,lang,public_metrics',
                'expansions': 'author_id,geo.place_id'}


# Add bearer token authorization and user agent headers to the request
def bearer_oauth(r):
    r.headers["Authorization"] = f"Bearer {bearer_token}"
    r.headers["User-Agent"] = "v2FullArchiveSearchPython"
    return r


# Send a GET request to the X API endpoint and return the JSON response
def connect_to_endpoint(url, params):
    response = requests.request("GET", url, auth=bearer_oauth, params=params)
    print(response.status_code)
    if response.status_code != 200:
        raise Exception(response.status_code, response.text)
    return response.json()


# Request tweets from the API, save the response to a file, and return pagination info
def request_tweet():
    json_response = connect_to_endpoint(search_url, query_params)
    formatted_json = json.dumps(json_response, indent=4, sort_keys=True)
    next_page = None
    number_current_page = None
    formatted_json_dict = json.loads(formatted_json)
    if 'meta' in formatted_json_dict and 'next_token' in formatted_json_dict['meta']:
        next_page = formatted_json_dict['meta']['next_token']

    if 'meta' in formatted_json_dict and 'result_count' in formatted_json_dict['meta']:
        number_current_page = formatted_json_dict['meta']['result_count']

    global file_number
    file_number = file_number + 1
    with open("Houston_Hurricane_Harvey_2017_" + str(file_number) + '.json', 'w') as file:
        file.write(formatted_json)

    return next_page, number_current_page


def main():
    num_tweets_total = 0
    start_time = time.time()
    max_number = 300000 # Maximum number of tweets to collect for each disaster

    while num_tweets_total < max_number:
        next_token, number_current_page = request_tweet()
        if next_token is not None:
            query_params['pagination_token'] = next_token
        if number_current_page is not None:
            num_tweets_total += number_current_page
            print(num_tweets_total)

        if next_token is None:
            break

        time.sleep(3) # Time interval set to comply with X API rate limits

    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Elapsed time: {elapsed_time} seconds")


if __name__ == "__main__":
    main()