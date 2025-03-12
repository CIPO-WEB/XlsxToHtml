import pandas as pd

# Load the Excel file, skipping first 5 rows and selecting columns B to P
file_path = r"https://ised-isde.canada.ca/site/canadian-intellectual-property-office/sites/default/files/documents/OPIC_Brevets_Preoctrois_Hebdomadaires-CIPO_Patents_Weekly_Pre-Grants_1.xlsx"
df = pd.read_excel(file_path, skiprows=5, usecols="B:P", header=None)  # Start from row 6, column B

# ✅ Fix: Ensure "E" column is an integer before converting to a string
df.iloc[:, 4] = pd.to_numeric(df.iloc[:, 4], errors='coerce')  # Convert to numeric, NaN stays unchanged
df.iloc[:, 4] = df.iloc[:, 4].apply(lambda x: str(int(x)) if pd.notna(x) and x == int(x) else str(x))  # Remove .0

# ✅ Convert all values to strings before replacing missing values
df = df.astype(str).replace("nan", "N/A").replace("<NA>", "N/A")

# Define column indices that contain date values
date_columns = [0, 1, 2, 11]  # Update with actual indices of date columns in B:P

# ✅ Correctly format date columns using .iloc[:, col]
for col in date_columns:
    df.iloc[:, col] = pd.to_datetime(df.iloc[:, col], errors='coerce').dt.strftime('%Y-%m-%d')
    df.iloc[:, col] = df.iloc[:, col].fillna("N/A")  # Handle NaT (invalid dates)

# ✅ Replace " & " with " &amp; "
df = df.map(lambda x: x.replace(" & ", " &amp; ") if isinstance(x, str) else x)

# ✅ Wrap ONLY words containing a hyphen (-) inside <span class="nowrap">
def wrap_hyphenated_words(text):
    if isinstance(text, str) and "-" in text and text != "N/A":
        words = text.split()  # Split the cell text into words
        wrapped_words = [f'<span class="nowrap">{word}</span>' if '-' in word else word for word in words]
        return " ".join(wrapped_words)  # Join words back together
    return text  # Return unchanged if no hyphen is found

df = df.map(wrap_hyphenated_words)

# Wrap content of column J (index 8) in <span lang="fr"></span>
df.iloc[:, 8] = df.iloc[:, 8].apply(lambda x: f'<span lang="fr">{x}</span>' if x != "N/A" else x)

# Define custom headers matching the selected columns
custom_headers = [
    "Predicted Grant Date", "Final Fee Received Date", "Pre-Grant Date", 
    "Application Number", "PCT", "Applicants", "Inventors",
    "English Title", "French Title", "Classification", "Agent", 
    "Examination Requested Date", "PCT Application Number", "PCT Publication Number", "Comments"
]

# Convert the DataFrame to an HTML table without headers
html_table_rows = df.to_html(index=False, header=False, border=1, escape=False)

# Manually define the table headers in the HTML
html_table = f"""
<div class="small table-responsive">
<table class="wb-tables small dataTable no-footer table table-striped table-hover" data-wb-tables="{{&quot;lengthMenu&quot; : [10, 20, 50, 100], &quot;order&quot;: [0, &quot;asc&quot;]}}" id="dataset-filter">
    <caption class="bg-primary">Weekly Pre-Grants<br><span class="nowrap">2025-03-07</span></caption>
    <thead>
        <tr class="bg-info">
            {''.join(f'<th>{col}</th>' for col in custom_headers)}
        </tr>
    </thead>
    <tbody>
        {html_table_rows.split('<tbody>')[1]}  <!-- Retains only tbody part from Pandas html -->
</div>
"""

# Save to HTML file
output_file = "GrantTable_eng.html"
with open(output_file, "w", encoding="utf-8") as file:
    file.write(html_table)

print(f"HTML file '{output_file}' has been created successfully!")