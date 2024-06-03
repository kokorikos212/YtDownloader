from youtubesearchpython import VideosSearch

def search_youtube(query, max_results=5):
    """
    Searches YouTube for the given query and returns a list of video URLs.

    Parameters:
    query (str): The search query (song name, playlist, or band).
    max_results (int): The maximum number of results to return.

    Returns:
    list: A list of YouTube video URLs.
    """
    videos_search = VideosSearch(query, limit=max_results)
    results = videos_search.result()
    video_urls = [video['link'] for video in results['result']]
    return video_urls

def read_queries_from_file(file_path):
    """
    Reads search queries from a text file.

    Parameters:
    file_path (str): The path to the text file containing search queries.

    Returns:
    list: A list of search queries.
    """
    with open(file_path, 'r') as file:
        queries = [line.strip() for line in file]
    return queries

def save_links_to_file(links, output_file):
    """
    Saves a list of YouTube video URLs to a text file.

    Parameters:
    links (list): A list of YouTube video URLs.
    output_file (str): The path to the output text file.
    """
    with open(output_file, 'w') as file:
        for link in links:
            file.write(f"{link}\n")

def main(input_file, output_file):
    """
    Main function to read search queries from a file, search YouTube, and save the results to a file.

    Parameters:
    input_file (str): The path to the input text file containing search queries.
    output_file (str): The path to the output text file to save video URLs.
    """
    queries = read_queries_from_file(input_file)
    all_links = []
    for query in queries:
        links = search_youtube(query)
        all_links.extend(links)
    save_links_to_file(all_links, output_file)
    print(f"Saved {len(all_links)} links to {output_file}")

if __name__ == "__main__":
    input_file_path = input("Enter the path to the input text file: ")
    output_file_path = input("Enter the path to the output text file: ")
    main(input_file_path, output_file_path)
