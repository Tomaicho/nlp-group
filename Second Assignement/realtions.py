import json
import spacy

def find_related_terms(data):
    nlp = spacy.load("<language_model>")  # Replace with appropriate language model, e.g., "en_core_web_sm"

    for term in data:
        if "des" in data[term]:
            descriptions = data[term]["des"]
            nouns = []
            adjectives = []

            for description in descriptions:
                doc = nlp(description)
                for token in doc:
                    if token.pos_ == "NOUN":  # Noun check
                        nouns.append(token.text)
                    elif token.pos_ == "ADJ":  # Adjective check
                        adjectives.append(token.text)

            for related_term in data:
                if related_term != term:
                    if "pt" in data[related_term]:
                        pt_term = data[related_term]["pt"]
                        if pt_term in nouns or pt_term in adjectives:
                            if "relation" not in data[term]:
                                data[term]["relation"] = []
                            data[term]["relation"].append(related_term)

    return data

# Parse the JSON data
data = json.loads(json_data)

# Find and add related terms
updated_data = find_related_terms(data)

# Print the updated JSON dictionary
print(json.dumps(updated_data, indent=2))
