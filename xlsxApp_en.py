import streamlit as st
import pandas as pd
import io
from datetime import datetime

st.set_page_config(page_title="Pre-Grant Excel to HTML")
st.title("Weekly Patent Pre-Grant Excel to HTML Table")

#####
# 1. File uploader
#####
uploaded_file = st.file_uploader(
    "Upload your Excel file (skip first 5 rows, columns B:P)", type=["xlsx"]
)

html_table = None  # Initialize

if uploaded_file is not None:
    with st.spinner("Processing..."):

        # 2. Load DataFrame
        try:
            df = pd.read_excel(uploaded_file, skiprows=5, usecols="B:P", header=None)
        except Exception as e:
            st.error(f"Could not read Excel file: {e}")
            st.stop()

        # 3. Convert all values to strings & replace missing values
        df = df.astype(str).replace("nan", "N/A").replace("<NA>", "N/A")

        # 4. Fix column 3 (PCT) to remove ".0" from whole numbers
        df.iloc[:, 3] = df.iloc[:, 3].apply(lambda x: str(int(float(x))) if x.replace('.', '', 1).isdigit() else x)

        # 5. Date columns: indices 0,1,2,11 (corresponds to B,C,D,M)
        date_columns = [0, 1, 2, 11]
        for col in date_columns:
            df.iloc[:, col] = pd.to_datetime(df.iloc[:, col], errors='coerce').dt.strftime('%Y-%m-%d')
            df.iloc[:, col] = df.iloc[:, col].fillna("N/A")

        # 6. Replace " & " with " &amp; "
        df = df.map(lambda x: x.replace(" & ", " &amp; ") if isinstance(x, str) else x)

        # 7. Wrap ONLY words containing a hyphen (-) inside <span class="nowrap">
        def wrap_hyphenated_words(text):
            if isinstance(text, str) and "-" in text and text != "N/A":
                words = text.split()
                wrapped_words = [f'<span class="nowrap">{word}</span>' if '-' in word else word for word in words]
                return " ".join(wrapped_words)
            return text

        df = df.map(wrap_hyphenated_words)

        # 8. Wrap content of column J (index 8) in <span lang="fr"></span>
        df.iloc[:, 8] = df.iloc[:, 8].apply(lambda x: f'<span lang="fr">{x}</span>' if x != "N/A" else x)

        # 9. Custom column headers
        custom_headers = [
            "Predicted Grant Date", "Final Fee Received Date", "Pre-Grant Date", 
            "Application Number", "PCT", "Applicants", "Inventors",
            "English Title", "French Title", "Classification", "Agent", 
            "Examination Requested Date", "PCT Application Number", "PCT Publication Number", "Comments"
        ]

        # 10. Convert to HTML rows without headers
        html_rows = df.to_html(index=False, header=False, border=1, escape=False)

        # 11. Assemble full HTML table
        # Use today's date as table caption, or let user set it
        today_str = datetime.today().strftime("%Y-%m-%d")
        caption_str = st.text_input("Table Caption Date", value=today_str)
        html_table = f"""
<div class="small table-responsive">
<table class="wb-tables small dataTable no-footer table table-striped table-hover" data-wb-tables="{{&quot;lengthMenu&quot; : [10, 20, 50, 100], &quot;order&quot;: [0, &quot;asc&quot;]}}" id="dataset-filter">
    <caption class="bg-primary">Weekly Pre-Grants<br><span class="nowrap">{caption_str}</span></caption>
    <thead>
        <tr class="bg-info">
            {''.join(f'<th>{col}</th>' for col in custom_headers)}
        </tr>
    </thead>
    <tbody>
        {html_rows.split('<tbody>')[1]}
</div>
"""

        # 12. Display & download
        # Display HTML preview
        with st.expander("See HTML code of output table"):
            st.code(html_table, language='html')

        # Download button
        outbuf = io.BytesIO(html_table.encode("utf-8"))
        st.download_button(
            label="Download GrantTable_eng.html",
            data=outbuf,
            file_name="GrantTable_eng.html",
            mime="text/html",
        )

        st.success("HTML file is ready!")

# Optional: Example file link
st.markdown("""
---
ℹ️ Example source file:  
[OPIC_Brevets_Preoctrois_Hebdomadaires-CIPO_Patents_Weekly_Pre-Grants_1.xlsx](https://ised-isde.canada.ca/site/canadian-intellectual-property-office/sites/default/files/documents/OPIC_Brevets_Preoctrois_Hebdomadaires-CIPO_Patents_Weekly_Pre-Grants_1.xlsx)
""")