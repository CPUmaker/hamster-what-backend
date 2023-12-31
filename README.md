# ECE651_Backend



## Getting started

To make it easy for you to get started with GitLab, here's a list of recommended next steps.

## Leverage the repo with git

- [ ] Add your ssh-key to your GitLab account and clone the repo:

```script
# It is recommended to clone with ssh.
git clone ist-git@git.uwaterloo.ca:c58li/ece651_frontend.git
cd ece651_frontend
```

- [ ] Create/switch your develop branch:

```script
git checkout -b <new-branch>            # <new-branch> is what your branch will name.
git checkout ＜existing-branch＞        # <existing-branch> is what your branch names.
# If you wanna list all branch, use the following command:
git branch -a
```

Noted: Name branch followed by naming convention: `<name>\<category>\<description>`.

- [ ] After modifying the project, add, commit and push the change to the remote repo:

```script
git add .
git commit -m "..."     # "..." is where you need to add comment.
git push
git push origin <branch-name>       # another version
git push -u origin <new-branch>    # push for new branch
```

- If your teammate reviewed your code, merge it into the main branch:

```script
# ensure you have added and commited in your current branch
git checkout main
git merge <branch-name>
```

## Installation

- [ ] Install [Miniconda](https://conda.io/projects/conda/en/stable/user-guide/install/download.html) or [Anaconda](https://www.anaconda.com/) to manage your python packages.

- [ ] Create a virtual env via conda: `conda env create -f environment.yml`.

- [ ] Start the Django server:

```script
python manage.py runserver
python manage.py runserver 0.0.0.0:8000     # This command could let you test your code in other computers in the same LAN.
```

- [ ] The setup procedure could be found in Django official documents and toturial as well.

## Usage

- Check migration before run the server:

```script
python manage.py makemigrations
python manage.py migrate
```

- Run the server

```script
python manage.py runserver
```

- Browser the document

Type the link (`http://127.0.0.1:8000/docs/`) in to the browser, and you could see the API document there.

## Support

Tell people where they can go to for help. It can be any combination of an issue tracker, a chat room, an email address, etc.

## Contributing

State if you are open to contributions and what your requirements are for accepting them.

For people who want to make changes to your project, it's helpful to have some documentation on how to get started. Perhaps there is a script that they should run or some environment variables that they need to set. Make these steps explicit. These instructions could also be useful to your future self.

You can also document commands to lint the code or run tests. These steps help to ensure high code quality and reduce the likelihood that the changes inadvertently break something. Having instructions for running tests is especially helpful if it requires external setup, such as starting a Selenium server for testing in a browser.

## Authors and acknowledgment

Show your appreciation to those who have contributed to the project.

## License

For open source projects, say how it is licensed.
