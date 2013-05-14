Laser Asteroids
===============
[![Laser Asteroids Video](http://img.youtube.com/vi/5XTi-jf-ans/0.jpg)](http://youtu.be/5XTi-jf-ans)

Programmed for the 2012 [Georgia Game Jam](http://www.spsu.edu/games/gamejam/), 
Laser Asteroids utilizes the [Ether Dream](http://www.ether-dream.com/) 
DAC for laser projectors in order to project a game inspired by *Asteroids* onto 
a surface of choice. 

This game was developed on a 30Kpps Laser Projector, and I'm anxious to see
if it runs on any other setups. Any owners of the Ether Dream DAC are encouraged
to try the game and send me feedback. Patches are also welcome.

Libraries, etc. 
---------------
Laser Asteroids leverages the `PyGame framework` to capture input from 
videogame controllers. It was initially tested with a PS3 controller, but
development has continued with an XBox 360 controller. You may need to adjust
the bindings if you wish to run the code. (But that's easy enough.)

This project contain's Jacob Potter's GPL-licensed `dac.py`, which is also
[available on github](https://github.com/j4cbo/j4cDAC).

License
-------
Laser Asteroids is available under the MIT license. 

My other beginner laser projects 
--------------------------------
* [Laser Testbed](https://github.com/echelon/laser-testbed), 
  misc experiments including OpenCV, Graffiti Markup Language, 
  and more.
* [Laser Client](https://github.com/echelon/laser-client), 
  simple object shows that can cycle. Some parts are shared with 
  Laser Testbed, and much needs to be backported.

More sophisticated laser projects
---------------------------------
* [Light Engine](https://github.com/echelon/light-engine), a C++
  library for advanced laser projecting. Currently a work in progress.
