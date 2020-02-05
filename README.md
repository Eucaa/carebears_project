# Care Bears Database

***Find all information about the loveable characters which originated in the '80.***

## Introduction
___

This is database was created to give people the oppurtinity to discover more about the backgrounds of the characters from the care bears familiy, 
and add and adjust information regarding their favorite caharcter from the series. It's purpose is not to only attract fans of the series, but also peak
the interst of unfamiliars. Since the series has been running from the '80 and it's concept is still running in a new shape today, there will be lots of 
potential to enhance this database into further depths for many years to come.

You can visit the Care Bears Database home page from here: [_Care Bears Database_](https://carebear-db.herokuapp.com/).

## UX
____

The database provides an overview of the charaters created for the Care Bears franchise. It includes detailed information about the character itself and the 
possibility to write a small story about the personality of the character. Since the trademark has been excisting since the 1980', it's age group of 
intersted individuals can extent to a wide range as well. It was therefor essential to make this database easy accessible and appealing for multiple ages.
The home page provides a search bar where user can type in a word that they (think) that might be realted to their favourite character. By clicking the 
'search' button, the user will immediately be redirected to a new page the a list will be available showing all characters that contain the requested word.
From here, the user can click on the 'details' link to access futher character information.
The 'see all characters' button will redirect the user to a page with the full list of available characters in the database.
To appeal the user and interest them to read more about other present characters, a "feature characters" is available. By clicking on the image, the user
wil be automatically redirect to the appointed character's info page.
The user will be able to add, update and delete characters. A link to add a character and the complete character list are also located in the navbar.
The navbar also includes an 'about'- link, which will redirect the user to a page with a general story about the franchise.
This database was created in a mobile friendly manner.


### General User Stories
____
- As a type of user, I would like to be seach for my favorite character in an easy accessible way.
- As a type of user, I would like to explore new characters that I didn't knew about before.
- As a type of user, I would like to search on a keyword of a detail I can remember about the character.
- As a type of user, I would like to be able to add, update and delete information when needed.


### Wireframes
____
The original wireframes of the project: [_Wireframes_](https://github.com/Eucaa/carebears_project/blob/1fdc51d9311ebc2bfd9c442eceffb5d5899fab4c/wireframes_and_ERD/Care%20Bear%20DB%20original%20wireframes.pdf)


### ERD
____
The final ERD of the project: [_ERD_](https://github.com/Eucaa/carebears_project/blob/1fdc51d9311ebc2bfd9c442eceffb5d5899fab4c/wireframes_and_ERD/Care%20Bears%20DB%20ERD.png)


## Features
____
- Search bar - Allows the user to look for a character.
- See all characters button - Redirects the user to the page showing a list of all characters available.
- Featured character - Shows two randomly selected characters in the database which a user can access by clicking the image itself.
- Character creation - Lets the user user create a charater.
- Character List - Shows all characters available in the database.
- Care Bears icon - The Care Bears icon on the left side in the icon bar will refer you back to the home page by clicking it.

### Existing Features

* Searching for a character is possible by entering a keyword. For entering multiple keywords, a user can divide the keywords by using a comma.
* A direct link to more detailed information of a character is available behind the rule of the character in the character list.
* The user will be able to add a character, including an image. 
* Once uploaded, a new image cannot be uploaded again to prevent misuse. 
* All other information of an exciting character will be able to be editted.
* Once editted, the user will be taken back to the character's information page.
* The character information page also includes a 'delete character' button, to delete the complete file of the character.
* If a character cannot be found by a keyword, the character collection list will return empty with the message "No results found", and will be able
  to try again by clicking the link, which will return the user to the home page with search bar option.
* A register and log-in page have been created, but are not functional yet. This does mean that everyone who access the database, will be able to 
  add/edit and delete characters.

### Future Features

* Adding functionality to the register and log-in page.
* Only allowing registered users to delete their own created characters but edit all.
* Non- registered user will only be allowed to read the items in the database, but not add, edit or delete any.
* Add an extra notification before a registered can delete a character.


## Technologies Used
____
- [HTML5](https://developer.mozilla.org/en-US/docs/Web/Guide/HTML/HTML5) This project uses HTML to build the foundation of the web application and 
  includes links to [Bootstrap](https://getbootstrap.com/docs/4.4/getting-started/introduction/), [Gijgo](https://gijgo.com/), JS and CSS.
- [CSS3](https://developer.mozilla.org/en-US/docs/Web/CSS) This project uses CSS3 to add a personal style to the pages and features of the project.
- [Javascript](https://developer.mozilla.org/en-US/docs/Glossary/JavaScript) JavaScript has been added for interactive functionality of the application.
- [Python](https://www.python.org/) The Python language is used to provide backend functionality, including functions to add, edit or delete.
- [PyMongo](https://api.mongodb.com/python/current/) Is used as a driver to access the MongoDB database.
- [MongoDB Atlas](https://www.mongodb.com/cloud/atlas) Was used as cloud host for the database.
- [Flask](https://flask.palletsprojects.com/en/1.1.x/) The Flask framework was used to interact between the front- and backend.
- [Google Fonts](https://fonts.google.com/) Google Fonts was used to provide fonts for the headings of the web application.


## Testing
____

### Manual Testing

This project has been manually tested in different scenario's to check the user experience.

Homepage

1. Clicking the home icon button in the navbar.
    - Get redirected back to the home page.
2. Using the search option by entering keywords.
    - Either get a list of connected characters or "try again.
3. Using the 'See all charaters button'.
    - Get redirect to the view showing all available characters.

About

1. Click the 'about' link in the navbar.
    - Get redirected to the 'about the care bears' page.

Character Creation

1. Click the 'character creation' link in the navbar.
    - Get redirect to the 'Character Creation' page.
2. Add information and image to form.
3. Submit the form.
    - Get redirected to the 'Character Information' page.

Character List and Character Information page

1. Click the 'Character List' link in the navbar.
    - Get redirected to the complete list of characters available in the database.
2. Choose an available character and check the details.
    - Get redirected to the 'Character Information' page.

Edit or Delete a character through the Character Information page

1. On the Character Information page, click the 'Edit Character' button to edit the characters' information.
    - Get redirected to the 'Edit Character' page to edit information about the character (image upload is excluded). Already excisting information will be shown.
2. Sumbit changes by clicking the 'Edit Character' button.
    - Character information will be updated, and user will be redirected back to the Character Information page to view changes.
3. On the Character Information page, click the 'Delete Character' button to delete a characters' data from the database.
    - On click, the character will be deleted and the user will be redirected back to the complete available character list.

### Responsive Testing 

This application has been tested on mobile, tabled and desktop sizes via Google Chrome Developer Tools and is mobile friendly.

### Code Validation

- The HTML coding was checked by using the [W3C Markup Validation](https://validator.w3.org/nu/) by input of url of the webpage.
- CSS coding was checked by using the [W3C Markup Validation](https://jigsaw.w3.org/css-validator/#validate_by_input) by direct input.
- Javascript was checked by using [JShint](https://jshint.com/) by direct input.

### Bugs

- There were issues with being able to save uploaded images in MongoDB. This has been resolves by transversing the uploaded image into code as an image blob
  which could then be translated back into an actual image in the application.
- The information in the tables in the character information where not scaled nicely on smaller devices. I adjusted this by resizing the width the table cells.
- The character container list wasn't showing while using the Safari browser. This was fixed by adding a left and right of 0; to the styling class of the container.


## Deployment
____
The source code for this application can be found on Github and the application itself has been deployed onto Heroku. 
There is no difference between the GitHub code and the code in the live application.

It can be installed with the following steps:

- Download the git repository

- Sign up/login to Heroku.com

- Click Create New App from the dashboard.

- Decide a unique name (non-excisting for Heroku) and your region and click 'Create'.

- From the command line, enter heroku to ensure heroku is installed (if not installed, use sudo snap install --classic heroku)

- Use the heroku login

- Enter your credentials for heroku.com sudo pip3 install Flask sudo pip3 install pymongo sudo pip3 freeze --local > requirements.txt echo web: python run.py > 
  Procfile git add . git commit -m "initial commit" git push -u heroku master heroku ps:scale web=1

- From heroku.com app settings: set config vars to IP : 0.0.0.0, PORT : 8080 and MONGODB_CONNECTIONSTRING
  mongodb+srv://[ username ]:[ password ]@myfirstcluster-sfcla.mongodb.net
  update the username and password accordingly.

- Click More > Restart all Dynos

- Application is live at https://your-app-name.herokuapp.com/

### The repository can be found on:

(https://github.com/Eucaa/carebears_project)


### Credits
____
I would to credit the following sources for their inspiration:
Stack Overflow community
CodePen community


### Media
____
Images have been taken from 
[care bears fandom](https://carebears.fandom.com/wiki/Care_Bear_Wiki)
[getwallpapers.com](http://getwallpapers.com/collection/care-bears-wallpaper-backgrounds)


### Acknowledgement
____
I especially would like to thank my mentor Anthony Ngene, Arjan Speiard for their support throughout this project.