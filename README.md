# PacMan Game
A PacMan duplicated game created using `python` and `pygame` by team No Name.

## Navigation
<a name="top"></a> 
1. [Game Description](#description)
2. [How to Install PacMan](#install)
3. [How to Play PacMan](#play)
4. [High-level Overview of Our Code](#overview)
5. [Documentation](#document)
6. [Extend our Code](#extend)
7. [Developers](#authors)
8. [License Information](#license)

## <a name="description"></a>Game Description

Do you absolutely love the famous 80s arcade game, PacMan? Then our version of PacMan is the perfect game for you!

PacMan is our Python implementation of the famous arcade game "PacMan". With a intricate blue-and-black theme, an intuitive interface, and easy installation, PacMan can be enjoyed by all ages.

PacMan uses a grid layout that forms the board on which the game is played on. The player moves the yellow PacMan using the arrow keys on their keyboard. The objective of this game, simply enough, is to get the highest score by eating all the pellets on the screen while avoiding making contact with the ghosts that gets increasingly aggressive in their pursuit of you.

The rules of PacMan are very straightforward; avoid the ghosts and eat all the pellets while trying to increase your score. The game ends when you have lost your 3 lives after being caught by the ghosts 3 times.

[Back to top](#top)

## <a name="install"></a>How to Install PacMan

We designed our game to be completely non-discriminatory, and we mean to other operating systems that is as we offer our game in all the operating systems that you could possibly need as you can see below and specific instructions for these operating systems will be outlined below.

### For `Windows`

We have made it as easy as possible for you to play our game. We have placed an exe of our fully functional game on our website. You may download it by clicking [here](https://pacmannoname.herokuapp.com/)

Once the game is downloaded, all you need to do is to unzip the folder and just run the `Welcome.exe` file which should look like the screenshot below.
![Imgur](https://i.imgur.com/i61t3Z8.png)

### For `Mac & Linux`

The installation process is, believe it or not, even simpler for Mac and Linux users. You would simply need to click the Mac or Linux download button from our website clicking [here](https://pacmannoname.herokuapp.com/) and our game will be downloaded as a single file that is completely compatible with the your operating system and will look like the screenshot below.
![Imgur](https://i.imgur.com/5ImjveY.png)

[Back to top](#top)

## <a name="play"></a>How to Play PacMan

All gameplay is controlled by the four arrows keys on your keyboard.
The title screen contains a "Ready!" button which you click when you're ready.
Click on the "Ready!" button to advance to the game screen.
![Imgur](https://i.imgur.com/sebSbVW.png)

The game screen contains a grid layout of the PacMan board with the pellets filling the space in between the walls.
![Imgur](https://i.imgur.com/mbh9VD3.png)

Use your arrow keys to move PacMan to eat all the pellets.
Important: There will be powerups scattered across the board that will allow you to temporarily eat the ghosts and gain additional points. This will turn all the ghosts a dark blue color and have a terrified look on their ‘face’ as shown below.
![Imgur](https://i.imgur.com/Gfii3Sc.png)

The game will automatically proceed to the next level when you have successfully eaten all the pellets on the screen.

[Back to top](#top)

## <a name="overview"></a>High-level Overview of Our Code

There are seven main files that run this game. Welcome.py is the first file that needs to be run to be able to open to game. This file creates the starting screen and runs Main.py. 

Main.py runs the class GameController which controls everything in the game. It controls the basic game loop, renders the game objects and updates the game. The remaining main files are the components of the game. Node.py contains the classes, Node and NodeGroup. A node represents the special point on the board, for example, the path and the wall, the portal and the starting point of PacMan and the ghost. 

The NodeGroup class is the basic grid of the board which is made up of the nodes. This grid is made up of reading the maze file. Next is the Entity.py file that contains the MazeRunner class. Class MazeRunner sets the movement of PacMan and Ghost. For Pacman.py, it contains the Pacman class that inherits the MazeRunner class. 

The Pacman class sets the movement and the position of the PacMan and checks the collision between PacMan and Ghost also between PacMan and pellets. For file Ghosts.py, it contains the Ghost class that inherits MazeRunner. Class Ghost sets the movement and the position of the ghosts. Lastly, file Pellets.py contains the Pellets and PowerPellets class. These classes set the position of the pellets and the power pellets.

[Back to top](#top)

## <a name="document"></a>Documentation

- Directory Structure  

`idea` : Folder containing .xml files  
`res` : Folder containing .png files  
`Main.py` : contains Python source code  
`animation.py` : contains Python source code  
`constants.py` : contains Python source code  
`entity.py` : contains Python source code   
`ghost.py` : contains Python source code  
`maze.py` : contains Python source code  
`maze.txt` : A text file containing maze drawing  
`maze_rot.txt` : A text file containing maze drawing  
`pacman.py` : contains Python source code  
`pellets.py` : contains Python source code  
`setup.py` : contains Python source code  
`sprites.py` : contains Python source code  
`stack.py` : contains Python source code  
`vector.py` : contains Python source code  
`welcome.py` : contains Python source code  
`welcome.spec` : contains Python project dependencies  

- Major classes and Methods

The `GameController` class contains all the logic behind the game.  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`update ()` : The update method is a method that we call once per frame of the game. It is basically the game loop.  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`render ()` : This method draws any object we need to be drawn on the game screen.  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`check_updater()` : This method checks for certain events that happen during gameplay.
    
The `MazeRunner` class contains all the logic needed for basic movement for characters in the game.

[Back to top](#top)

## <a name="extend"></a>Extend our Code

There are multiple ways this game can be extended to add additional features. One of the features is adding an additional player. This can be achieved by adding another PacMan instance in the stripe game load method and also modifying the scoring system accordingly.
Another feature is to change the look of the PacMan and the game board. PacMan’s look can be changed by using different stripe image while rendering the PacMan game board. Game board can be customized by editing the loaded text file to create more nodes, obstacles, etc.

[Back to top](#top)

## <a name="authors"></a> Developers of NoName

NoName is a group of 5 2nd year computer science students at the University of Toronto Mississauga. The team members are as follows:
Please note that each team member is followed by a paragraph letting you know about their personal contribution to the assignment.


-	Shau Ching Michael Li (username(s): Shau Ching Michael Li)

  In the coding part of this project I am in charge of written the classes of pellets. I have written three classes in the file pellets.py, class Pellets, class PowerPellets and PelletsGroup. All these classes set the position of the pellets and power pellets and render them on the map. In README, I am in charge of writing an overview of our code. In this part, I have introduced the main classes that runs the game and a description of the function of the classes.
  

-	Danesh Rajasolan (username(s): dannyb0yy)

  As for the code aspect, I implemented the decrease_lives method in the Pacman class and initialized the lives property to 3 for Pacman in the initializer method. I also implemented the start method in the Pacman class as well and this class sets the starting node for Pacman in the game. I have also implemented the start_position method in the same class. Lastly, I have also implemented quality checks for the entirety of the code by ensuring comments have been used as well as all methods and classes having valid docstrings and most importantly, changing all method names to pothole_case as it was using camelCase previously and pothole_case was the recommended type for Python code in the documentation. And as for the README, I documented how to install and play our game as well as the description of our game.


-	Akshit Goyal (username(s): akshitgoyal)

  Contribution to the README: In the README documentation, I was responsible for writing about extensions to the game. I listed down three additional features that another developer can extend to our game code. I chose these features because these are the first few features that one would want while improving their game. I also briefly discussed how to implement these features by referring to various segments of our game code. Contributions to the Code: In the game code, I have implemented the scoring system. The scoring system records and updates whenever a pellet or a special object on the board is eaten by the PacMan.I have also fixed the code quality. Since we are using Python to code this game, I have updated all the methods, functions and classes except the classes for ghost (done by Richard) according to the standard Python conventions. Specifically, I have updated the type annotations, return types, and documentation for classes, methods and functions. Finally, I have coded a website for this game. The website gives user a link to our github repository wherein the user can go and follow the install instructions to run the game. The website can be accessed through the following link: https://pacmannoname.herokuapp.com/


-	Mohammad Tahvili (username(s): tahvili, Mohammad Tahvili, brebeuftv)

  In this group project, I was responsible for writing the code for the game states. These states are made so the user can be instructed based on winning, losing, or starting the game. Throughout the assignment, I was also held responsible to help others on the team with their code. This was to make sure that everyone would be able to succeed in this project. I was also responsible for dividing the README sections equally between team members and assigned myself the task of selecting a license for our repository and communicate it clearly.


-	Richard Ekene Mba (username(s): laxat)

  In the code, I was responsible for the creation of the Ghost, MazeRunner and Pacman classes. These methods were vital in the assembly of all the character’s movements and their primary functions. Some ideas that I developed include, Pacman’s collision with pellets and ghosts, the ghost states that change during gameplay, and basic ghost AI.  In the README, I was tasked with writing up the directory structure of our group’s repository. I was also involved in some code quality augmentations and documentation.

[Back to top](#top)

## <a name="license"></a>License Information

The MIT License (MIT)

Copyright © 2019 NoName - All Copy Rights Are Reserved.

You can find a copy of the License at https://mit-license.org/

All images and branding used are from the original PacMan creators and we do not hold any rights for them.

License for them is in `Public Domain`

[Back to top](#top)
