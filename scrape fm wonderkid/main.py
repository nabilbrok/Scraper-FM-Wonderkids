import pandas as pd
import requests
from bs4 import BeautifulSoup
import os

# Step 1: Link Website Yang Mau discrape datanya
link = input("Masukkan link website: ")
link_website = link

# Step 2: Membuat request untuk mendapatkan konten web
response = requests.get(link_website)

# Step 3: Parsing HTML
soup = BeautifulSoup(response.text, "html.parser")

# Lists to store the data
rating = []
name = []
club = []
age = []
pos = []

# Find the table with the player data
table = soup.find("table", {"class": "w100p tablesorter"})

if table:
    # Step 4: Get all rows in the table
    rows = table.find_all("tr")

    # Step 5: Loop through each row (skip the first row if it's a header)
    for row in rows[1:]:
        cols = row.find_all("td")

        # Ensure the row has the right number of columns
        if len(cols) >= 4:
            nilai_rating = cols[0].text.strip()
            nama_pemain = cols[1].text.strip()
            age_pemain = cols[2].text.strip()
            posisi_pemain = cols[3].text.strip()
            club_pemain = cols[4].text.strip()

            # Append the data to the lists
            name.append(nama_pemain)
            club.append(club_pemain)
            age.append(age_pemain)
            pos.append(posisi_pemain)
            rating.append(nilai_rating)
else:
    print("Table not found!")

# Step 6: Convert to DataFrame
df = pd.DataFrame(
    {"Name": name,
     "Club": club,
     "Age": age,
     "Position": pos,
     "Rating": rating
     }
)

# Function to create a folder in the same directory as the script
def create_folder(folder_name):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    folder_path = os.path.join(script_dir, folder_name)

    if not os.path.exists(folder_path):
        os.makedirs(folder_path)  # Fixed: use folder_path instead of folder_name
        print(f"Folder '{folder_name}' created.")
    else:
        print(f"Folder '{folder_name}' already exists.")

    return folder_path

# Define folder and file names
folder_name = "folder_output"
base_file_name = "data_wonderkid"

# Create the output folder
folder_path = create_folder(folder_name)

# Function to generate the next available file name with an incremented number
def get_next_filename(folder, base_name, ext='.xlsx'):
    i = 1
    while True:
        filename = f"{base_name}_{i}{ext}"
        file_path = os.path.join(folder, filename)
        if not os.path.exists(file_path):
            return file_path
        i += 1

# Get the next available filename
next_file_name = get_next_filename(folder_path, base_file_name)

with pd.ExcelWriter(next_file_name, engine='openpyxl') as writer:
    df.to_excel(writer, index=False, sheet_name='Wonderkids')
    # Access the workbook and the sheet to adjust the column widths
    workbook = writer.book
    worksheet = writer.sheets['Wonderkids']

    # Adjust the column widths to fit the content
    for column in worksheet.columns:
        max_length = 0
        column_letter = column[0].column_letter  # Get the column letter
        for cell in column:
            try:
                if len(str(cell.value)) > max_length:
                    max_length = len(str(cell.value))
            except:
                pass
        adjusted_width = max_length + 2  # Add some extra space
        worksheet.column_dimensions[column_letter].width = adjusted_width

print(f"Sudah tersimpan di {next_file_name}. Terima kasih.")
