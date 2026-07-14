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
from pathlib import Path
import json
import os

software_list_path = os.getenv("SOFTWARE_LIST_PATH", "docs/assets/")
domains_list_file = os.getenv("SOFTWARE_LIST_PATH", "docs/assets/domains.json")
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
