# DodgetheKar

# INTRODUCTION
This gaming python project is about dodging obstacles coming towards you in the form of cars.<br />
Here, pygame uses local images and sounds to run the game. Hence, it is important that the IDE is opened in the correct environment (i.e. the uploaded folder).<br />
Languages- Python: 100%<br />
Used python modules- Pygame  Time(sleep)  Sys   OS  Random<br />

# GAMEPLAY
The game begins with only one car coming towards you at a slow speed.<br />
With each passing level (except multiples of 5 i.e., levels 5, 10, 15 etc.) the speed of the cars increase and so does the player speed (going left and right).<br />
Every 5th level, the number of cars coming towards you is increased by 1 unit. The maximum number of cars is 8.<br />
The score increases with each successfully dodged car.<br />
An algorithm uses the current score to determine the level.<br />
The game could go on forever if the player doesn't lose.<br />

# CONTROLS
a) Intro-page:<br />
  i)  Escape- Quit window<br />
  ii) Space- Start Game<br />

b) Game area:<br />
  i)  Escape- Back to intro-page<br />
  ii) Right Key- Move Right<br />
  iii)Left Key- Move Left<br />

# FUNCTION DESCRIPTIONS
a) Main<br />
  Initializes the game resources and manages flow between Intro-page and game area.<br />
b) showIntroPage<br />
  This function displays the Intor-page, the name of the game and developer, runs background music.<br />
c) showGameArea<br />
  This function manages the entire flow of the game. It displays the game area, score, level, the cars and also provides them the necessary animation by using a FPS clock.<br />
d) checkCollision<br />
  Here, the co-ordinates of the player's car are checked against the co-ordinates of the obstacle cars. It returns true if collison occurs and false otherwise.<br />
e) modifyCars<br />
  This maintains a list of cars on the screen. New cars are generated using this function once the previous set of cars has a given difference (offset) from the top of the screen.<br />
f) increaseLevel<br />
  The various parameters defining a level (i.e., player speed, obstacle car speed and number of cars) is modified with each increasing level by this function.<br />
g) reset<br />
  This function is used to reset all the global variables once Escape key is hit in game area or if the player loses.<br />

#This is one of my first projects. So, please pardon the noobness, if any. :) 
