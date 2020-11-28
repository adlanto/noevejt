# NOEVE Jungle Tracker
The most Naive Jungle Tracker for your beloved video game. Please be aware that you are not allowed to use this tool in game. This will harm both your and your enemies gaming experience. This was for me just a fun project during the early days of the Covid-19 pandemic and I did never use it in public games. Still I think it might be interesting for game developers to get an insight what can be possible. 

Basic functionality: Template matching by OpenCV between the image of the enemy Jungler and the Map. If there is a high correspondence the Jungle Tracker will tell you the location of the target by creating Audios with by Google Text-to-Speech (gtts python package) and playing them. 

<p float="center">
  <img src="https://github.com/adlanto/no_eve_jungle_tracker/blob/master/docs/gui_start.png" width="500" />
  <img src="https://github.com/adlanto/no_eve_jungle_tracker/blob/master/docs/gui_ingame.png" width="500" /> 
</p>

For the basics of template matching refer to https://opencv-python-tutroals.readthedocs.io/en/latest/py_tutorials/py_imgproc/py_template_matching/py_template_matching.html
You will quickly understand the idea behind this naive algorithm.

The map is divied into 9 parts of non-equal size. The river areas are smaller than the ones closer to the base as they are assumed to be less relevant for the tracking of the jungler. These are the names the announcer will play in game.

<p float="center">
  <img src="https://github.com/adlanto/no_eve_jungle_tracker/blob/master/docs/map_division.png" width="500" />
</p>

## Professional and THE ONLY RECOMMENDED Usage:
The more interesting functionality of the tracker is the possibility to mine data of your games. This allows you to
- Enjoy the beauty of the data mined of your games in the /log folder
- See where all visible champions where on the map at specific timestamps
- Make your analysises and become a better competitor 

## Installation
I can not provide you the required templates here because first of they are copyright protected and second, more importantly, I do not want everyone to be able to use this tool. Again, this shall just give data lovers a playground. Thats the reason for not naming the used templates either. If you are really interested, you will find out from the code by yourself.
