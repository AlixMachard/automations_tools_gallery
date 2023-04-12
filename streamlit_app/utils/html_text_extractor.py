from bs4 import BeautifulSoup
import codecs
import pandas as pd


def text_extractor_from_html(html_file):
    # Empty list for storing results
    results = []

    # Define cell limit
    limit = 32767

    # Open the file using codecs
    # html = codecs.open(html_file)

    # Remove all HTML tags
    soup = BeautifulSoup(html_file)
    for script in soup(["script", "style"]):
        script.decompose()

    strips = list(soup.stripped_strings)

    # Connect all pieces of textxsinto a single string
    title = strips[0]
    preview = strips[1]
    h1_title = strips[2]

    string = ""
    for s in strips[3:]:
        string += " " + s

    # Divide the string into slices of at most 'limit' characters
    list_of_strings = ["index_file"]
    index = 0
    while index < len(string):
        end = index + limit
        list_of_strings.append(string[index:end])
        index += limit + 1

    # Attach the list of strings for 1 file to the global list 'results'
    results.append(list_of_strings)

    # Put results into a dataframe (columns)
    df = pd.DataFrame(results)
    df["title"] = title
    df["preview"] = preview
    df["h1_title"] = h1_title

    return df


# text_extractor_from_html(
#     "/home/alixmachard/workspace/dirty/streamlit_app/templates/index.html"
# )
