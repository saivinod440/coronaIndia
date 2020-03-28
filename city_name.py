from flask import Flask, request, Response, jsonify, abort
from fuzzywuzzy import process

with open("/home/meghanabhange/mysite/prefered_labels.txt", "r") as f:
    prefered_labels = f.readlines()


def correct_text(text):
    if not text:
        return
    output = {}
    output[process.extractOne(text, prefered_labels)[0]] = process.extractOne(
        text, prefered_labels
    )[1]
    if len(text.split()) > 1:
        output[
            process.extractOne(text.split()[0], prefered_labels)[0]
        ] = process.extractOne(text, prefered_labels)[1]
    for key, value in output.items():
        if value == 100:
            return key
        elif value > 85:
            return key
    return text


app = Flask(__name__)


@app.route("/city_name", methods=["POST"])
def correct_city_name():
    try:
        req_data = request.get_json()
        results = {
            "correct-port-of-origin-of-journey": correct_text(
                req_data["port-of-origin-of-journey"]
            ).replace("\n", "")
        }
    except TypeError:
        # abort when not JSON
        abort(400)
    except KeyError:
        # return error when no org paramter
        return jsonify(error="Not the correct request format!")
    return jsonify(results)