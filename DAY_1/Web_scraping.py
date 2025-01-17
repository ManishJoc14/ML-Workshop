from bs4 import BeautifulSoup
import pandas as pd
import requests

# URL to fetch
url = "https://en.wikipedia.org/wiki/Nepal"

# Send a GET request to the URL
response = requests.get(url)

# Parse the HTML content of the page
soup = BeautifulSoup(response.text, "html.parser")

# Check if the page was fetched successfully
if response.status_code == 200:
    print("Page fetched successfully!")
else:
    print(f"Failed to fetch page: {response.status_code}")

# Print the entire HTML of the page
print(soup)

# Find and print the first <h1> tag``
header = soup.find("h1")
print(header.text.strip())

# Find and print all <p> tags
all_para = soup.find_all("p")
for para in all_para:
    print(para.text.strip())

# Find the desired table with class "wikitable sortable"
scrap_table = soup.find("table", class_="wikitable sortable")

# ---------------------- Converting List into Dataframes --------------------- #

# Example data to demonstrate how data is appended to the dataframe
header_test = [["header1", "header2", "header3"]]
content_test = [
    ["content1", "content2", "content3"],
    ["content1", "content2", "content3"],
]

# Construct a dataframe from test headers and content
df_test = pd.DataFrame(content_test, columns=header_test)


# ----------- Step 1 : Fetch and convert headers to required format ---------- #
# Fetch all the headers of the table
header = scrap_table.find_all("th")


# Convert the headers into a list
# header_list = []
# for header_data in header:
#     header_list.append(header_data.text.strip())
header_list = map(lambda header_data: header_data.text.strip(), header)

# Remove unwanted headers from the list (keeping only the first 9 headers)
header_list_data = []
upto = 9
i = 0

for header_item in header_list:
    header_list_data.append(header_item)
    i += 1
    if i == upto:
        break


# ------------- Step 2 : Find and convert rows to required format ------------ #

# Find all the rows of the table
rows_data = scrap_table.find_all("tr")

# Append the content of each row into a list
all_rows_data = []
for row in rows_data:
    # find all td inside row
    row_data_elements = row.find_all("td")

    individual_row_data = []
    for data in row_data_elements:
        individual_row_data.append(data.text.strip())

    all_rows_data.append(individual_row_data)
    
# ----------- Step 3 : Create a dataframe from content and headers ----------- #
df = pd.DataFrame(all_rows_data, columns=header_list_data)


# --------------------- Save the dataframe to a CSV file --------------------- #
df.to_csv("scrapped_data.csv", index=False)
