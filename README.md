# Learning flashcard with Quackcard

### Video Demo: https://youtu.be/vUJAaRFw8i8

### Motivation
This project marks a significant milestone in my journey into computer science. It was my very first pet project, completed before I even entered college. Driven by pure curiosity about this field and inspired by what I learned from the CS50 course, I took on the challenge and brought it to life. I'm truly grateful for the insights and foundation that the CS50 course provided—it sparked a passion that continues to guide me today.

### Description
This is a web-based application that uses Python, SQL, HTML, CSS and Javascript which helps users to make flashcards and learn effectively. The website is built based on my personal experience. As someone who lives abroad and studies in my host country's language, I know how important language learning is. For me the flashcard method is one of the most effective and fastest learning methods that i have tried. Now let's dive deeper into this project!

**/login, logout and register**: With the flask session the users can register, login and logout of their own account. To avoid errors when malicious users try to access content they are not authorized to, some conditions have been added and notified to users so they know what to do properly.

**/index page**: The index page displays first to introduce users to the website, the method of learning with flashcards and some suggestions for using the website most effectively. Here i have used an available class of bootstrap accordion-flush to avoid showing the users too much information at once, but the users can still follow the content of the website.

**/decks**: First the users must create a new folder in /decks. With the z-index CSS property i created a container with 3 cards overlapping each other to represent a folder. The users can easily click on the folder name field to enter the name that they want for the folder and submit it via the + symbol. All folders that have been created will be shown in this /decks. The container for adding new folders will be always at the end of the row. Users can also edit, delete or go into the folder. With JavaScript getAttribute("hidden") and setAttribute("hidden", "hidden") the edit field will be hidden untill the edit symbol is clicked and hidden again when users click the edit icon.

**/cards**: When the users go into a folder that they have created, all cards in this folder wil be shown. The template is based on actual cards to create a user-friendly interface. Each of this cards also has features edit, delete or flip the card over and over separately. To add a new card i have used CSS class modal that simulates a real flashcard that users can flip it. Then when users click on + symbol the daten will be sent to Python and inserted into the SQL database or updated when users want to edit.

**/list**: Here provides users a table template to have an overview of all cards that they have created. First the users should select a folder from the selection field. With Jinja to combine HTML and Python i used some conditions and loop, so that when selecting a folder, users will be taken to the table containing all cards in this folder and the selected folder will be shown in the selection field. When the folder has no cards, it will show a notification. The users can also edit, delete or add card here. At bottom of the page there is a button to show and hide a text area that users can write a text and save it in SQL database.

**/learn**: Finally the users can learn all cards like in reality. Users select a folder and one card at a time from the first to the last card of the deck will be displayed. The card can be flipped or moved to the next or previous card if available. Users can also shuffle the deck in random order. Again button always brings the users to the top of the deck even if the cards are being shuffled. And the out button brings user back to the  field.
# Learning-Flashcard-with-Quackcard
# Learning-Flashcard-with-Quackcard
