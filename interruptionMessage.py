import streamlit as st
from datetime import date

# Define the HTML template
HTML_TEMPLATE = """
<h2 class="text-danger">TITLE HERE &ndash; (<time class="nowrap" datetime="DATE HERE(YYYY-MM-DD)">DATE HERE(YYYY-MM-DD)</time>)</h2>

<p>CONTENT HERE</p>

<p>For more information, please contact our <a data-entity-substitution="canonical" data-entity-type="node" data-entity-uuid="78a10a22-8b11-4c4e-bef2-5c37808ebaba" href="/site/canadian-intellectual-property-office/node/13">Client Service Centre</a>. For date-sensitive material, please review our <a data-entity-substitution="canonical" data-entity-type="node" data-entity-uuid="d0a59429-cdb8-4122-b2b0-6167cf90e56b" href="/site/canadian-intellectual-property-office/node/133">Correspondence Procedures</a>.</p>

<h2 class="text-danger">FRENCH TITLE HERE &ndash; (<time class="nowrap" datetime="DATE HERE(YYYY-MM-DD)">DATE HERE(YYYY-MM-DD) </time>)</h2>

<p>FRENCH CONTENT HERE</p>


<p>Pour de plus amples renseignements, veuillez communiquer avec notre <a data-entity-substitution="canonical" data-entity-type="node" data-entity-uuid="78a10a22-8b11-4c4e-bef2-5c37808ebaba" href="/site/canadian-intellectual-property-office/node/13">Centre de services à la clientèle</a>. Pour les demandes assorties de délais, veuillez consulter les <a data-entity-substitution="canonical" data-entity-type="node" data-entity-uuid="d0a59429-cdb8-4122-b2b0-6167cf90e56b" href="/site/canadian-intellectual-property-office/node/133">Procédures relatives à la correspondance</a>.</p>
"""

# Corrected template placeholders for clarity and direct replacement
# Note: I've used unique placeholders for English and French content as the template had "CONTENT HERE" twice.
# Also added a unique placeholder for the date text inside the <time> tag.
CORRECTED_HTML_TEMPLATE = """
<h2 class="text-danger">{english_title} &ndash; (<time class="nowrap" datetime="{date_iso}">{date_text}</time>)</h2>

<p>{english_content}</p>

<p>For more information, please contact our <a data-entity-substitution="canonical" data-entity-type="node" data-entity-uuid="78a10a22-8b11-4c4e-bef2-5c37808ebaba" href="/site/canadian-intellectual-property-office/node/13">Client Service Centre</a>. For date-sensitive material, please review our <a data-entity-substitution="canonical" data-entity-type="node" data-entity-uuid="d0a59429-cdb8-4122-b2b0-6167cf90e56b" href="/site/canadian-intellectual-property-office/node/133">Correspondence Procedures</a>.</p>

<h2 class="text-danger">{french_title} &ndash; (<time class="nowrap" datetime="{date_iso}">{date_text}</time>)</h2>

<p>{french_content}</p>


<p>Pour de plus amples renseignements, veuillez communiquer avec notre <a data-entity-substitution="canonical" data-entity-type="node" data-entity-uuid="78a10a22-8b11-4c4e-bef2-5c37808ebaba" href="/site/canadian-intellectual-property-office/node/13">Centre de services à la clientèle</a>. Pour les demandes assorties de délais, veuillez consulter les <a data-entity-substitution="canonical" data-entity-type="node" data-entity-uuid="d0a59429-cdb8-4122-b2b0-6167cf90e56b" href="/site/canadian-intellectual-property-office/node/133">Procédures relatives à la correspondance</a>.</p>
"""


st.set_page_config(page_title="HTML Message Generator", layout="centered")

st.title("HTML Message Generator")
st.write("Fill out the form below to generate your HTML message.")

# Input form
with st.form(key='html_form'):
    st.subheader("Message Details")

    english_title = st.text_input("English Title", key='en_title')
    french_title = st.text_input("French Title", key='fr_title')

    # Using a single date input as the template uses one date placeholder
    message_date = st.date_input("Date", value=date.today(), key='message_date')

    st.subheader("Content")
    english_content = st.text_area("English Content", key='en_content')
    french_content = st.text_area("French Content", key='fr_content')

    generate_button = st.form_submit_button("Generate HTML")

# Generate HTML on button click
if generate_button:
    if english_title and french_title and english_content and french_content and message_date:
        # Format the date
        date_iso_format = message_date.strftime("%Y-%m-%d")
        # Use the same format for the text display in the template
        date_text_format = message_date.strftime("%Y-%m-%d") # Or you could use a different display format here

        # Populate the template using the corrected placeholders
        generated_html = CORRECTED_HTML_TEMPLATE.format(
            english_title=english_title,
            french_title=french_title,
            date_iso=date_iso_format,
            date_text=date_text_format,
            english_content=english_content,
            french_content=french_content
        )

        st.subheader("Generated HTML Output")
        # Display the code using st.code
        st.code(generated_html, language='html')

        st.subheader("Preview")
        # Optionally display a preview (use with caution due to unsafe_allow_html)
        # st.markdown(generated_html, unsafe_allow_html=True)

    else:
        st.warning("Please fill out all fields.")

