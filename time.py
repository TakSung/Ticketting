import requests
from bs4 import BeautifulSoup

# URL of the website
url = "https://time.navyism.com/?host=ticket.interpark.com"

# Send a GET request to the website
response = requests.get(url)

# Parse the HTML content using BeautifulSoup
soup = BeautifulSoup(response.content, 'html.parser')

# Find the element containing the server time
# The specific tag and class may need adjustment based on the website structure
time_element = soup.find('span', {'id': 'time_area'})  # Example selector

# Extract and print the server time
server_time = time_element.text if time_element else "Time not found"
print("Interpark Server Time:", server_time)
