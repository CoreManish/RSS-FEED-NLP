import spacy

# Load spaCy English model
nlp = spacy.load("en_core_web_sm")

def categorize_text(text):
    doc = nlp(text)
    categories = []

    # Define keywords for each category
    terrorism_keywords = ['terrorism', 'protest', 'political unrest', 'riot']
    positive_keywords = ['positive', 'uplifting', 'joyful']
    natural_disaster_keywords = ['natural disaster', 'earthquake', 'flood', 'hurricane']

    # Check for relevant entities in the text
    for ent in doc.ents:
        if any(keyword in ent.text.lower() for keyword in terrorism_keywords):
            categories.append('Terrorism/Protest/Political Unrest/Riot')
        elif any(keyword in ent.text.lower() for keyword in positive_keywords):
            categories.append('Positive/Uplifting')
        elif any(keyword in ent.text.lower() for keyword in natural_disaster_keywords):
            categories.append('Natural Disasters')

    # If none of the predefined categories match, assign to 'Others'
    if not categories:
        categories.append('Others')

    return categories