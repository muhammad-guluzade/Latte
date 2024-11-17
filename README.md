# Latte

### /static
- /js - Upload any ***JavaScript*** (*.js*) 
- /css - Upload any ***CSS*** (*.css*) 
- /media - Upload any ***media*** like *.png* or *.gif*
- /db - Upload any ***database*** like *.db* or *.sql* 

### /templates

- Upload any ***HTML*** (*.html* or *.htm*) 

### Flask Architecture

The following files and folders ***must*** be in the same folder

- .py file that contains the *app*
- /templates folder
- /static folder

<hr>

### How to use git? Basic commands

- Step 1: Install git so that you can use it in your terminal

- Step 2: Cloning the repository
- - Step 2.1: Create an empty folder
- - Step 2.2: Open terminal and move to that folder
- - Step 2.3: Run `git init`
- - Step 2.4: Run `git clone https://github.com/muhammad-guluzade/Latte-main.git`
- - Step 2.5: Run `cd Latte-main`
- - Step 2.6: Run `git remote set-url origin https://github.com/muhammad-guluzade/Latte-main.git`

- Step 3: Modifying the files. 
- - Step 3.1: Locate test.txt file
- - Step 3.2: Modify test.txt file however you like
- - Step 3.3: Run `git add test.txt` while being inside Latte-main folder
- - Step 3.4: Run `git commit -m "Some message for commit"`
- - Step 3.5: Run `git checkout -b test_branch`
- - Step 3.6: If step 3.5 raised an error, it means that test_branch already exists. In this case run `git checkout test_branch`
- - Step 3.7: Run `git push`
- - Step 3.8: If `fatal: The current branch new_branch has no upstream branch.` occurs, run `git push --set-upstream origin test_branch` and run `git push` again

- Step 4: Retrieving the changes made by others
- - `git pull origin main` will pull all the changes and files into your local machine

- Step 5: Additional commands
- - `git branch` - tells which branch you are at currently
- - `git status` - shows the status of commited/uncommited files

<hr>

### What is .gitignore ?

In that file, you put everything that you do not want to push to main repository. For example, if in your local machine contains file "test.html" that you do not want to push, just include it as "templates/test.html", and it will not be pushed.

<hr>

### Files in our project (Explanation)

#### main.py

- This file is responsible for the flask application

#### database.py

- This file contains the database initializer