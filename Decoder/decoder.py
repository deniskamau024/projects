import requests
from bs4 import BeautifulSoup

def decode_secret_message(URL):
  """Retrieves and parses data from a publishesed Google Doc URL containing a table of characters and
  coordinates, and prints a decoded 2D graphic grid.
  """
  try:
      # Fetch published Google Doc HTML content
      response = requests.get(URL)
      response.raise_for_status()

      # Parse the HTML to extract the table data
      soup = BeautifulSoup(response.text,'html.parser')
      table = soup.find('table')
      if not table:
          print("Error could not find a table in the provided document URL.")
          return

      rows = table.find_all('tr')
      
      # Dictionary to map (x,y) coordinates to characters
      data_points = {}
      max_x = 0
      max_y = 0

      # Iterate over rows, skipping the header row
      for row in rows[1:]:
          cols = row.find_all('td')
          if len(cols) != 3:
              continue

          # Extract content from each cell and strip whitespace/special spacing characters
          x_text = cols[0].get_text().strip()
          char = cols[1].get_text()
          y_text = cols[2].get_text().strip()

          try:
              x = int(x_text)
              y = int(y_text)

              # store the point and track grid boundaries
              data_points[(x,y)] = char
              if x > max_x:
                  max_x = x

              if y > max_y:
                  max_y = y
          except ValueError:
          # skip any row that does not contain valid integers for coordinates
            continue

      # print the grid starting from max_y down to 0 (since y increases upwards)
      for y in range(max_y,-1,-1):
          row_chars = []
          for x in range(max_x + 1):
              # Use space character if no character is defined in coordinates
              row_chars.append(data_points.get((x,y), ' '))
          print("".join(row_chars))

  except requests.exceptions.RequestException as e:
      print(f"Error fetching data from the URL: {e}")


decode_secret_message("https://docs.google.com/document/d/e/2PACX-1vSvM5gDlNvt7npYHhp_XfsJvuntUhq184By5xO_pA4b_gCWeXb6dM6ZxwN8rE6S4ghUsCj2VKR21oEP/pub")