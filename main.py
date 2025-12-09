from flask import Flask, request, jsonify
import unicodedata

app = Flask(__name__)

ALLOWED_LANGUAGES = {"english", "spanish"}

def to_tokens(text: str, language: str):
    raw_tokens = text.split()
    if language == "english":
        tokens = [
            unicodedata.normalize("NFKD", t)
            .encode("ascii", "ignore")
            .decode("ascii")
            .lower()
            for t in raw_tokens
        ]
    else:  # spanish
        tokens = [t.lower() for t in raw_tokens]
    return tokens


@app.route('/transform', methods=['POST'])
def transform():
    # Non-JSON body -> 400 (force parse to avoid 415)
    try:
        data = request.get_json(force=True)
    except Exception:
        return jsonify({"error": "invalid JSON"}), 400

    if data is None:
        return jsonify({"error": "invalid JSON"}), 400

    if 'text' not in data:
        return jsonify({"error": "missing required field 'text'"}), 400

    text = data.get('text')
    if not isinstance(text, str):
        return jsonify({"error": "field 'text' must be a string"}), 400

    language = data.get('language', 'english')
    if not isinstance(language, str):
        return jsonify({"error": "unsupported language"}), 400

    language = language.lower()
    if language not in ALLOWED_LANGUAGES:
        return jsonify({"error": "unsupported language"}), 400

    tokens = to_tokens(text, language)
    count = len(tokens)
    has_numbers = any(ch.isdigit() for ch in text)

    return jsonify({
        "tokens": tokens,
        "count": count,
        "has_numbers": has_numbers
    }), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
