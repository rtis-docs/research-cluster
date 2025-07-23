


## Developing locally



### Fork or Clone repo (if you have write permissions)
- Make a fork of the repo if you don't have direct write access
- Clone the fork or original (if write access)
- Switch to the `dev` branch
- Make changes to `dev` branch and once happy push to github and create a pull request to main



### Make and serve locally

These commands will let you build and serve the mkdocs website locally for development


Create a python virtual environment and install the needed packages

- **The requirements were last updated 23-07-2025** - local enviroment recreation may be needed


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