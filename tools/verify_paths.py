import os
import re
import sys

root = r'C:\Users\Admin\Workspaces\nxtutor-landing-pages'
html_files = []
for dirpath, _, filenames in os.walk(root):
    for fn in filenames:
        if fn.endswith('.html'):
            html_files.append(os.path.join(dirpath, fn))

missing = []
pattern = re.compile(r'(?:href|src)=["\']([^"\'>\s]+)["\']')
checked_count = 0

for fpath in html_files:
    with open(fpath, 'r', encoding='utf-8') as f:
        content = f.read()
    for m in pattern.finditer(content):
        url = m.group(1)
        if url.startswith(('http://', 'https://', 'mailto:', '#')):
            continue
        checked_count += 1
        clean_url = url.lstrip('/')
        clean_url = clean_url.split('?')[0].split('#')[0]
        if not clean_url:
            target = os.path.join(root, 'index.html')
        elif clean_url.endswith('/'):
            target = os.path.join(root, clean_url.replace('/', os.sep), 'index.html')
        else:
            cand1 = os.path.join(root, clean_url.replace('/', os.sep))
            cand2 = os.path.join(root, clean_url.replace('/', os.sep), 'index.html')
            if os.path.exists(cand1):
                target = cand1
            elif os.path.exists(cand2):
                target = cand2
            else:
                target = cand1
        if not os.path.exists(target):
            missing.append({'source': fpath.replace(root, ''), 'url': url, 'target': target.replace(root, '')})

if not missing:
    print(f'ALL_LOCAL_PATHS_RESOLVED_100%_CLEAN (Checked {len(html_files)} HTML files, {checked_count} local links/assets)')
    sys.exit(0)
else:
    for m in missing:
        print(f'MISSING: {m}')
    sys.exit(1)
