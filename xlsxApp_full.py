import streamlit as st
import pandas as pd
import io
from datetime import datetime

st.set_page_config(page_title="Pre-Grant Excel to HTML")
st.title("Weekly Patent Pre-Grant Excel to HTML Table")

# UI: English / French toggle
mode = st.radio(
    "Choose output language/format:",
    options=["English (eng)", "Français (fra)"],
    horizontal=True,
    index=0,
    format_func=lambda x: "English" if x == "English (eng)" else "French / Français"
)

# UI: File uploader
uploaded_file = st.file_uploader(
    "Upload your Excel file (skip first 5 rows, columns B:P)", type=["xlsx"]
)

html_table = None

if uploaded_file is not None:
    with st.spinner("Processing..."):

        # Load excel
        try:
            df = pd.read_excel(uploaded_file, skiprows=5, usecols="B:P", header=None)
        except Exception as e:
            st.error(f"Could not read Excel file: {e}")
            st.stop()

        if mode == "English (eng)":
            # ENG parameters
            custom_headers = [
                "Predicted Grant Date", "Final Fee Received Date", "Pre-Grant Date", 
                "Application Number", "PCT", "Applicants", "Inventors",
                "English Title", "French Title", "Classification", "Agent", 
                "Examination Requested Date", "PCT Application Number", "PCT Publication Number", "Comments"
            ]
            na_value = "N/A"
            span_col = 8  # French Title
            span_lang = "fr"
            caption_default = "Weekly Pre-Grants"
            caption_suffix = "eng"
            col_for_span = 8
        else:
            # FRA parameters
            custom_headers = [
                "Date prévue d'octroi", "Date de réception de la taxe finale", "Date de préoctroi", 
                "Numéro de demande", "PCT", "Demandeurs", "Inventeurs",
                "Titre anglais", "Titre français", "Classification", "Agent", 
                "Date de requête d'examen", "Numéro de demande PCT", "Numéro de publication PCT", "Commentaires"
            ]
            na_value = "s/o"
            span_col = 7  # English Title
            span_lang = "en"
            caption_default = "Préoctrois Hebdomadaires"
            caption_suffix = "fra"
            col_for_span = 7

        # Turn all to string and set missing values
        df = df.astype(str).replace("nan", na_value).replace("<NA>", na_value)

        # Fix column 3 (PCT) to remove .0 from ints
        df.iloc[:, 3] = df.iloc[:, 3].apply(lambda x: str(int(float(x))) if x.replace('.', '', 1).isdigit() else x)

        # Format dates (cols 0,1,2,11)
        date_columns = [0, 1, 2, 11]
        for col in date_columns:
            df.iloc[:, col] = pd.to_datetime(df.iloc[:, col], errors='coerce').dt.strftime('%Y-%m-%d')
            df.iloc[:, col] = df.iloc[:, col].fillna(na_value)

        # Replace " & " with " &amp; "
        df = df.map(lambda x: x.replace(" & ", " &amp; ") if isinstance(x, str) else x)

        # Wrap ONLY words containing a hyphen (-) inside <span class="nowrap">
        def wrap_hyphenated_words(text):
            # Don't wrap "s/o"/"N/A"
            if isinstance(text, str) and "-" in text and text != na_value:
                words = text.split()
                wrapped_words = [f'<span class="nowrap">{word}</span>' if '-' in word else word for word in words]
                return " ".join(wrapped_words)
            return text

        df = df.map(wrap_hyphenated_words)

        # Wrap lang spans
        df.iloc[:, col_for_span] = df.iloc[:, col_for_span].apply(
            lambda x: f'<span lang="{span_lang}">{x}</span>' if x != na_value else x
        )

        # HTML conversion (no border, headers)
        html_rows = df.to_html(index=False, header=False, border=1, escape=False)

        # Date for caption
        today_str = datetime.today().strftime("%Y-%m-%d")
        caption_str = st.text_input(
            "Table Caption Date", value=today_str, key="caption_input_"+caption_suffix
        )

        # Prepare the output HTML (table, caption, etc)
        html_table = f"""
<div class="small table-responsive">
<table class="wb-tables small dataTable no-footer table table-striped table-hover" data-wb-tables="{{&quot;lengthMenu&quot; : [10, 20, 50, 100], &quot;order&quot;: [0, &quot;asc&quot;]}}" id="dataset-filter">
    <caption class="bg-primary">{caption_default}<br><span class="nowrap">{caption_str}</span></caption>
    <thead>
        <tr class="bg-info">
            {''.join(f'<th>{col}</th>' for col in custom_headers)}
        </tr>
    </thead>
    <tbody>
        {html_rows.split('<tbody>')[1]}
</div>
"""

        # Show result
        with st.expander("See HTML code of output table"):
            st.code(html_table, language='html')

        # Download button
        outbuf = io.BytesIO(html_table.encode("utf-8"))
        st.download_button(
            label=f"Download GrantTable_{caption_suffix}.html",
            data=outbuf,
            file_name=f"GrantTable_{caption_suffix}.html",
            mime="text/html",
        )

        st.success("HTML file is ready!")

st.markdown("""
---
ℹ️ Example file:  
[OPIC_Brevets_Preoctrois_Hebdomadaires-CIPO_Patents_Weekly_Pre-Grants_1.xlsx](https://ised-isde.canada.ca/site/canadian-intellectual-property-office/sites/default/files/documents/OPIC_Brevets_Preoctrois_Hebdomadaires-CIPO_Patents_Weekly_Pre-Grants_1.xlsx)
""")