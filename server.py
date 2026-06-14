try:
    # try to import flask, or return error if has not been installed
    from flask import Flask
    from flask import send_from_directory
    from flask import jsonify, render_template, request
except ImportError:
    print("You don't have Flask installed, run `$ pip3 install flask` and try again")
    exit(1)

import os
import re
import subprocess

static_file_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), './')
app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0 #disable cache


def _class_sort_key(name):
    match = re.match(r"^class_(\d+)$", name)
    return int(match.group(1)) if match else 10**9


def _get_class_dirs():
    dirs = []
    for name in os.listdir(static_file_dir):
        full_path = os.path.join(static_file_dir, name)
        if os.path.isdir(full_path) and re.match(r"^class_\d+$", name):
            dirs.append(name)
    return sorted(dirs, key=_class_sort_key)


def _build_catalog():
    catalog = []
    for class_name in _get_class_dirs():
        class_path = os.path.join(static_file_dir, class_name)
        summaries = []
        complete = []

        for entry in sorted(os.listdir(class_path)):
            entry_path = os.path.join(class_path, entry)
            if not os.path.isfile(entry_path):
                continue

            lower = entry.lower()
            if lower.endswith('.md') and (lower.startswith('resume_') or lower.startswith('resumen_')):
                summaries.append(entry)
            elif lower.endswith('.json'):
                complete.append(entry)

        catalog.append({
            'class': class_name,
            'summaries': summaries,
            'complete': complete
        })

    return catalog


def _find_allowed_file(catalog, class_name, content_type, filename):
    valid_type = 'summaries' if content_type == 'resumen' else 'complete'
    for item in catalog:
        if item['class'] == class_name and filename in item[valid_type]:
            return True
    return False

# Serving the index file
@app.route('/', methods=['GET'])
def serve_dir_directory_index():
    if os.path.exists("app.py"):
        # if app.py exists we use the render function
        out = subprocess.Popen(['python3','app.py'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        stdout,stderr = out.communicate()
        return stdout if out.returncode == 0 else f"<pre style='color: red;'>{stdout.decode('utf-8')}</pre>"
    if os.path.exists("index.html"):
        return send_from_directory(static_file_dir, 'index.html')
    else:
        return "<h1 align='center'>404</h1><h2 align='center'>Missing index.html file</h2><p align='center'><img src='https://github.com/4GeeksAcademy/html-hello/blob/main/.vscode/rigo-baby.jpeg?raw=true' /></p>"


@app.route('/academy', methods=['GET'])
def serve_academy():
    return render_template('academy.html')


@app.route('/api/classes', methods=['GET'])
def api_classes():
        return jsonify({'classes': _build_catalog()})


@app.route('/api/content', methods=['GET'])
def api_content():
        class_name = request.args.get('class', '').strip()
        content_type = request.args.get('type', '').strip().lower()
        filename = request.args.get('file', '').strip()

        if not class_name or not filename or content_type not in ['resumen', 'completa']:
                return jsonify({'error': 'missing_or_invalid_parameters'}), 400

        if '/' in filename or '\\' in filename or '..' in filename:
                return jsonify({'error': 'invalid_filename'}), 400

        catalog = _build_catalog()
        if not _find_allowed_file(catalog, class_name, content_type, filename):
                return jsonify({'error': 'file_not_allowed'}), 404

        full_path = os.path.join(static_file_dir, class_name, filename)
        if not os.path.isfile(full_path):
                return jsonify({'error': 'file_not_found'}), 404

        with open(full_path, 'r', encoding='utf-8', errors='replace') as f:
                text = f.read()

        ext = filename.rsplit('.', 1)[-1].lower() if '.' in filename else ''
        return jsonify({
                'class': class_name,
                'type': content_type,
                'file': filename,
                'extension': ext,
                'content': text
        })

# Serving any other image
@app.route('/<path:path>', methods=['GET'])
def serve_any_other_file(path):
    if not os.path.isfile(os.path.join(static_file_dir, path)):
        path = os.path.join(path, 'index.html')
    response = send_from_directory(static_file_dir, path)
    response.cache_control.max_age = 0 # avoid cache memory
    return response

app.run(host='0.0.0.0',port=3000, debug=True, extra_files=['./',])
