import streamlit as st
from datetime import date
import html  # import to use html.escape()

# Corrected template with placeholders
CORRECTED_HTML_TEMPLATE = """
<h2 class="text-danger">{english_title} &ndash; (<time class="nowrap" datetime="{date_iso}">{date_text}</time>)</h2>

{english_content}

<p>For more information, please contact our <a data-entity-substitution="canonical" data-entity-type="node" data-entity-uuid="78a10a22-8b11-4c4e-bef2-5c37808ebaba" href="/site/canadian-intellectual-property-office/node/13">Client Service Centre</a>. For date-sensitive material, please review our <a data-entity-substitution="canonical" data-entity-type="node" data-entity-uuid="d0a59429-cdb8-4122-b2b0-6167cf90e56b" href="/site/canadian-intellectual-property-office/node/133">Correspondence Procedures</a>.</p>

<h2 class="text-danger">{french_title} &ndash; (<time class="nowrap" datetime="{date_iso}">{date_text}</time>)</h2>

{french_content}

<p>Pour de plus amples renseignements, veuillez communiquer avec notre <a data-entity-substitution="canonical" data-entity-type="node" data-entity-uuid="78a10a22-8b11-4c4e-bef2-5c37808ebaba" href="/site/canadian-intellectual-property-office/node/13">Centre de services à la clientèle</a>. Pour les demandes assorties de délais, veuillez consulter les <a data-entity-substitution="canonical" data-entity-type="node" data-entity-uuid="d0a59429-cdb8-4122-b2b0-6167cf90e56b" href="/site/canadian-intellectual-property-office/node/133">Procédures relatives à la correspondance</a>.</p>
"""

st.set_page_config(page_title="HTML Message Generator", layout="centered")
st.title("HTML Message Generator")
st.write("Fill out the form below to generate your HTML message.")

# INPUT FORM
with st.form(key='html_form'):
    st.subheader("Message Details")

    english_title = st.text_input("English Title", key='en_title')
    french_title = st.text_input("French Title", key='fr_title')
    message_date = st.date_input("Date", value=date.today(), key='message_date')

    st.subheader("Content")
    english_content = st.text_area("English Content", key='en_content')
    french_content = st.text_area("French Content", key='fr_content')

    generate_button = st.form_submit_button("Generate HTML")

# FUNCTION: Turn paragraphs into <p>...</p> and escape HTML
def content_to_paragraphs(content):
    # Split text on double newline for paragraphs
    paragraphs = [para.strip() for para in content.split('\n\n') if para.strip()]
    # Escape HTML entities and wrap in <p>
    return '\n\n'.join(f"<p>{html.escape(para)}</p>" for para in paragraphs)

# HTML GENERATION
if generate_button:
    if english_title and french_title and english_content and french_content and message_date:
        date_iso_format = message_date.strftime("%Y-%m-%d")
        date_text_format = message_date.strftime("%Y-%m-%d")

        english_paragraphs = content_to_paragraphs(english_content)
        french_paragraphs = content_to_paragraphs(french_content)

        generated_html = CORRECTED_HTML_TEMPLATE.format(
            english_title=html.escape(english_title),
            french_title=html.escape(french_title),
            date_iso=date_iso_format,
            date_text=date_text_format,
            english_content=english_paragraphs,
            french_content=french_paragraphs
        )

        st.subheader("Generated HTML Output")
        st.code(generated_html, language='html')
        st.subheader("Preview")
        # If you want to preview the result as HTML (be aware of XSS risks!):
        # st.markdown(generated_html, unsafe_allow_html=True)

    else:
        st.warning("Please fill out all fields.")