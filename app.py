import os
import pathlib
from importlib import import_module

from flask import Flask, jsonify, Blueprint

source_root = os.path.dirname(os.path.abspath(__file__))
app = Flask(__name__)


@app.route("/")
def root():
    return jsonify(
        name="CWB JSON API",
        source="https://github.com/sodascourse/cwb-json-api",
        endpoints=[url_rule.rule for url_rule in app.url_map.iter_rules()
                   if not url_rule.rule.startswith('/static') and url_rule.rule != '/'],
    )


# Find pages
for page_module_path in pathlib.Path(source_root, 'pages').glob('*.py'):
    page_module_name = page_module_path.stem
    if page_module_name == '__init__':
        continue

    try:
        page_module = import_module('pages.{}'.format(page_module_name))
    except ImportError:
        continue

    blueprint_page = getattr(page_module, 'page', None)
    if blueprint_page is None or not isinstance(blueprint_page, Blueprint):
        continue

    url_prefix = getattr(page_module, 'url_prefix', None)
    if url_prefix is None or not isinstance(url_prefix, str):
        continue

    app.register_blueprint(blueprint_page, url_prefix=url_prefix)


if __name__ == "__main__":
    DEBUG = int(os.environ.get('DEBUG', '0')) != 0
    app.run(debug=DEBUG)
