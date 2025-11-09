def extract_field(doc, field_name):
    """Extract field value (like url, name, etc.) from structured doc text"""
    for line in doc.page_content.splitlines():
        if line.lower().startswith(f"{field_name.lower()}:"):
            return line.split(":", 1)[1].strip()
    return "N/A"

def format_doc(doc):
    """Convert Document into API-friendly JSON object"""
    return {
        "url": extract_field(doc, "url"),
        "name": extract_field(doc, "name"),
        "adaptive_support": extract_field(doc, "adaptive_support"),
        "description": extract_field(doc, "description"),
        "duration": extract_field(doc, "duration"),
        "remote_support": extract_field(doc, "remote_support"),
        "test_type": [t.strip() for t in extract_field(doc, "test_type").split(",") if t.strip()]
    }
