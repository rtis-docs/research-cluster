


## Developing locally



### Fork or Clone repo (if you have write permissions)
- Make a fork of the repo if you don't have direct write access
- Clone the fork or original (if write access)
- Switch to the `dev` branch
- Make changes to `dev` branch and once happy push to github and create a pull request to main



### Make and serve locally

These commands will let you build and serve the mkdocs website locally for development


Create a python virtual environment and install the needed packages

- **The requirements were last updated 23-07-2025** - local environment recreation may be needed


```bash
# create a python virtual environment
python -m venv venv/

# activate it (might not work on Windows - see below)
source venv/bin/activate
# If the above line doesn't work then navigate to the folder with activate.ps1 in it then run
.\\activate.ps1

# install the requirements into it
pip install -r requirements.txt
#you may need to make sure you are in the directory that contains this file
```

To build and serve locally:
```bash
mkdocs serve
```

In the output look for messages about pages containing links but there is no such page or anchor. This will help prevent broken links creeping in.


## Conventions

### Peer-review vs merge straight in

New pages, small modifications or expansions of a page(s) (e.g. straight forward edits) can be merged straight in and for things that are substantial re-writes or structural/layout changes a peer-review on the pull request should be requested so implications of the change can be discussed.


### Including support email

In all places where the support/contact email is being referenced use the variable `{{support_email}}` which will substitute in the correct mailto link and gives a single location where we can update the email address if needed.

- Try to use the phrase `...email the eResearch Support team at **{{ support_email }}**...` which will make the email address clear to the user rather than being hidden as only the link contents.

### Use relative links

Originally variables were being used for some highly referred to pages (apptainer, conda, spack, etc.). It is now preferred in all cases when referring to content within the documentation to do so via relative links. This gives greater visibility when doing `make serve` as to where there might be broken/missing content.

### Git commits

Try to limit commits to a single feature or type of change and avoid combining unrelated changes into a single commit.


### Capitalisation

Use "Slurm" and "OnDemand" to remain consistent with how those products refer to themselves. 


### Navigation bar and `.nav.yml`

Where possible use a H1 heading at the top of the specific page, rather than customising the page name within `.nav.yml`

Use a `.nav.yml` in the directory to alter how the structure of the navigation behaves. If moving a page, make sure to update the `.nav.yml` of the source and target directories (where applicable).

