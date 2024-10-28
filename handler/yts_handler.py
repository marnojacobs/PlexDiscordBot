import requests

base_url = "https://yts.mx/api/v2"

def get_movie_details(title: str, year: int, quality: str = "1080p"):
    """
    Fetches the details of a movie from YTS based on title, release year, and preferred quality.
    
    """
    endpoint = f"{base_url}/list_movies.json"

    params = {
        'query_term': title,
        'year': year,
        'limit': 1
    }
    
    try:
        response = requests.get(endpoint, params=params)
        response.raise_for_status()

        data = response.json()
        
        if data['data']['movie_count'] == 0:
            return f"No results found for '{title}' ({year})."
        
        movie = data['data']['movies'][0]
        movie_details = {
            'Title': movie['title'],
            'Year': movie['year'],
            'Rating': movie['rating'],
            'Genres': movie['genres'],
            'Summary': movie['summary'],
            'Language': movie['language'],
            'Runtime': movie['runtime'],
            'Cover Image': movie['large_cover_image']
        }
        
        preferred_torrent = next((torrent for torrent in movie['torrents'] if torrent['quality'] == quality), None)
        
        if preferred_torrent:
            movie_details['Preferred Torrent Link'] = preferred_torrent['url']
            movie_details['Torrent Quality'] = preferred_torrent['quality']
            movie_details['Size'] = preferred_torrent['size']
        else:
            movie_details['Preferred Torrent Link'] = f"No torrent found for {quality} quality."
        
        return movie_details
    
    except requests.exceptions.RequestException as e:
        return f"An error occurred: {e}"