import pandas as pd

# Load the Excel file, skipping first 5 rows and selecting columns B to P
file_path = r"https://ised-isde.canada.ca/site/canadian-intellectual-property-office/sites/default/files/documents/OPIC_Brevets_Preoctrois_Hebdomadaires-CIPO_Patents_Weekly_Pre-Grants_1.xlsx"
df = pd.read_excel(file_path, skiprows=5, usecols="B:P", header=None)  # Start from row 6, column B

# ✅ Convert all values to strings before replacing missing values
df = df.astype(str).replace("nan", "s/o").replace("<NA>", "s/o")

# Define column indices that contain date values
date_columns = [0, 1, 2, 11]  # Update with actual indices of date columns in B:P

# ✅ Correctly format date columns using .iloc[:, col]
for col in date_columns:
    df.iloc[:, col] = pd.to_datetime(df.iloc[:, col], errors='coerce').dt.strftime('%Y-%m-%d')
    df.iloc[:, col] = df.iloc[:, col].fillna("s/o")  # Handle NaT (invalid dates)

# ✅ Replace " & " with " &amp; "
df = df.map(lambda x: x.replace(" & ", " &amp; ") if isinstance(x, str) else x)

# ✅ Wrap ONLY words containing a hyphen (-) inside <span class="nowrap">
def wrap_hyphenated_words(text):
    if isinstance(text, str) and "-" in text and text != "s/o":
        words = text.split()  # Split the cell text into words
        wrapped_words = [f'<span class="nowrap">{word}</span>' if '-' in word else word for word in words]
        return " ".join(wrapped_words)  # Join words back together
    return text  # Return unchanged if no hyphen is found

df = df.map(wrap_hyphenated_words)

# Wrap content of column J (index 7) in <span lang="en"></span>
df.iloc[:, 7] = df.iloc[:, 7].apply(lambda x: f'<span lang="en">{x}</span>' if x != "s/o" else x)

# Define custom headers matching the selected columns
custom_headers = [
    "Date prévue d'octroi", "Date de réception de la taxe finale", "Date de préoctroi", 
    "Numéro de demande", "PCT", "Demandeurs", "Inventeurs",
    "Titre anglais", "Titre français", "Classification", "Agent", 
    "Date de requête d'examen", "Numéro de demande PCT", "Numéro de publication PCT", "Commentaires"
]

# Convert the DataFrame to an HTML table without headers
html_table_rows = df.to_html(index=False, header=False, border=1, escape=False)

# Manually define the table headers in the HTML
html_table = f"""
<div class="small table-responsive">
<table class="wb-tables small dataTable no-footer table table-striped table-hover" data-wb-tables="{{&quot;lengthMenu&quot; : [10, 20, 50, 100], &quot;order&quot;: [0, &quot;asc&quot;]}}" id="dataset-filter">
    <caption class="bg-primary">Préoctrois Hebdomadaires<br><span class="nowrap">2025-03-07</span>
    </caption>
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
output_file = "GrantTable_fra.html"
with open(output_file, "w", encoding="utf-8") as file:
    file.write(html_table)
print(f"HTML file '{output_file}' has been created successfully!")