


## Developing locally

### Clone repo
- Make a local copy with `git clone git@github.com:rtis-docs/research-cluster.git && cd research-cluster`
- Switch to the `dev` branch `git switch dev`
- Make changes to `dev` branch and once happy push to github and create a pull request to main

### Make and serve locally

These commands will let you build and serve the mkdocs website locally for development

Create a python virtual environment and install the needed packages
```bash
# create a pythong virtual environment
python -m venv venv/

# activate it
source venv/bin/activate

# install the requirements into it
pip install -r requirements.txt
```

To build and serve locally:
```bash
mkdocs serve
```