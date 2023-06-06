# Ecommerce Website
#### Video Demo:  <https://www.youtube.com/watch?v=wZQRqfGzehA>
#### Description:
#### **BOONT** is the name of my ecommerce Website, I had been thinking about how those website work and if could build something like that with what i learn until now, so i decide to be my final project.
#### From week 7 Mr David J. Malan made me so interesting in database and how we manage it, it was actually the best lecture for me so this website was a good practice for me.
#### **Now let me introduce my website**
BOONT is a flask app which built with (html, css, python with flask and jinja)
#### contains of the project:
#### DATABASE:
####
My database which is in store.db contains three tables:
* A customer table have all the users information with hashing the password for sure:
    customer ( id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, username TEXT NOT NULL, password TEXT NOT NULL, email TEXT NOT NULL, shipping_address TEXT);

* An item table which contain the products of the store with there informations:
    * for the images i save them just as a path because i heard a lot of ones says that if you save it as an image in the database it going to slow the process of getting data from the database
    item ( id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, name TEXT NOT NULL, description TEXT NOT NULL, quantity INTEGER NOT NULL, image TEXT NOT NULL, price REAL NOT NULL );

* An order table which will save all the orders of customers, connected with a FOREIN KEY with the customer table and item table:
    orders ( id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, customer_id INTEGER NOT NULL, item_id INTEGER NOT NULL, sold_quantity INTEGER NOT NULL, time TIMESTAMP DEFAULT CURRENT_TIMESTAMP, FOREIGN KEY (customer_id) REFERENCES customer(id), FOREIGN KEY (item_id) REFERENCES item(id) );

#### Static:
####
* /static : Is a directory of static files, my style.css and /img
    * style.css : Css file contains of the project all my css
    * /img : All images used in my project.

#### Templates:
####
* /templates : Is a directory of HTML files.
    * layout.html: HTML file with jinja contain the layout of the whole website, header and footer, i user here jinja in the header too for specifying waht the user can see in the header if he is loged in or not, for example a user who is not registered he should't have access to the profile and cart ... in the header.
    * register.html : A form that has action of "/register" for registering users by getting inputes like (email, username, password, confirmation of password, shipping_address) and a submit button, also there is a link that lead to the "/login" route if the user have an account.
    * login.html : A form have action of "/login" for submit the username and the password, with a link that lead to the "/register" route if the user doesn't have an account.
    * index.html : The home page which contain the items for sell, here i use jinja to implement a python loop for getting items from the database.
    * item_detail.html : which is rendered by the "/item/<int:item_id>" route show the detail of an item and let the user add to cart the quantity that he want if it's in stok.
    * cart.html : which contain all the items that the customer what buy, with the total price and the ability to remove an item,and the checkout button as well, the user can go to the cart page by adding an item to the cart or by clicking the cart icon located in the header.
    * profile.html : Is a simple profile page contain the user name, email, address and the ability to change the password.
    * change_password.html : A form to get the new password form the user for update it in the database.
    * apology.html : A page that i use when the user have an error.
    * success.html : A page that i use when the user do a successful checkout, NOTE ( i do not implement a payment get way so it is not really a successful checkout)

#### app.py:
I implement many route to make this website Functional:
* "/" : The home page route which select all the items form the item table and pass it to index.html.
* "/register" : Get the data form register.html via post, than ensure the data is valid, if the username is used before, hash the password, and add to the database.
* "/login" : Atart by forgeting any user id, than getting data via post, ensre data is valid, remember the user id to use it later
* "/item/<int:item_id>" : A route which takes by the item id as a parameter to Define which item the user click over, than pass the information of that item to item_detail.html.
* "/Addtocart" : Connected with the button Add to cart in item_detail.html used for get the item id and quantity that the user want buy and check if the quantity is available if it is he add the item to the cart.html and render the template with all his orders, he dose all that after verifying that the user is loged in if not redirect to "login".
* "/cart" : Connected with the cart button in the header, it render the template of cart.html with all the orders of the user.
* "/remove_from_cart/<int:item_id>" : It come with an input the item id to select in the databse the item that the user want delete, than it deleted form the table of orders, and than it select the other orders of the user to render the cart.html agin.
* "/checkout" : Connected with the checkout button, select the orders of the user and check if the quantity of item is valid than update the quantity in the database and clear the cart.html if the quantity is not vaild throw an error.
* "/profile" : Connected with the profile button in the header, it leads you to a simple profile page, where y can change the password as well.
* "/change_password" : Connected with the change password button in the profile page, for update the user password.
* "/logout" : Connected with the log out in the header for log out the user.
