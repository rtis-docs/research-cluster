"""most of the commenting has been left from the NeSI documentation and currently software_environments.md is not using macro
content so I have deleted macro_hooks.py"""
"""
mkdocs_hooks allows injection of variables into templating stage of rendering.
This allows for arbitrary use of variables in TEMPLATE FILES, (e.g. `overrides/*.html`).
As opposed to `macro_hooks.py` which injects variables into macro rendering (e.g. `docs/*.md`).
If this is confusing, ask Cal to explain.
"""

import proselint as pl
import glob
import hashlib
from pathlib import Path
import json
import os

software_list_path = os.getenv("SOFTWARE_LIST_PATH", "docs/assets/")
domains_list_file = os.getenv("SOFTWARE_LIST_PATH", "docs/assets/domains.json")


# Material fingerprints its own bundle - it ships as main.<hash>.min.css - so every build lands
# on a new URL and no cache anywhere can pair new HTML with an old stylesheet. Our own files in
# extra_css and extra_javascript keep a constant name, which leaves them open to exactly that.
#
# It bit us in production on 12 August 2026. Cloudflare fronts researchcomputing.otago.ac.nz and
# caches assets for four hours, but serves the HTML uncached. After a deploy the browser got the
# new markup together with the previous build's extra.css, so a set of freshly styled figures
# arrived with none of their rules and fell back to full-width blocks stacked down the page. The
# origin was correct the whole time; only the edge was stale.
#
# Hashing the file's contents into a query string closes the gap. The query string forms part of
# the cache key, so the URL changes exactly when the file changes, and stays put when it does
# not - unchanged assets keep their cache entry across deploys.
def on_config(config, **kwargs):
    docs_dir = Path(config["docs_dir"])
    for key in ("extra_css", "extra_javascript"):
        config[key] = [_fingerprint(entry, docs_dir) for entry in config[key]]
    return config


def _fingerprint(entry, docs_dir):
    """Append a content hash to a local asset reference, leaving anything else untouched.

    extra_javascript entries arrive as ExtraScriptValue rather than plain strings when they
    carry defer or type, and the template reads their .path, so those are updated in place.
    """
    path = getattr(entry, "path", None) or str(entry)

    # Leave remote assets, and anything already carrying a query, exactly as they are.
    if "://" in path or "?" in path:
        return entry

    source = docs_dir / path
    if not source.is_file():
        return entry

    hashed = f"{path}?h={hashlib.sha256(source.read_bytes()).hexdigest()[:8]}"

    if hasattr(entry, "path"):
        entry.path = hashed
        return entry
    return hashed
# Makes software data accessible for the HTML override templates
def on_env(env, config, files, **kwargs):
    domains = json.load(open(domains_list_file))
    software = {}
    for software_json in Path(software_list_path).glob('software_list.*.json'):
        app_list = json.load(open(software_json))
        for key in app_list:
            if software.get(key) is None:
                software[key] = app_list.get(key)
    
    for key in software:
        if domains.get(key) is not None:
            software[key]["domains"] = domains.get(key).get("domains")
    # add entire module list to keyword 'applications
    #env.globals["applications"] = json.load(open(software_list_path))
    env.globals["applications"] = dict(sorted(software.items()))
    # env.globals["domains"]=json.load(open('../tags/domains.json')).keys() # Needs list of cannon domains to make into


#QULAITY CHECKER
def lint(*args, **kwargs):
    output = {}
    print("running linter")
    for file in glob.iglob("docs/**/*.md", recursive=True):
        with open(file, "r") as f:
            output[Path(file).stem] = pl.tools.lint(f.read())
    with open("lint_report.json", "w+") as f:
        f.write(json.dumps(output))
    print(output)
