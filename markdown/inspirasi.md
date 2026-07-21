have a whole bunch of images those you don't have to worry about at this point and we have a bunch of audio files those also don't matter too much at this point
7.27.34
0 detik
what you want to primarily work in is code and data and Via those try to finish the exercise see how far you
7.27.44
0 detik
get inside of the game class I want to create a setup method and for now I want
7.27.51
0 detik
to load the TMX map or in other words I want to create a local variable let's call it TMX map this I get via load pame
7.28.01
0 detik
where I want to go to data and Maps if I show this in the file explorer we want to go to data maps and there we
7.28.10
0 detik
have world. TMX this is the file we want to load world. TMX if you open that file
7.28.17
0 detik
by the way you are going to get something like this where we have three layers main decorations and entities on
7.28.26
0 detik
the main layer we have the actual level on decorations we have a whole bunch of well
7.28.33
0 detik
decorations and finally for entities we have the player start position this one up here and then we have a couple of areas all of those are for the warm
7.28.42
0 detik
enemies not too important for now so don't worry about it all that we care about at this point is decoration and
7.28.49
0 detik
Main to set up the level which means to get started I want for x y and the image
7.28.57
0 detik
in GMX map and get layer by name the layer that we want to load is called main since this one is a tile layer I
7.29.05
0 detik
want to add Tiles at the end that why I am getting XY and image decoded right away I want to create a very simple
7.29.13
0 detik
Sprite class in which we can add an X and Y position then the image and then the groups the groups we actually
7.29.21
0 detik
already have all Sprites and collision Sprites those we want to add in there right away s a tuple self. all Sprites
7.29.29
0 detik
and self. Collision Sprites also remember X and Y inside of tiled is a grid coordinate but we want to have all
7.29.38
0 detik
of this as a pixel position for that from settings we want to get the tile size and multiply it with both of those
7.29.46
0 detik
values with that we can create a basic Sprite for which I want to create a new python file Sprites
7.29.55
0 detik
dop in there we want from settings and import everything and then create a class called Sprite
7.30.03
0 detik
wave pygame dos sprite. Sprite then we will need a Dunder init method with self
7.30.11
0 detik
a position a surface and the groups afterwards we can call Super Thunder
7.30.19
0 detik
init and pass the groups right through self. image is going to be the surface
7.30.24
0 detik
and self. Rec will be self. image doget F rectangle in which we are going to
7.30.32
0 detik
place the top left wherever the position is that covers the basic spread class back inside of main.py I want from
7.30.41
0 detik
Sprites import everything that way this Sprite should be working all that we have to do is let
7.30.49
0 detik
me add another section load game in which we want to call self. setup and with that we get one part of the level
7.30.58
0 detik
that looks really good while we are here we can also duplicate those two lines because besides main we also have decoration which should only be in self.
7.31.09
0 detik
all Sprites there should be no collisions with those tiles but other than that this is all we had to do for
7.31.16
0 detik
this part after that I want for obj in TMX map and get layer by name
7.31.26
0 detik
entities that is an object layer on which we have the player starting position which we can identify via the
7.31.33
0 detik
name player or in other words I want to check if obj do name is equal to player
7.31.42
0 detik
and if that is the case I want to create a player class for now in there I want to have the position objx and obj doy
7.31.52
0 detik
then I will need self. all Sprites for the groups and self. collision Sprites for the collisions later we are going to
7.32.00
0 detik
add a bit more but that's not an issue for now I first of all want to create another class called layer and important
7.32.09
0 detik
for this one I want to inherit from Sprite the class that we have just created we will always need a thunder in
7.32.17
0 detik
it method and we need what we have specified here a position groups and collision Sprites self position groups
7.32.26
0 detik
and collision uncore Sprites then we will need Super thunder
7.32.34
0 detik
in nit and important now we are calling this thunder init method for which we will need a position a surface and the
7.32.44
0 detik
groups now we do have a position and a groups via the parameters that part is fine but we don't have a surface at the
7.32.52
0 detik
moment which is totally fine we can simply create a surface via pame do surface
7.33.00
0 detik
for now the dimensions are going to be let's say 40 and 20 also while we are here I want to create an attribute self.
7.33.10
0 detik
Collision unor Sprites is going to be Collision Sprites with that if I'm
7.33.16
0 detik
running main. Pi we can see a very basic player thingy although I think it should be
7.33.24
0 detik
quite a bit taller instead of 20 let's go with 80 that feels much more realistic that would be the basic player I want to call
7.33.33
0 detik
an update method with self and Delta time for which we are going to need self. move and this move method is going
7.33.42
0 detik
to consist of two parts the move method itself with self and data time and then
7.33.49
0 detik
we will need Define collision with self and E direction to get started with
7.33.56
0 detik
moving we want to get self. w.x plus equal self. direction which doesn't
7.34.04
0 detik
exist at the moment and for that we can actually create a movement and collision section which is going to contain Direction P game.
7.34.16
0 detik
Vector 2 that is a part we have seen a couple of times by now and also in this bit I want to have self. speeed for for
7.34.24
0 detik
this one I went with 400 with that we have self. Direction multiplied with self. speed multiplied
7.34.33
0 detik
with Delta time this I can duplicate because the next line should be self. r.y and I realized for X we want self.
7.34.42
0 detik
Direction dox and for y self. direction.
7.34.45
0 detik
y that way we have the horizontal and the vertical movement afterwards we have to call self. Collision with
7.34.54
0 detik
horizontal and vertical that would cover the basic movement to test all of this I want to
7.35.01
0 detik
have an input method in which we are getting the keys and then py game. key doget uncore rest at least for now I
7.35.11
0 detik
want to update self. Direction dox and set it to the integer of keys and py
7.35.19
0 detik
game. Kore right minus let me copy all
7.35.24
0 detik
of this and change K right to K left then we can duplicate all of this and
7.35.31
0 detik
then K down minus K up also we want to get self. direction and set it to self.
7.35.41
0 detik
direction.
7.35.43
0 detik
normalize if self. direction if that is not the case we simply want to get self.
7.35.49
0 detik
direction also before we are moving I want to call self.
7.35.54
0 detik
input with that if I run main. Pi the player can move around just fine that is
7.36.02
0 detik
looking pretty good for the collisions I want to check for sprite in self.
7.36.09
0 detik
Collision Sprites if sprite. rec. Collide wed with self.
7.36.18
0 detik
rectangle and by the way for this project you could be using hitboxes but you don't really need to if you want to
7.36.25
0 detik
add it do it in your own time afterwards if Direction is equal to horizontal then we want to check if
7.36.35
0 detik
self. direction dox is greater than zero then we know self. re. write should be
7.36.43
0 detik
equal to sprite. do left then we can duplicate all of this and check if the direction is smaller than zero in which case self.
7.36.55
0 detik
re. left should be sprite. re. right next up I want to duplicate all of this
7.37.02
0 detik
and then check the vertical collisions in which we want to check self.
7.37.06
0 detik
direction. y if this one is greater or smaller than zero if it is greater than zero we are moving down and want to
7.37.15
0 detik
check the bottom of the player if this one collides with the Sprite we want to set the bottom to the top of the Sprite
7.37.23
0 detik
and vice versa if the player is moving up and we have a collision then self.
7.37.28
0 detik
rec. Toop should be sprite. w. bottom if I now run around we're getting
7.37.35
0 detik
collisions with the level finally then we are going to need a camera for that
7.37.42
0 detik
inside of the code folder I want to add groups dopy as always we will need from
7.37.49
0 detik
settings and import everything then class all Sprites which is going to be a child of pygame Dos sprite.
7.38.00
0 detik
group a Dunder init method is always needed although this one without custom parameters and we want to call Super Dunder innit also self.
7.38.11
0 detik
displore surface is going to be py game.
7.38.15
0 detik
display and get surface that's the easy part besides that we want to have a custom draw
7.38.22
0 detik
method with self and a Target uncore position via this target position we
7.38.28
0 detik
want to influence uence self. offset on X and Y and at this point I realized I have
7.38.36
0 detik
forgotten to create self. offset this one is simply a pame vector 2 self.
7.38.43
0 detik
offset dox is going to be the negative value of Target position zero or the horizontal position of the player and
7.38.51
0 detik
from that we are subtracting window wi divided by two a very similar thing we want to do for self. offset doy
7.39.00
0 detik
except for this one we want to get the vertical position and subtract window height divided by two that way we
7.39.09
0 detik
are getting the offset for the camera that we can use with force sprite in itself and self. display surface. blit
7.39.19
0 detik
with sprite. image and sprite. rec. toop
7.39.25
0 detik
left plus self. offset with that back inside of main.py when we are calling
7.39.33
0 detik
all Sprites do draw we do not want to have the argument anymore and also when we are creating all Sprites this should
7.39.42
0 detik
be all Sprites and for that to work we have to add from groups import all Sprites
7.39.51
0 detik
nearly done the last thing that we have to do is when we are calling the draw method we have to get the player position but which we want to store the
7.40.00
0 detik
player in an attribute self. player is going to be the player Sprite and then
7.40.06
0 detik
self. player. re. Center let's try and
7.40.12
0 detik
we have a camera that is looking pretty good with that we have a basic setup via
7.40.19
0 detik
a few classes so I hope at this point this exercise wasn't impossible and if you could follow along you already know
7.40.27
0 detik
pame pretty well we have to Basics out of the way we can work on the platformer logic which is going to give us an
Segmen 25: Platformer logic
7.40.33
0 detik
actual platformer game and quite honestly we don't really have to make that many
7.40.40
0 detik
changes for the platformer movement the player is still going to control left and right movement however for up and
7.40.48
0 detik
down the player doesn't have control anymore instead we are using gravity and jumping or in other words we have to
7.40.55
0 detik
increase Direction doy by increasingly large number numbers that way it looks like the player is affected by gravity
7.41.03
0 detik
and when the player jumps we are setting Direction y to some static negative value and we'll talk about this in just
7.41.09
0 detik
a second in a lot more detail that being said though including Delta time with the full speed does include a bit more
7.41.17
0 detik
math which I want to avoid so we're going to set the frame rate to 60 frames per second although if you want to have the full platform experience check out
7.41.26
0 detik
this video in there I create a proper super nintend Nintendo style platformer including an Overworld if you have gotten so far you can follow along with
7.41.34
0 detik
this tutorial just fine back in the code first of all I want to update the frame rate and this I have actually already
7.41.42
0 detik
done because when we are calling the take method we are passing in the frame rate that we getting from settings. PI
7.41.49
0 detik
there we have a frame rate of 60 we already limited our frame rate which for a platformer can be a good idea it makes
7.41.57
0 detik
your math just a bit easier after we have that inside of the move method I want to add a comment with the
7.42.04
0 detik
horizontal movement this is the part we're not going to touch but we do have to make some changes to the vertical bit
7.42.12
0 detik
for now what I want to do if this is the player we should have a downward movement that is getting larger and
7.42.18
0 detik
larger the longer we fall just like real world gravity for that in the dunder init method of the player I want to add another attribute self.
7.42.29
0 detik
gravity which I have set to 50 before we are updating self. r.y I want to update
7.42.36
0 detik
self. Direction doy and increase this value by self. gravity multiplied with
7.42.45
0 detik
Delta time afterwards on the next line self. r.y is going to be increased by self. Direction although for this we
7.42.53
0 detik
don't need speed and Delta time anymore and what is happening now on the first line when then we are increasing self.
7.43.00
0 detik
Direction doy we are making this value larger and larger on every single frame because we keep on adding to the existing value on top of that this self.
7.43.11
0 detik
direction we are adding to the vertical position of the player that way we are falling at an increasingly large speed although if I
7.43.20
0 detik
run main. Pi we are well we are falling and we have collisions but if I keep on falling we are falling at a constant
7.43.28
0 detik
rate rate what is the issue here and well if you look at the player in the input method we are normalizing
7.43.38
0 detik
the direction Vector because of that all of these values are normalized or in other words the entire length of the
7.43.45
0 detik
vector never exceeds one fortunately that is very easily fixable we simply have to remove those two lines and then
7.43.52
0 detik
if I run main. Pi we are getting proper gravity although it's still not ideal
7.44.00
0 detik
let me run all of this again so we have some basic gravity but if I fall again we are falling really fast the issue for
7.44.07
0 detik
all of this is imagine that we have the player standing on a platform and also
7.44.15
0 detik
because of those two lines we keep on increasing the gravity on the first frame the
7.44.22
0 detik
player move down by this amount and then be constrained by the platform which is totally fine a few frames later we go a
7.44.31
0 detik
bit further down because of the gravity and we are still constrained by the platform however after some more time
7.44.39
0 detik
the gravity puts the player so far down that we are skipping the platform entirely as a consequence the player
7.44.46
0 detik
teleports right through and all of the collisions stop working we are simply moving too fast for them to fix that we
7.44.53
0 detik
want to work inside of the collisions specifically when the the rectangle bottom of the player collides with the
7.45.01
0 detik
top of an obstacle if that is the case then we also want to set self. Direction doy
7.45.10
0 detik
to0 with that if we are on the floor the gravity doesn't keep on increasing which means we get proper gravity and if I
7.45.19
0 detik
fall down again we get a much nicer gravity Behavior now other than that we can't really do very much but at least this
7.45.28
0 detik
part is working next up then I want to implement a jump mechanic for which inside of input I want to check if keys and py game.
7.45.40
0 detik
Kore space I want to set self. Direction doy to -20 with that inside of the game
7.45.50
0 detik
I can now jump around and this is giving us a very basic platformer that's looking really good but it's not ideal
7.45.58
0 detik
yet because the player can jump the entire time even if we are not on the floor so essentially we are
7.46.07
0 detik
flying which could be a nice effect but not what I want for this game we only want to allow a jump if the
7.46.15
0 detik
player is on the floor for that I want to add another attribute self.
7.46.21
0 detik
onore floor which by default let's set this one to fults and only allow a jump
7.46.29
0 detik
if we are pressing space and self dot on floor so how can we tell if the player is on the floor that part is going to be
7.46.38
0 detik
your exercise I want you guys to find a way to detect if the player is on the floor or not try to figure this one out
7.46.46
0 detik
on your own I want to work inside of the Collision
7.46.54
0 detik
method and effectively if we have a vertical Collision where the player is moving down then we
7.47.01
0 detik
are already setting Direction doy to0 that means we must be on the floor in other words self. on floor is going to
7.47.10
0 detik
be true although you also need to be careful here because at the moment we are only ever enabling on floor we are
7.47.19
0 detik
never disabling it or in other words if I now run main not Pi the player can still jump around in
7.47.28
0 detik
the air to fix that at some point we have to set self. on floor to false and this I want
7.47.37
0 detik
to do inside of the vertical movement before we are doing anything else in there self dot on floor should be false
7.47.47
0 detik
so that basically on every single frame of the game we are first setting on floor to false then we are doing all of
7.47.53
0 detik
this and inside of the collisions if the player collides with the floor then we are setting on floor to True once we
7.48.01
0 detik
have that inside of main Pi I can only jump if the player is on the floor so I keep on pressing space but we only ever
7.48.10
0 detik
get a single jump that being said I am not the biggest fan of this approach ideally before we getting the input I
7.48.18
0 detik
would want to self. check uncore floor and put all of this into a separate
7.48.27
0 detik
method which we can Al do fairly easily for that I want to have a check uncore floor method without any custom
7.48.36
0 detik
parameters also self. on floor inside of collisions and inside of move should
7.48.43
0 detik
disappear instead what I want to do inside of check floor I want to create a bottom rectangle which we're going to do
7.48.52
0 detik
via py game. F rectangle in which we first of all need a position this this can be 0 and zero
7.49.00
0 detik
we will change that in a second anyway and the width of this rectangle is going to be self. rect do WID and a height of
7.49.08
0 detik
two imagine this is the player and we want to check if this player is on the floor what I want to do for that is
7.49.17
0 detik
create another rectangle right below the player and check if this rectangle collides with any of the floor tiles and
7.49.26
0 detik
that rectangle is going to be the bottom rectangle although at the moment the position of this rectangle is off I want this always to be at the bottom of the
7.49.34
0 detik
player and for that we can add in another method move to because in there you can specify a specific point that we
7.49.42
0 detik
can place in my case this is going to be the mid top the position of this point
7.49.48
0 detik
should be self. rec. mid bottom so one of the limitations of py game. re or py game. F re is that we are always placing
7.49.57
0 detik
the top left so whatever Point you're specifying in here is always going to be the top left which very often isn't what
7.50.04
0 detik
you want and using move two is a really handy way to get around that so next up we want to check if this rectangle is
7.50.12
0 detik
colliding with any of the Collision Sprites for that you could write a for Loop but I prefer another approach the
7.50.21
0 detik
way I approach this I am first of all going to create a level rects list I want to use list comprehension and then
7.50.29
0 detik
get sprite. Rec for sprite in self.
7.50.34
0 detik
Collision Sprites that way I am getting a list of rectangles that Define the level and then I want to get the bottom
7.50.43
0 detik
rectangle and check Collide list with the level recks that we have just created and just to demonstrate what is
7.50.51
0 detik
happening here let me print the return value and then run main. Pi we are now
7.50.59
0 detik
getting 34 35 51 59 60 and seemingly a
7.51.05
0 detik
random integer what does it mean and also really important if we don't have a bottom Collision then we getting ne1
7.51.14
0 detik
essentially Collide list is going to look at the collisions between the bottom rectangle and the level rectangles and it's going to return an
7.51.21
0 detik
integer of the index of the rectangle that we are colliding with and if there's no Collision we getting negative one or in other words if we have a
7.51.30
0 detik
negative one then we know there's no Collision which means we can do something like self dot on floor is
7.51.39
0 detik
going to be true if we have a bottom wck with Collide list and this value needs
7.51.46
0 detik
to be greater or at least equal to zero if that is not the case else this value should be false once we have that the
7.51.55
0 detik
player can only jump if we are on the floor also we can refine all of this by simply passing the list comprehension straight
7.52.04
0 detik
into Collide list that way we are saving one line and the code feels a bit more elegant and if you want to have a more
7.52.13
0 detik
advanced platformer being able to detect collisions with the floor or the walls is really important so with this logic
7.52.20
0 detik
you could also very easily detect a collision with the left or the right side of the player but anyway there's just one more
7.52.28
0 detik
thing that I want to do back inside of the game there's one issue right now if I jump and we have a top Collision the
7.52.36
0 detik
player hovers in the air for just a bit which is a very strange effect if I find another area you can see it even better
7.52.45
0 detik
here if once again this is the player and the player is moving up because we are jumping and then we have some kind
7.52.53
0 detik
of top Collision we are stopping the player at the bottom side of this Collision but
7.53.00
0 detik
the player direction is still pointing up and it takes a while for Gravity to pull it down again that way it looks
7.53.08
0 detik
like the player is hovering in the air and this we can fix quite easily by
7.53.13
0 detik
setting self. Direction doy to Z if we have a top or bottom
7.53.22
0 detik
Collision that way inside of main. Pi I can collide with the top and to player fults down
7.53.30
0 detik
immediately and this is feeling a lot better and once again all of this can be
7.53.36
0 detik
organized just a bit better I want to remove the indent and cut out self.
7.53.45
0 detik
Direction then for self. direction being smaller than zero this should also not be indented anymore and all we really
7.53.53
0 detik
want to do is set self. direction if we have the vertical direction that way back inside of main. Pi we should be
7.54.01
0 detik
getting the same result let's try it here that is looking really good so this seems to be working pretty well
7.54.10
0 detik
perfect and also our code is feeling a lot more organized quite honestly there really wasn't that much of a change
7.54.17
0 detik
compared to a top down game although for the animations we do have to include a few more bits that's going to be the
7.54.24
0 detik
next section for the next part we are going to cover Imports and animations by the end of it we have a basic player
Segmen 26: Platformer animations
7.54.32
0 detik
animation and we also have the very basic enemies at this point the enemies don't do very much but that we can work on
7.54.40
0 detik
later and there isn't going to be that much new stuff for this section we are going to use basically the same animation logic that we have already
7.54.48
0 detik
seen the only change is that we have to update the state management for the player who account for the platform of logic that being said when we are doing
7.54.57
0 detik
the input ports I want to centralize them quite a bit more or in other words I want to have one method that loads all of the files and then we don't have to
7.55.06
0 detik
worry about it anymore inside of the game class I want to create a method
7.55.13
0 detik
called load uncore assets no need for custom parameters and in there I want to
7.55.20
0 detik
load all of the graphics and all of the sounds for example in there I want to have self. player frame
7.55.29
0 detik
which should be a list with the animation frames of the player or in other words to visualize all of this inside of images we have a very basic
7.55.38
0 detik
player animation it really doesn't do very much all of this we want to import for that I want to create a separate
7.55.46
0 detik
function import uncore folder in which we can specify the file path I want to go to images and in there we have the
7.55.55
0 detik
player this I want to import which which doesn't exist at the moment for which we want to create another python file let's
7.56.04
0 detik
call it support. Pi in there as always we will need from settings and import
7.56.12
0 detik
everything and then I want to start by creating an import image function this is not going to import an entire folder
7.56.21
0 detik
so we couldn't use it for the player import but what we could be using it for let me comment out the player stuff and instead I want to import self.
7.56.31
0 detik
bullet surface or in other words what we want to start importing is inside of images we have gun and there's bullet
7.56.40
0 detik
and fire I want to import the bullet for now via a more convenient method or in other words I want to run import uncore
7.56.49
0 detik
image with a file path we want to go to images then we want to go to gun and
7.56.57
0 detik
finally we want to go to Bullet notice here I am not specifying the file type we do not addpng at the end and that is
7.57.06
0 detik
intentional also what we are going to need is from support import everything
7.57.14
0 detik
that way we have this import image and first of all what I want in there is to unpack all of the arguments which are
7.57.21
0 detik
going to be the path so all of this stuff we want to have straight away and just so you can see what we are getting
7.57.29
0 detik
via this unpacking parameter I want to print the path and then call load assets which we have to do before we are
7.57.36
0 detik
calling the setup method self. load assets and now if I run all of this we getting a tupo with the three arguments
7.57.45
0 detik
we have specified and because of this unpacking parameter we can specify as many arguments as we want we are always
7.57.53
0 detik
going to get a tupal with all of them which we can actually use to create a full path right away using the join
7.58.01
0 detik
method we simply have to add the path in here although for that we want to unpack the path one more time that way we are
7.58.09
0 detik
splitting up this tupal into three values and then we can use it inside of the join method the end result is going
7.58.17
0 detik
to be if I print the full path we getting the full path to this file
7.58.24
0 detik
images gun and bullet that is looking really good although we are also going to need the file format this I want to
7.58.31
0 detik
be able to specify inside of the parameters in there I want to have a format and since we are almost always
7.58.39
0 detik
working with a PNG file this should be the default or in other words if we don't specify anything we should be getting a PNG file and to add that to
7.58.48
0 detik
Thea path I simply want to add an F string with Dot and then the
7.58.56
0 detik
format that way I can run main.py again and we are getting images gun and bullet.png that is working really well
7.59.05
0 detik
that we can now use to import a surface via py game. image. load with the full
7.59.14
0 detik
path and now we have to decide do we want to convert all of this or convert Alpha all of this which depends on the
7.59.22
0 detik
image having Alpha values or not which we cannot really detect meaning this has to be another parameter I want to know
7.59.30
0 detik
if there are alpha values inside of this image and by default I am going to assume that there are some because that's usually what you see and then run
7.59.39
0 detik
convert Alpha if Alpha is true and if that is not the case we want to run all
7.59.46
0 detik
of this once again except now only convert without Alpha and that is basically
7.59.54
0 detik
it at the end of all of this we want to return the surface and then we are getting the surface
8.00.01
0 detik
inside of this parameter I can print self. bullet surface run all of this and
8.00.08
0 detik
we are getting a surface we are still doing a basic import via py game. image.
8.00.13
0 detik
load but we are now adding a few more extra things to make all of this quite a bit more convenient not a major change
8.00.20
0 detik
but if you have to import hundreds of images this can be a massive difference and by the way all of this can be made quite a bit more elegant right away we
8.00.29
0 detik
don't actually need a surf variable we can return the surface from py game.
8.00.34
0 detik
image. load right away the result would be identical so with that we can import a single image much more elegantly
8.00.43
0 detik
besides that I also want to be able to import a folder for which once again we want to specify a path and unpack it
8.00.52
0 detik
right away via that we are going to import all of the player frames we are
8.00.59
0 detik
already calling import folder and getting images and player notice here this is a path to a folder not to an
8.01.07
0 detik
image so what we want to do is import all of the images inside of this folder I first of all want to create a local
8.01.16
0 detik
variable called frames and this has an empty list by default afterwards we want to do for
8.01.25
0 detik
folder uncore PA and then subfolders and finally file uncore names
8.01.32
0 detik
in walk join and then unpack the path this is the logic we have already seen a
8.01.39
0 detik
couple of times we are basically using the walk method to walk through a folder and get the folder path the subfolders
8.01.46
0 detik
and the file names in there I want to have for file uncore name in file
8.01.54
0 detik
names and then create a full underscore path which we're doing via the join
8.02.02
0 detik
method where we are getting the full folder path and then the file name via this we can create a surface with py
8.02.11
0 detik
game. image. load the full path and for this we basically always want to convert
8.02.19
0 detik
Alpha now you could make this a bit more flexible like we have done in import image and add a custom parameter
8.02.26
0 detik
although I don't think this is really necessary after that I want to get the frames and then append the Surface by
8.02.34
0 detik
the end of it I want to return the r with that back inside of main. Pi I
8.02.43
0 detik
can print self. player frames run all of this and we are getting a list of
8.02.51
0 detik
surfaces that is all we need for the player animation frames or rather the import of the player animation frames
8.02.59
0 detik
now this I want to change in two ways the first one is easy once again we don't really need this local surface variable we can simply append High game.
8.03.10
0 detik
image. load to frames straight away also since we're not using subfolders there should be an underscore besides that
8.03.18
0 detik
this slightly more important change is that I want to sorted the file names just to make sure that they are being
8.03.26
0 detik
imported in order for that we will need a key with a Lambda function where we
8.03.33
0 detik
have a name parameter and once again as a reminder what we're getting with the file name is something like
8.03.41
0 detik
0.png and we want to isolate the zero and turn it into an integer that way we can sort all of these
8.03.49
0 detik
values which means I want to create an integer get the name and split it wherever we have a DOT and then pick the
8.03.58
0 detik
first value the end result is going to be the same but in some cases it might prevent a bug but anyway with that we
8.04.06
0 detik
have the basic graphic Imports what we can now do besides the bullet surface we also want to have a fire uncore surface
8.04.14
0 detik
that we are getting via import image and we want to get images gun and fire next
8.04.21
0 detik
up I want to have self. bore frames which we're getting from import folder I
8.04.29
0 detik
want to go to images there we have the enemies and in there we have the b or in other words if you look at the images
8.04.38
0 detik
folder there we have enemies and the B frames there are only two images in there besides that we have the worm and
8.04.45
0 detik
this one looks really similar or in other words I can duplicate this line and then get the worm frames with images
8.04.54
0 detik
enemies and worm and that that is covering all of the Imports for the graphics now we have to figure out how
8.05.02
0 detik
to use them for that I want to work inside of the Sprites for a basic animation I want to have a class
8.05.11
0 detik
animated Sprite Which is going to inherit from the Sprite class that we have created so let me open it this is
8.05.19
0 detik
going to be the parent class which means when we are calling Thunder a it I want to specify besid self the frames a
8.05.28
0 detik
position and the groups after that when we are calling super thunder in nit we
8.05.35
0 detik
are calling this thunder init method for which we do have a position that we don't have a surface but then once again
8.05.43
0 detik
we have a group's parameter so we have to figure out this surface for that we need just a bit more information I want
8.05.51
0 detik
to have three attributes self. frames self. frame uncore index and self.
8.06.00
0 detik
animation uncore speed the values for all of them are going to be the frames
8.06.08
0 detik
parameter the value zero and for the animation speed I went with 10 once we have that inside of super Dunder init we
8.06.17
0 detik
can get the surface via self. frames and self. frame index that's basically it
8.06.25
0 detik
besides that I also want to have an animate method wave self and Delta time
8.06.32
0 detik
in there self. frame index plus equal self do animation speed multiplied with
8.06.39
0 detik
Delta time and self. image is going to be self do frames with an integer of
8.06.46
0 detik
self. frame index then modulus with length of self. frames that would be a
8.06.55
0 detik
really basic animated Sprite class and I hope you can see at this point why inheritance is quite useful for this
8.07.02
0 detik
class we never specify the image or the rectangle all of that is handled via the parent class and that system we're going
8.07.10
0 detik
to expand on quite a bit because animated Sprite is never going to be used inside of the game the only way
8.07.17
0 detik
that we are going to use it is as the parent class for the player and there we want to have the animated Sprite for
8.07.26
0 detik
that to work we have to make a few changes most importantly when we are creating one instance of the player I
8.07.34
0 detik
want to have a bunch of frames and also we don't want to have a surface anymore instead I want to pass the
8.07.43
0 detik
frames through to the parent class because now when we are calling this Stander init method we are effectively
8.07.51
0 detik
running all of this for which we are going to need frames positions and groups and I really realiz the order here is a bit messed up the first
8.08.00
0 detik
argument needs to be frames then we have the position and then we have the groups once we have
8.08.07
0 detik
that inside of main. Pi when we are creating the player instance we have to
8.08.14
0 detik
add one more argument self. player frames and now if I run all of this we
8.08.21
0 detik
have a very basic player image which isn't animated yet because we we are not
8.08.27
0 detik
calling the animate method that is a very easy thing to fix inside of update
8.08.33
0 detik
self. animate with Delta time after that we are getting the
8.08.41
0 detik
animation that is looking pretty good and once again notice here we didn't write any logic inside of the player for
8.08.50
0 detik
the animation all of that happens inside of the parent class which makes it much easier for us to organize all of this
8.08.58
0 detik
although truth be told we do have to override the animate method I want to have inside of the player Define animate
8.09.05
0 detik
with self and Delta time or in other words at this point from animated Sprite this method is not going to work anymore
8.09.14
0 detik
that is necessary because for the player we have to account for the different states for example if the player is not moving then we shouldn't have an
8.09.21
0 detik
animation but step by step first of all let's recreate the very basic logic I want to have self. image is going to be
8.09.30
0 detik
self. frames and then via the integer we are doing self. frame index
8.09.38
0 detik
modulus with the length of self. frames also we're going to need self. frame
8.09.45
0 detik
index plus equal self do animation speed multiplied with Delta time although this
8.09.54
0 detik
we only want to do if a certain condition is true in my case if self.
8.09.59
0 detik
direction dox is different from zero or in other words we only want to update the animation if the player is moving
8.10.06
0 detik
left or right with that back inside of main. Pi if I'm not moving we have no animation however once I'm going left or
8.10.14
0 detik
right the player is animating that is working quite well also if the player
8.10.20
0 detik
stops moving else then I want to set self. frame index to zero that way we
8.10.29
0 detik
are going back to the starting position let's try and I can move around if I'm moving
8.10.37
0 detik
we get the walking animation but if I stop moving the player is Idle the one major thing that is missing at this point is that the player is always
8.10.45
0 detik
facing to the right to fix that I want to inside of the dander init method add
8.10.52
0 detik
another attribute self. flip and by default this one is going to be faults next up after we have gotten the part
8.11.00
0 detik
from the animation I want to add another thing to self. image or in other words I want to run py game.
8.11.08
0 detik
transform. flip with self. image self.
8.11.13
0 detik
flip this is for the horizontal flip and for the vertical flip this one should always be false that why by default we
8.11.20
0 detik
are not going to get any change however if we are setting self. flip to
8.11.27
0 detik
through then the player is always going to be flipped with the animation still working just fine which means we just
8.11.35
0 detik
have to update this value in real time which we're doing inside of this if statement if we have movement or in
8.11.42
0 detik
other words if self. direction dox is different from zero then we want to set
8.11.47
0 detik
self. flip to self. Direction dox being smaller than zero this is going to
8.11.55
0 detik
return a Boolean value if if we are moving right it's going to be true if we moving left it's going to be false and this is then going to influence the flip
8.12.04
0 detik
method I can move to the right and to the left and we always get the proper facing Direction so this is working
8.12.12
0 detik
quite well the last thing that I don't like is that if the player is jumping we still are playing The Walking animation
8.12.19
0 detik
which looks really weird to fix that before we are doing anything in the image I want to check if not self. onf
8.12.29
0 detik
floor or in other words this if statement is checking if we are in the air and if that is the case self. frame
8.12.36
0 detik
index should be zero let's try now and if I'm on the floor we have the walking animation but if I am jumping we are
8.12.44
0 detik
getting the first frame so this is kind of working the issue is we don't want to have the frame with the index zero we
8.12.52
0 detik
want to have the index one that is going to look much better now it looks like the player is jumping which I like much better and
8.13.01
0 detik
this we can make just a bit more elegant I want to set self. frame index to
8.13.08
0 detik
one if the player is not on the floor if that is not the case else then we want to keep self. frame index and then we
8.13.17
0 detik
also don't need the other stuff anymore and that feels a bit nicer the end result though is still
8.13.25
0 detik
going to be just the same perfect and with that we have a very basic player animation which is getting
8.13.32
0 detik
us very close to a proper platformer to finish up all of this let's do an exercise I want you guys to
8.13.39
0 detik
do two things number one create a class for the be and to worm later on those two are going to behave differently so
8.13.46
0 detik
we will need two classes although both should animate from animated Sprite then create one instance of each in the level and really important for
8.13.55
0 detik
this one both of these enemies should be animated besides that write a function to import all of the audio files you
8.14.03
0 detik
don't have to play them at this point I simply want to have all of the files inside of the game that should be quite a bit of work pause the video now and
8.14.11
0 detik
see how far you get righty to get started with the enemies I want to create another class
8.14.20
0 detik
called e and this one for the parent is going to have an animated Sprite Which which means when we have the dunder init
8.14.29
0 detik
method we want to have a bunch of frames a position and the groups and then I
8.14.35
0 detik
want to call Super Thunder init in which we are calling this thunder init method
8.14.42
0 detik
for that we already have all of the arguments we need the frames the position and the groups and that is all
8.14.51
0 detik
we need to get started so inside of main.py when we are calling the setup method I want to create one instance of
8.15.00
0 detik
a b somewhere on the level for that we will need self. B frames the input for
8.15.07
0 detik
that we have done earlier this value here for the position let's go with 500 and 600 two entirely random values
8.15.17
0 detik
finally for the groups I want to have self. all Sprites for now after that if I run the game you can see we have one B
8.15.25
0 detik
inside of the level doesn't do anything at the moment but at the very least we have something and to animate this B you
8.15.33
0 detik
could simply write an update method inside of the class don't forget Delta time and then call self. animate with
8.15.40
0 detik
Delta time if you do that we have an animated B so this is all we needed for
8.15.47
0 detik
this part next up I want to copy all of this and then create a warm
8.15.55
0 detik
class which for now at least is going to stay identical to the b class which means inside of main. Pi I want to
8.16.03
0 detik
create a warm and for that we will need self. warm frames for the position let's
8.16.10
0 detik
go with 700 and 600 and then self. all Sprites I can run the game now and we
8.16.19
0 detik
are getting a warm somewhere in the air not perfect yet but that we can work on in the next bit before for that we want
8.16.28
0 detik
to import all of the sounds for which we could do something like import image or in other words we could wrap py game.
8.16.36
0 detik
mixer. sound in some other stuff to make it more efficient but I want to go a bit further I want to have self. audio and
8.16.43
0 detik
this is going to be a dictionary that will be created via audio importer the file path for this one is
8.16.51
0 detik
simply going to be audio this function doesn't exist at the moment so in inside of support. Pi I
8.16.59
0 detik
want to have audio uncore importer for which we need a path
8.17.05
0 detik
parameter that we are unpacking right away in there first of all I want to create an audio dictionary which doesn't
8.17.14
0 detik
have any values by default then once again I will need for folder uncore PA we don't care about
8.17.22
0 detik
subfolders so underscore and then file underscore names in walk join and unpacking the path in there we want to
8.17.31
0 detik
check for file uncore name in file names and now we don't have to sort the file names because we don't care about
8.17.40
0 detik
the order of the sound files this one simply doesn't matter I want to create a full underscore path via the join method
8.17.48
0 detik
I want to combine the folder path with the file name once we have that I can get the audio dictionary and then create
8.17.56
0 detik
create a key which should be the name of the audio file and I should actually explain so at the moment we don't need
8.18.03
0 detik
code data or images I want to look at the audio folder in there we have impact. OG music. wav and shoot.
8.18.13
0 detik
wav for this audio dictionary the key should be the name of the file without the file ending which I can get via the
8.18.22
0 detik
file name and then use the split method once again to split all of this wherever we have a DOT and then pick the first
8.18.30
0 detik
value that way we're getting the name of the file without the file ending and the associated value should be pame do
8.18.38
0 detik
mixer. sound with the full uncore path and that is literally it at the end of
8.18.45
0 detik
all of this we can return the audio dictionary and that we are capturing inside of self. AIO in other words if I
8.18.54
0 detik
print self. audio and run the entire game we are getting a dictionary with
8.19.01
0 detik
three sound files or rather three key value pairs the name of the file and then the sound object and to use that
8.19.09
0 detik
all we would really need to do for example to play the background music is self. audio and then the music with play
8.19.18
0 detik
inside of the
8.19.19
0 detik
[Music]
8.19.22
0 detik
game we are getting some music although this isn't something that I want to do because it would be really
8.19.30
0 detik
distracting anyway with that we have a whole bunch of imports and we have the player animations for the next section
Segmen 27: Creating timers
8.19.39
0 detik
we are going to add proper timers which are going to do quite a bit inside of the game for example we have a cool down for the bullets and every time the
8.19.47
0 detik
player shoots a bullet we have a short fire animation both of those things are going to be heavily influenced by the timers on top of that we have a repeated
8.19.56
0 detik
timer that creates a b enemy and all of this we want to have as flexible as possible or more generally games rely
8.20.04
0 detik
heavily on timers for example for this game whenever the player shoots a bullet we have a cool down we spawn a b every X
8.20.12
0 detik
seconds we have a fire sprite animation for a bit that gets destroyed after a few milliseconds and all of the enemies
8.20.19
0 detik
will die after 0.2 seconds after being shot for all of these things we will need a timer or other words ideally we
8.20.28
0 detik
want to have a reusable timer that can do number one be easily called anywhere it should also call a function
8.20.35
0 detik
on timeout and it should be repeatable and for all of this we have already seen the most fundamental Logic for a timer
8.20.42
0 detik
we are simply getting the current time subtract the start time and if the resulting value is greater than some duration we are doing something this is
8.20.50
0 detik
some very basic logic but this I want to expand upon and also at this point I do not want to use the build python events
8.20.57
0 detik
anymore because those just aren't that flexible and the system that we are going to create will be much better for
8.21.04
0 detik
all of that back inside of the code I want to create another python file timer. Pi first of all we will need from
8.21.13
0 detik
settings and import everything afterwards we have a timer class without any inheritance I want to have a Dunder
8.21.23
0 detik
init method with quite a few parameters the most important one will be the duration besides that we have a function
8.21.31
0 detik
with a default value of none then we have a repeat value also with a default value of none and we have an
8.21.41
0 detik
auto start parameter that by default is going to be false after that I want to
8.21.47
0 detik
set self. duration to the duration I want to set self. start time
8.21.55
0 detik
to Z and finally self. active is going to be false by are those three values we can
8.22.05
0 detik
create an update method in which we are fundamentally going to check if the
8.22.13
0 detik
current time minus self. start time is greater or equal to self. duration and
8.22.21
0 detik
if that is the case we want to do something now this is not going to work at the moment because we do not have the current time for that we would need py
8.22.30
0 detik
game. time.get Pi next up if this if statement does happen to be the case we want to run self.
8.22.40
0 detik
deactivate and while we are here I also want to create an activate method without any custom parameters so we want
8.22.48
0 detik
to have activate and deactivate for both of those methods for self. activate we want to have self.
8.22.56
0 detik
active being through and self. start time is going to be py. time.get uncore
8.23.05
0 detik
tick for deactivate we are going to do basically the opposite self. active will
8.23.12
0 detik
be BS and self. start time we can set back to zero and that is all you need
8.23.19
0 detik
for a basic timer to go over it really quickly by default we have the dander in it method and to activate the timer we
8.23.26
0 detik
are calling activate in there we're getting the start time which we are using inside of the update method and
8.23.34
0 detik
there we are checking the current time and subtracting the start time if the resulting value is greater than self.
8.23.42
0 detik
duration then we are calling self. deactivate which is going to set self.
8.23.47
0 detik
active to false and to start time to zero so with that via self. active we can check if this timer is active or not
8.23.55
0 detik
and the way you would be using that let's start inside of the player we don't need any of the other
8.24.03
0 detik
classes I want to work inside of the dunder init method and create a timer section for the player we only want to
8.24.10
0 detik
have a shoot uncore timer which is going to be the timer class we have just created and for that we have to import
8.24.18
0 detik
from timer import timer for now we can only set a duration 500 or half a second
8.24.26
0 detik
we working in milliseconds here next up when we are calling the input method I also want to check if keys and high
8.24.35
0 detik
game. Kore s that is the S key on the keyboard that I want to use for firing a bullet if that is the case
8.24.44
0 detik
shoot bullet if we run this without anything else I can press s and we're getting shoot bullet on every single
8.24.52
0 detik
frame of the game or in other words we will be shooting a bullet 60 times times per second which obviously would be way too many
8.25.00
0 detik
bullets so we are going to need a cooldown timer which we get via the shoot time or in other words we want to
8.25.08
0 detik
check two conditions if the player is pressing a button and self. shoot
8.25.15
0 detik
timer. active and also this should be self. shoot timer inside of thunder in it also also we want to check if this
8.25.23
0 detik
shoot timer is currently not active or in other words after the player shoots one bullet we want to get self do shoot
8.25.32
0 detik
timer and activate it so while the timer is running the player is not able to shoot a bullet just one more thing
8.25.39
0 detik
before we can use all of this the timer is only going to work if we are calling the update method which at the moment we
8.25.46
0 detik
are not doing for this self do shoot timer so nothing would happen to fix that inside of the update method before
8.25.53
0 detik
we are doing anything else self Dot shoot timer do update that way inside of the game if I
8.26.02
0 detik
hold down s we are only getting one bullet every 500 milliseconds and if I
8.26.10
0 detik
increase the duration to let's say 1,500 I can try all of this again and
8.26.17
0 detik
now we are getting much fewer bullets looking pretty good besides that inside of the timer I
8.26.25
0 detik
want to have three more things we want to call a function once this if statement triggers then we want
8.26.33
0 detik
to make the timer repeatable and be able to auto start all of this and auto start just to explain it basically activates
8.26.40
0 detik
the timer when we are creating it so we don't have to call activate on it to get started with the function I first of all want to store this as an attribute self.
8.26.51
0 detik
Funk is going to be Funk before we are deactivating the timer I want to check if self. Funk exists and if that is the
8.27.01
0 detik
case I want to call it although before we continue there's one more thing that I want to add self. start time is
8.27.09
0 detik
different from zero when we are getting started the start time is going to be zero and there is a chance that py
8.27.16
0 detik
game.get tick is also going to return zero which means all of this would be running and then we would trigger this one as well and Via this second
8.27.24
0 detik
condition we are avoiding all of that a fairly minor point but it can be a bit annoying anyway to test all of this
8.27.33
0 detik
inside of thunder in it of the game class I want to have a timer as well let's call this one the bore timer for
8.27.42
0 detik
which we will need a timer class that we don't have yet from timer import timer the duration of this one is going
8.27.51
0 detik
to be 200 and then we want to call a function self.
8.27.57
0 detik
creatore B this one doesn't exist at the moment so we have to create it Define
8.28.04
0 detik
create underscore B without any custom parameters inside of this method I simply want to create a b which we have
8.28.13
0 detik
already done so in there we have a b and once again don't forget we have to call before we are doing anything else self.
8.28.22
0 detik
B timer and I realized once again I have forgotten the self anyway after that
8.28.28
0 detik
self. b timer. update now this is still not going to work because this timer does not start by default what we would
8.28.37
0 detik
have to do is call Self dob timer.
8.28.43
0 detik
activate and let's add a slightly larger value so let's say after 2 seconds we want to call this method which would
8.28.51
0 detik
create one instance of a b if I run the game and and after 2 seconds we get a B
8.28.58
0 detik
this has worked really well with that we can do an exercise I want you guys to add the repeat and the auto start
8.29.05
0 detik
functionality to the timer pause the video now and see how far you get Auto starts is the easier part
8.29.15
0 detik
actually all we have to check for this one is if auto start is true then we want to call self. activate right away
8.29.24
0 detik
with that inside of main Hood pi we don't need this activate anymore instead when we are creating one instance of the
8.29.32
0 detik
timer I want to add auto start and set this one to true if I now run all of this we should still be getting a b and
8.29.41
0 detik
we do perfect besides that we have to work on repeat that should be an attribute self. repeat is going to be
8.29.51
0 detik
repeat and basically all that we have to do once all of this is running out and we are calling deactivate we want to check if self.
8.30.00
0 detik
repeat is the case self do activate that way inside of main.py for the B timer I
8.30.09
0 detik
want to set repeat to R and I guess to make all of this a bit more visible I
8.30.15
0 detik
want to have random values from random import Rand int and then for the B
8.30.23
0 detik
position for now I want to have a Rand ROM integer between 300 and 600 and the same
8.30.32
0 detik
I want to have for the Y position also for the timer I want to have a duration of 500 and now let's try all of this and
8.30.42
0 detik
we should be getting a whole bunch of bees that is looking really good perfect and I hope from looking at this thing
8.30.50
0 detik
you can tell that this is much better than the inbuilt python events we don't have to create a custom event or work in the event Loop we are simply creating a
8.30.58
0 detik
timer and then call a function whenever it times out and that's basically it nearly done there's just one more thing that I want to do because in actual
8.31.07
0 detik
larger projects what I ended up doing a lot is checking for self. shoot timer.
8.31.12
0 detik
active and this active you can get rid of you would need let's do it right below Dunder in nich we want to have
8.31.21
0 detik
Define Thunder pool this is is what's being called if you put this timer
8.31.28
0 detik
inside of an if statement the default functionality for this one is that you are always returning true which is not
8.31.35
0 detik
what we want to do in our case we want to return self. active that way inside
8.31.42
0 detik
of the player we can simply check and not self. shoot timer and the return value would be this timer being active
8.31.50
0 detik
or not active or in other words if I run main. pi and I press s and hold it down we are only getting shoot bullet every
8.31.58
0 detik
1.5 seconds I believe whatever we specified inside of the timer and well with that we have a really powerful
8.32.07
0 detik
timer that we can now use to add a whole bunch of things to our game right below the Sprites I want to create a class
8.32.15
0 detik
called bullet which for the parent is going to have a Sprite after that we will need Thunder a knit with self a
8.32.25
0 detik
surface a position a direction and the groups after that we have to call super.
8.32.32
0 detik
Thunder init in which we are calling this thunder init
8.32.39
0 detik
method for which we will need a position a surface and the groups besides that I want to have some extra stuff for the
8.32.48
0 detik
movement self. Direction needs to be an attribute and then we have self do speed
8.32.56
0 detik
which I have set to 850 besides that we will need an update method with self and Delta time and then call self.
8.33.07
0 detik
r.x plus equals self. Direction multiplied with self. speed multiplied
8.33.14
0 detik
with Delta time so with that we have a very basic bullet that we now want to create whenever the player presses the S
8.33.23
0 detik
button and the timer isn't active also the bullet we want to have inside of
8.33.30
0 detik
another Sprite group self. bullet unor Sprites pame dos sprite. group this is
8.33.39
0 detik
the part we have seen plenty of times by now to create a bullet below create B I want to have create underscore bullet
8.33.49
0 detik
for the parameters we will need a position and a direction both of those we are going to get from the player
8.33.56
0 detik
although for now I simply want to create a bullet where we already have a surface
8.34.03
0 detik
self. bullet surface we imported this inside of load assets not too long ago
8.34.10
0 detik
for the position and the direction we are simply going to use the parameters finally for the groups I want
8.34.17
0 detik
to have a tupal with self do all Sprites and self. bullet Sprites this create
8.34.24
0 detik
bullet we now have to add to the player I want to have self. create bullet inside of the player for that to work
8.34.34
0 detik
back inside of the Sprites the player is going to need one more parameter create uncore bullet I suppose we can store
8.34.42
0 detik
that one as an attribute right at the top create underscore bullet it's going to be create bullet and this create
8.34.51
0 detik
bullet we want to call instead of the print statement create bullet and then we are going to
8.35.00
0 detik
need a position and a direction for the position at the moment I simply want to get self. rect do Center and for the
8.35.09
0 detik
direction this one should be -1 if self do flip and if it is not the
8.35.18
0 detik
case else it should be one or in other words if the player is facing to the left then we are returning -1 and if not
8.35.25
0 detik
not then we are facing to the right so the Bullet should have a direction of one let's try all of this and if I press
8.35.32
0 detik
s we are getting a bullet not too many because the timer cool down is really large but at least we're getting
8.35.41
0 detik
something I suppose for that we can change the cool down to 500 milliseconds that way all of this is
8.35.49
0 detik
going to feel quite a bit better next up the main issue we have at the moment is that the bullet is always facing to
8.35.58
0 detik
the right because we are not making any updates to the surface for that I want to have an
8.36.06
0 detik
adjustment section where we are updating self.
8.36.12
0 detik
image all we need in here is py game. transform. flip with self.
8.36.21
0 detik
image and then for flip X the only thing that we really care about we want to get direction and check if this value is
8.36.28
0 detik
equal to1 or in other words this is only going to be true if the bullet is going to the left or flip y we want to have
8.36.37
0 detik
faults if I now run main. pi and I look to the right we get a bullet facing to the right and if I face left the bullet
8.36.45
0 detik
is also facing left although if you look at the player the starting position of the bullet just isn't
8.36.51
0 detik
ideal or in other words the way you have the issue happens because if this is our
8.36.59
0 detik
player the starting position is always the center and the point we are placing for the bullet is the top left we would
8.37.07
0 detik
always get something like this which really is not ideal to fix that I want
8.37.13
0 detik
to work inside of create bullet and create a custom x value I always want to
8.37.21
0 detik
get the original player Center position or position zero to that I want to add the direction and
8.37.30
0 detik
multiply it with a value that I think is large enough after some testing I landed on 34 but this we only want to do if
8.37.40
0 detik
direction is equal to one or in other words we are going to the right if that is not the case else we still want to do
8.37.49
0 detik
all of this but then we also want to account for the top left position in other words sell dot bullet surface and
8.37.58
0 detik
then get whiffed after we have that instead of the position I want to have a
8.38.04
0 detik
tupal with X and position one just to test all of this inside of Sprites I want to set the bullet speed
8.38.13
0 detik
to zero if I now run main. pi and I look to the right I can create a bullet it's right in front of the player and on the
8.38.22
0 detik
left side we are also right in front of the player player that means we can set the bullet speed back to
8.38.30
0 detik
850 and we get bullets that look significantly better cool now to understand this line we have a player
8.38.39
0 detik
with a center position that is what we're getting from the position parameter if the player is facing to the
8.38.46
0 detik
right then we want to do all of this meaning we are going from this point a bit further to the right by 34 pixels
8.38.56
0 detik
and then we are placing the top left of the bullet I think that part is fairly straightforward however if we are moving
8.39.04
0 detik
to the left then we are doing all of this we still start from the center of the player and then we are going to the
8.39.12
0 detik
left by 34 pixels that covers this bit but then you have to remember that we are placing the top left of the bullet
8.39.20
0 detik
meaning the bullet would be roughly here which obviously is wrong what we want to place is the right side of the bullet in
8.39.29
0 detik
other words we want to move the entire thing by its own width and this we're doing with this last
8.39.35
0 detik
line and that is basically it with that we have the bullets that covers all we need for this
8.39.42
0 detik
class besides that I also want to have a fire class which is also going to inherit from the Sprite class now for
8.39.51
0 detik
this one we first of all want to have a thunder init method with self a surface a position groups and we also need the
8.40.01
0 detik
player basically for this one every time the player fires a bullet we also want to have a fire animation or well fire
8.40.10
0 detik
animation might overstate things just a bit if you look at images scun there we have a fire image this we want to show
8.40.19
0 detik
for a very short amount of time if the player fires a bullet and then via a timer destroy it right after and for
8.40.27
0 detik
that we're going to need the player so this fire animation moves with the player it would look really weird if it didn't do that for that we will need a
8.40.36
0 detik
super Dunder init method with the surface the position and the
8.40.44
0 detik
groups that way we are getting all of this on top of that I want to store self. player as an attribute and also I
8.40.53
0 detik
want to know when we are creating all of this if the player is flipped or not which means self. flip will be player.
8.41.01
0 detik
flip on top of that I want to create self. timer which is going to be a timer
8.41.08
0 detik
that has a duration of 100 and it's also going to auto start and once this thing
8.41.16
0 detik
times out we want to call a function which is going to be self. kill we want to call the inbuilt kill method of the
8.41.24
0 detik
Sprite which we can totally do let's try all of this inside of main.py besides creating
8.41.31
0 detik
a bullet I also want to create a fire instance for the surface I want to have a fire surface for the position for now
8.41.41
0 detik
let's stick with the position of the player groups is simply going to be self. all Sprites and the player will be
8.41.48
0 detik
self. player if I now run all of this we are getting an error that Tuple object
8.41.54
0 detik
has no attribute get F rectangle and I think that usually means we are adding some wrong arguments somewhere you
8.42.03
0 detik
probably saw it already the order of the arguments are wrong we first of all need a position then we need a surface and then we need
8.42.12
0 detik
the groups if we now run out of this we are getting a fire Sprite that is pointing
8.42.20
0 detik
mostly in the wrong direction and the position is also not great but at least we have something oh and on top of that
8.42.27
0 detik
it also doesn't disappear that happens because the timer is not being updated which means we need an update method
8.42.34
0 detik
with self and Delta time although Delta time we don't care about and then self. timer.
8.42.41
0 detik
update if I now run all of this I can shoot a bullet and we get a very short fire animation that's a good start but
8.42.51
0 detik
we also have to update the position for that since we have to player available we can do all of that fairly easily if self. player.
8.43.02
0 detik
flip then I want to set self. re.
8.43.06
0 detik
midr to self. player. re. mid left on top of that since we are now facing to
8.43.13
0 detik
the left we want to flip the entire fire image or in other words self. image is going to be py game.
8.43.23
0 detik
transform. flip with self. image true and
8.43.29
0 detik
false if that is not the case else then we simply want to set self. do midle to
8.43.38
0 detik
self. player. re. Mid right that is a good start but on top of that I want to
8.43.44
0 detik
copy all of this and then inside of the update method do all of this except updating the image that way this fire
8.43.53
0 detik
animation goes along with the player which is quite important if I now fire all of this you can see that we have a
8.44.03
0 detik
basic fire animation although the position is a bit off this thing has to move down just a little bit that is
8.44.10
0 detik
quite easily done inside of Thunder init I want to have self. let's call it y off
8.44.17
0 detik
set which is going to be a pame do Vector 2 with zero and let's say eight
8.44.24
0 detik
pixels after we have that whenever we are updating the position of the rectangle we always want
8.44.33
0 detik
to add the Y offset that way if I shoot the bullet we get the proper nozzle fire
8.44.41
0 detik
animation and that is looking pretty good and I think now I can also demonstrate why you need this part if I
8.44.50
0 detik
comment it out and run main dop again and shoot a bullet sometimes you can see if the player is
8.44.57
0 detik
moving the fire animation doesn't move along with the player which is kind of a weird effect meaning we really want to include
8.45.05
0 detik
this part nearly done there's just one more part I do want to work on let me move away from the bees and if I shoot a
8.45.14
0 detik
bullet and turn right away we getting a slightly weird effect when we are creating the fire animation and the
8.45.22
0 detik
player is facing to the right and if we are then turning around the entire thing falls apart to avoid that if the player turns
8.45.31
0 detik
around while we have a fire animation we want to Simply destroy the entire thing or in other words if self. flip is
8.45.41
0 detik
different from self. player do flip if that is the case self. kill that way if I run main.
8.45.51
0 detik
Pi I can move a bit further to the right and as soon as as I shoot and turn around the fire
8.45.58
0 detik
disappears and with that we have the fire animation that covers another really important part with that covered we just have to figure out the enemy
8.46.07
0 detik
logic and the bullet
Segmen 28: Bees and worms
8.46.11
0 detik
[Music]
8.46.14
0 detik
collisions to finish up the game I want to work on the enemy Logic for the B we want to have a Sprite that is slowly
8.46.21
0 detik
moving to the left we have some vertical movement as as well and for the worm we are going to move this thing in the predefined area on top of that we will
8.46.31
0 detik
also add the collisions between the bullets and the enemies and the enemies and the player finally we can add some audio files and then we have the entire
8.46.39
0 detik
project done shouldn't be too difficult for all of this back inside of the code I want to work inside of the Sprites and
8.46.48
0 detik
looking at all of this we don't need the timer. piy groups. piy or support. piy file anymore instead we want to look at
8.46.55
0 detik
the worm and the bee those two classes are identical at this point on top of that they are going to share a bit more
8.47.04
0 detik
code in just a bit to account for all of that I want to create another class called
8.47.10
0 detik
enemy which is going to have an animated Sprite as the parent for this we going
8.47.17
0 detik
to need a thunder init method with self braams position and groups in there we
8.47.26
0 detik
are going to need Super and thunder in knit which means we are calling animated Sprite thunder in it and then pass
8.47.35
0 detik
through all of the arguments which means for the B the parent class should be the enemy class and the same for the worm
8.47.43
0 detik
that already means inside of the enemy class we can call update with self and Delta time and then self. animate also
8.47.53
0 detik
with Delta time because of that we don't need this update method anymore and we are already simplifying the code inside
8.48.02
0 detik
of m.p the animations should still work and they do cool for both of these
8.48.09
0 detik
classes I want to create a move method which is also going to need Delta time and for now we're going to add pass in
8.48.17
0 detik
there for both of them this move method we are going to call inside of the parent class cell do move now we have to
8.48.26
0 detik
figure out the actual movement for the B this is fairly simple we want to have self. rect dox minus some amount for
8.48.37
0 detik
that value I want to create self. speed which is going to be random and this we want to multiply with Delta time for
8.48.45
0 detik
that to work we will need self. speed which is going to be set by a parameter
8.48.52
0 detik
speed with that back inside of main. Pi when we are creating a b we will need one more argument also to organize all
8.49.01
0 detik
of this just a bit better I want to use named arguments we have frames we have a
8.49.09
0 detik
position and then we have the groups besides that we will need speed which is
8.49.16
0 detik
going to be a random integer between 300 and 500 if I now run all of this we have
8.49.23
0 detik
pce that are moving to the right so this is already working quite well perfect although now the starting position
8.49.31
0 detik
doesn't really work anymore what I want to have if this is the entire level the bees should be spawning on the right of
8.49.39
0 detik
it for that first of all when we are setting up the level we need to know how
8.49.45
0 detik
wide this TMX map is we need TMX map and then do whift if I now run all of this
8.49.53
0 detik
we are getting the number 45 to understand this value you want to go to the tile map and then map and map
8.50.02
0 detik
properties that is going to give you this dialogue on the left and all the way at the top you can see the width
8.50.09
0 detik
which is 45 in my case or in other words our map has 45 columns that's literally
8.50.16
0 detik
all that this means which we can use I want to define a self. levore for
8.50.25
0 detik
whift which is going to be TMX map. wift multiply it with the tile size once we
8.50.31
0 detik
have that back inside of create B for X we want to have self. LEL wift plus some
8.50.40
0 detik
kind of offset let's go with the window whift just to be sure and since the player cannot see this value anymore we
8.50.48
0 detik
don't need Randomness meaning Rand in and disappear that is looking pretty good if
8.50.56
0 detik
I now run all of this and I move all the way to the right at some point there should be some bees coming our way and
8.51.04
0 detik
that is working pretty well next up we also want to cover the entire height of the map meaning we have to do basically
8.51.11
0 detik
the same thing we have done before besides a level Whi I want to have self.
8.51.17
0 detik
levore height which is going to be TMX map. height multiplied with the tile size
8.51.26
0 detik
after that for this value we do need Randomness we want to have a value between zero so all the way at the top
8.51.33
0 detik
and self. level height once we have that I can run the game and at some point we
8.51.41
0 detik
could be seeing bees covering the entire height and that is working pretty
8.51.49
0 detik
well although for the movement of the bees I want to add a bit more randomness
8.51.55
0 detik
and for that I want from math import sin this is giving us a signed function and
8.52.03
0 detik
what that is doing if you put this on a graph we need some kind of x value and
8.52.12
0 detik
along this value the sign function is going to look something like this we basically get a wave that fluctuates
8.52.19
0 detik
between 1 and -1 and in our case the x value is going to be the time and just to demonstrate what we are going to do
8.52.28
0 detik
inside of the player I want to in the update method
8.52.34
0 detik
print the sign function with pame do time.get ticks if I now run all of this
8.52.43
0 detik
you can see that we getting a whole bunch of output and this output is always between nearly one and then
8.52.51
0 detik
nearly -1 and it goes between those two values really really quickly that is all that we are doing in
8.52.59
0 detik
here now in the player we don't need it but inside of each instance of the
8.53.06
0 detik
B we want to use all of that to influence self. doy to that value we want to add the sign value of py game.
8.53.17
0 detik
time.get six don't forget to call it and this value will now be between 0 and 1
8.53.24
0 detik
which is not going to do very much for the vertical position but we can multiply it with some sort of
8.53.33
0 detik
amplitude and also don't forget whenever we have Movement we have to multiply things with Delta time now amplitude
8.53.40
0 detik
doesn't exist at the moment although we can create it self. amplitude is going to be a random integer that we have to
8.53.49
0 detik
import from random import Rand in I want to have a random value between 500 and
8.53.57
0 detik
600 with that if I run all of this again and we have to wait for the Beast for just a second we should be getting
8.54.06
0 detik
something and well this is kind of working but it's not ideal yet that is because the frequency is way too high to fix that I want to have self.
8.54.18
0 detik
frequeny which is also going to be a random integer in my case between 300
8.54.24
0 detik
and 600 and this value we want to use to divide get. tick or in other words divide by self do
8.54.33
0 detik
frequency with that we should be getting a proper outcome if I now Run the game
8.54.40
0 detik
and we could be seeing bees moving in a much more organic way this is much
8.54.49
0 detik
nicer perfect that covers the movement of the be next up I also want to have a
8.54.56
0 detik
constraint because once again we keep on creating bees and we have to make sure that we are getting rid of them at some point as
8.55.04
0 detik
well now in this case this is fairly simple we simply want to check if self.
8.55.11
0 detik
re. right is smaller or equal to zero if that is the case we want to kill the
8.55.19
0 detik
Sprite and also this constraint method we want to call inside of the parent class self.
8.55.26
0 detik
constraint to make sure that the game doesn't crash we also have to add the same method to the worm class meaning in here
8.55.34
0 detik
con straint without without any custom parameters and this one is going to get pass for now with that we have to be
8.55.43
0 detik
enemy next up we have to work on the worm inside of til we have an object layer called entities this one contains
8.55.52
0 detik
the player that's the part we have already seen besides that we have a whole bunch of rectangular
8.56.00
0 detik
areas and the way those are going to work I want to spawn a worm roughly here
8.56.07
0 detik
and then make it move to the right if the worm goes too far to the right let's say we are ending up here then the
8.56.15
0 detik
direction of this enemy should be reversed the same thing we want to do on the left side and I think you know where this is going this is going to be your
8.56.23
0 detik
exercise I want you guys to create the worm movement logic pause the video now and see how far you
8.56.32
0 detik
get first of all we have to import all of the areas that is going to happen inside of setup after we are creating
8.56.41
0 detik
the player now we already are creating one instance of the worm that we want to keep however first of all we want to
8.56.49
0 detik
check if obj do name is equal to worm and just to make sure if you go back to
8.56.56
0 detik
tiled and you click on one of these areas you can see name worm if that is the case we want to create one instance
8.57.05
0 detik
of the worm and then add a couple of arguments the frames can stay as they are and at least for now we can also
8.57.13
0 detik
keep the groups but we have to update the position this one simply doesn't work anymore and what I want to do
8.57.20
0 detik
instead is create a pame f rectangle with the size of the rectangle inside of
8.57.27
0 detik
til that we can get via obj dox obj do y
8.57.32
0 detik
obj do width and obj do height with that we have a rectangle that defines the
8.57.40
0 detik
area that the worm can move in although to use that inside of the worm we need to update the parameters instead of a
8.57.48
0 detik
position we now have a rectangle to turn that into a position at least for the super under init method we want to get
8.57.56
0 detik
wreck. top left and that should already do something if I now Run the game we're
8.58.03
0 detik
getting multiple worms and they are in the area position at least roughly now obviously the worm should always be on
8.58.12
0 detik
the ground for that I want to update self. w. bottom
8.58.19
0 detik
left and set it to rect dot bottom left that way the worms are always going to
8.58.27
0 detik
be on the floor which is already feeling a lot better I also want to keep the rectangle let's call it maincore
8.58.36
0 detik
rectangle this is just going to be the rectangle from the parameter after than that we want to have self. speed which
8.58.43
0 detik
can be a random integer between 160 and 200 also we will need self. direction
8.58.52
0 detik
which can be one by default afterwards for the move method I want to get self. dox plus equal self. direction
8.59.02
0 detik
multiplied with self do speed multipied with Delta time with that since we are already
8.59.10
0 detik
calling the move method all of the worms are moving to the right which is a good start but not ideal yet because they are
8.59.19
0 detik
supposed to turn around for that we will need the constraint method and the basic logic just to reiterate if this is the
8.59.27
0 detik
area the worm is starting in the bottom left and also moves to the right if we are then outside of this area we want to
8.59.36
0 detik
go the other way now for that you could check if the right side of the worm is greater than the right side of the area
8.59.44
0 detik
and do the same thing for the left side although that would be a bit of an Overkill because what we can do instead
8.59.51
0 detik
is to check if not self do main rectangle do contains with self.
9.00.00
0 detik
rectangle this way we are checking if the rectangle is not entirely contained by the main rectangle anymore which can
9.00.08
0 detik
only happen if we are too far to the left or too far to the right if that is the case self. Direction multiply equal
9.00.16
0 detik
minus one with that we should be getting the proper constraint this is looking really good
9.00.26
0 detik
just one more change that we have to make whenever we are doing this we also want to invert all of the frames so that
9.00.34
0 detik
it looks like the worm is moving in the right direction all we have to do for that is overwrite self.
9.00.40
0 detik
frames which we can do via py game.
9.00.43
0 detik
transform. flip and in there we want to get a Surface and then true and false
9.00.50
0 detik
this we're doing for every surface in self. frames once we have
9.00.57
0 detik
that we're getting the proper animation and that is looking pretty good now once again this could be optimized just a
9.01.05
0 detik
little bit more because now inside of the game every time the worm is hitting a specific point we are transforming two
9.01.13
0 detik
surfaces what you could do instead inside of load aets load the worm frames and then invert them right inside of
9.01.21
0 detik
this method afterwards you can simply load the right frames depending on what you have inside of the worm that would
9.01.28
0 detik
also work but for this game it's not too much of an issue and I think at this point if you want to implement it you can do it on your own anyway with that
9.01.37
0 detik
we have both of the enemies which means now we can work on the Collision
9.01.45
0 detik
methods Define collision and those are going to be the collision between the bullet and the enemies and the enemies and the player
9.01.53
0 detik
first of all I want to have the collision between the bullets and the enemies for bullet in self. bullet
9.02.04
0 detik
Sprites and then get all of the Sprite collisions which we're getting via pame
9.02.10
0 detik
dos sprite. Sprite cite in there we want to get one bullet and then self.
9.02.19
0 detik
enmore Sprites this one doesn't exist yet we will change that in just a second finally we will need to kill which
9.02.28
0 detik
should be false now before we can continue we want to work inside of the dunder init method
9.02.36
0 detik
and then create the enemy sprite's group this we want to use both for the
9.02.43
0 detik
worm and for the bees meaning those should be in self. all Sprites and self.
9.02.50
0 detik
enemy Sprites the be we are creating inside of the create B method and in there for the
9.02.57
0 detik
groups I want to have all Sprites and self. enemy Sprites with that this line should be
9.03.05
0 detik
working and I suppose while we are here we can also add py game.
9.03.10
0 detik
sprite. polite mask right away next up we want to check if Sprite
9.03.18
0 detik
Collision then we want to get the bullet and kill it and for Sprite in Sprite Collision we want to call sprite.
9.03.30
0 detik
destroy once again this method does not exist but that we can change because inside of the enemy
9.03.38
0 detik
class we can have Define destroy which for now is simply going to call self. kill all we have to do now is
9.03.48
0 detik
after we recording all Sprites update self.
9.03.52
0 detik
Collision let's try all of this now and if I shoot at one of the worms they disappear this should also work a second
9.03.58
0 detik
time perfect and once I hit a b there we go this is also working although this I
9.04.06
0 detik
want to refine a bit by using a mask inside of the enemy or in other words first of all I want to create self.
9.04.17
0 detik
Deathcore timer which is going to be a timer with a duration of 200 milliseconds
9.04.24
0 detik
and the function self. kill as soon as we are calling the destroy method we are starting this timer self. death timer.
9.04.34
0 detik
activate besides that I also want to set self. animation speed to zero and then
9.04.41
0 detik
self. image should be pame do mask. from surface with self. image and that we
9.04.50
0 detik
want to turn to a surface straight away also self. image and set color key with
9.04.58
0 detik
a black color that way once the Sprite is being destroyed we don't have an animation anymore and the entire image
9.05.05
0 detik
is going to be a white silhouette on top of that I want to stop the movement of the enemy which we can do inside of the
9.05.12
0 detik
update method I only want to call move and animate if not self. death timer as soon
9.05.22
0 detik
as a death timer is running we don't want to call move or animate anymore you could also put a constraint in there it doesn't really matter once
9.05.31
0 detik
we have that if I now shoot at a worm we're getting a white silhouette for a short time and this doesn't change that happens because self. death timer.
9.05.42
0 detik
update was not called let's try this again and I can shoot at a worm and it disappears perfect this happens a second
9.05.50
0 detik
time as well very good and now I have to hit a b let's hope I get one there we go this is also working which means with
9.05.59
0 detik
that we have the proper enemy logic that was basically it and I hope from the logic here you can see how
9.06.07
0 detik
inheritance can be incredibly powerful inside of the B and the worm class we are not actually doing very much we are
9.06.15
0 detik
simply initializing a couple of basic values then we have a very simple move method and then a fairly simple constraint method
9.06.24
0 detik
that's pretty much it a lot more of the logic happens inside of the parent enemy class the animations are covered inside
9.06.31
0 detik
of animated Sprite and the very basic setup happens inside of the Sprite class that way the entire thing is much more
9.06.38
0 detik
manageable and for a larger project we would be writing a lot less code the last thing that we really have to work
9.06.45
0 detik
on is the collision between the enemies and the player all we need for this part
9.06.53
0 detik
is if pygame dos sprite. Sprite collide with self. player self. enemy Sprites
9.07.02
0 detik
and the DU kill argument doesn't really matter let's go with folds and then we want to have pygame DOS sprite.
9.07.08
0 detik
Collide underscore mask if that returns anything then we want to set self.
9.07.16
0 detik
running to bals let's try that part and now as soon as I get hit by a worm the
9.07.23
0 detik
game should be over and it is perfect that means the last thing that we have to implement is the audio that means
9.07.31
0 detik
inside of Thunder init after we are loading all of the assets we are running the setup I guess in there we can start
9.07.39
0 detik
the music all the way at the bottom I want to get self. audio and then get
9.07.46
0 detik
music remember for this part the name of each of the files is the file name without the file end
9.07.54
0 detik
this file we want to play with loops being1 let's
9.08.01
0 detik
[Music]
9.08.04
0 detik
try cool that part is working and just why we're testing the other audio files I want to comment out this part so next
9.08.13
0 detik
up we have to work on the shooting mechanic that means whenever we are creating a bullet we also want
9.08.20
0 detik
to self. audio shoot and
9.08.28
0 detik
play and now every time I'm shooting a bullet we are getting another sound whenever we are hitting an enemy that
9.08.36
0 detik
happens inside of collision we want to play self. audio this one is called
9.08.44
0 detik
impact and then play it with that we are getting a sound every time
9.08.52
0 detik
we're hitting an enemy me and with that we are done this is the entire game the last thing I suppose
9.09.00
0 detik
that we have to do is uncomment the background music this covers another pretty fancy
9.09.08
0 detik
game so I hope this was useful and at this point you should have a really good understanding of P game which means there's just one more game to go and for
9.09.16
0 detik
that we're going to work a lot more with user interfaces there is just one more game that is left to make and that is


summary:
**Bagian 1: Pengaturan Level dan Peta (Tile Map)**
Untuk game keempat ini, kita akan membuat game platformer dasar di mana pemain dapat melompat dan menembak. Logika keseluruhannya cukup sederhana, namun ada tiga hal baru: logika fisika platformer, pengaturan impor yang lebih terorganisir, dan pembuatan pengatur waktu (timer) yang fleksibel. Kita mulai dengan memuat data peta dari file Tiled (world.TMX) yang memiliki tiga layer: main (level utama), decorations (dekorasi), dan entities (posisi awal pemain dan musuh). **Posisi grid dalam Tiled kemudian dikonversi menjadi posisi piksel sebenarnya dengan mengalikannya dengan rasio ukuran tile**. Layer dekorasi dimasukkan ke grup sprite tanpa deteksi tabrakan, sedangkan tile rintangan dimasukkan ke grup yang mendukung sistem tabrakan keras.

**Bagian 2: Pemain, Pergerakan, dan Kamera**
Ketika kode mendeteksi objek bernama 'player' pada layer entitas, sistem membuat objek pemain dari kelas Player yang mewarisi fungsi Sprite dasar. **Pergerakan pemain dihitung menggunakan vektor arah (direction) yang dikalikan dengan kecepatan dan *Delta Time*, kemudian dipecah secara terpisah untuk gerakan sumbu horizontal dan vertikal guna memudahkan penanganan tabrakan (Collision Detection) pada dinding atau lantai**. Kita juga mengimplementasikan kamera otomatis. Kamera ini dibuat dengan cara mengambil titik offset dari posisi pusat pemain lalu dikurangi setengah dari lebar dan tinggi jendela, sehingga ilusi kamera akan selalu mengikuti pemain di pertengahan layar.

**Bagian 3: Gravitasi dan Mekanik Lompat**
Pergerakan vertikal dalam game platformer berbeda dari game *top-down* karena adanya pengaruh gravitasi yang menarik pemain turun. **Kita memasukkan nilai gravitasi (gravity) pada kecepatan vertikal secara bertahap setiap framenya agar saat melompat atau jatuh, pemain melesat jatuh ke bawah semakin cepat**. Saat pemain akhirnya mendarat di lantai (bertabrakan arah ke bawah), kecepatan vertikalnya akan langsung disetel kembali ke angka nol agar pemain tidak jatuh menembus dataran. Untuk mekanik lompatan, saat tombol Spasi ditekan dan pemain terdeteksi aman berada di lantai, kita menyetel nilai kecepatan vertikal menjadi angka konstan negatif seperti -20 agar karakter pemain terdorong drastis ke udara. Demi mendeteksi lantai secara akurat, dibuatlah metode khusus `check_floor` yang meletakkan area persegi (rectangle) tipis tepat di bawah kaki karakter untuk memantau persinggungan.

**Bagian 4: Sistem Impor dan Animasi Karakter**
Kita membuat fungsi utilitas kustom yang memanfaatkan metode penjelajah folder untuk memuat semua gambar ke dalam memori kamus (dictionary) secara otomatis berdasarkan namanya. Nama file gambar tersebut diurutkan terlebih dahulu agar siklus animasi berjalan sesuai urutan frame. Kita kemudian membangun kelas *AnimatedSprite* yang dapat memperbarui frame gambar menggunakan perhitungan modulus matematika dari sebuah parameter batas rentang frame. **Animasi pemain dapat berganti-ganti sesuai dengan tindakannya**: sistem memutar animasi berjalan (run) saat pergerakannya bukan nol, memutar animasi diam (idle) jika tidak bergerak, serta menahan frame khusus lompat secara statis jika pemain melayang di udara dan tidak sedang menyentuh tanah. 

**Bagian 5: Timer Kustom dan Menembak**
Game yang lebih terpoles akan bergantung pada penggunaan pengatur waktu (timer) untuk mengendalikan jeda aksi permainan. Karenanya, kita merancang kelas Timer independen yang mengkalkulasi durasi dari milidetik berjalan yang lalu dapat mengeksekusi suatu fungsi tembakan bila waktunya habis. Saat pemain menekan tombol S, sebuah objek peluru akan di-spawn dengan offset posisi moncong depan lalu dibiarkan meluncur mandiri ke sisi kiri atau kanan sesuai orientasi karakter. **Agar pemain tidak terus-menerus menembak peluru, sistem jeda ini diaktifkan (cooldown 500ms) untuk melarang peluru tambahan keluar sementara waktu**. Sistem juga merender animasi kilat tembakan berdurasi pendek yang akan melenyapkan dirinya sendiri otomatis menggunakan fungsi timer.

**Bagian 6: Logika Musuh (Lebah dan Cacing)**
Permainan akan menampung kelas lebah dan cacing yang sepenuhnya dianimasikan. Untuk cacing (Worm), objek cacing dilahirkan di dalam sebuah kotak batas imajiner yang diambil propertinya dari map Tiled. **Entitas musuh ini akan bergeser terus-menerus, dan apabila titik geraknya menyeberangi kotak areanya, musuh tersebut diprogram untuk memutar vektor pergerakan sekaligus membalik grafis tubuhnya ke ujung sebaliknya**. Untuk musuh terbang, mereka melaju secara konstan sesuai kecepatan yang ditentukan.

**Bagian 7: Deteksi Tabrakan Canggih dengan Musuh**
Sistem disempurnakan lagi untuk mendeteksi tumpang-tindih (overlap) antara entitas peluru dan musuh. **Untuk mengejar ketelitian hit yang jauh lebih baik, fungsi `pygame.mask` diadaptasi untuk menciptakan Pixel-Perfect Collision agar area gambar transparan tidak keliru dianggap sebagai titik tubuh**. Saat musuh sukses terpukul peluru, musuh ini tidak dihancurkan detik itu juga. Sebagai sentuhan efek polesan, animasi cacing atau lebah disetop geraknya, diubah menjadi permukaan siluet putih murni, lalu sebuah fungsi Timer Kematian (Death Timer) pendek bekerja menghancurkan mereka dengan fungsi bawaan kill() jika batas 200ms terlewati. Jika justru karakter utama yang tertabrak, kita cukup memutus sirkulasi game utama menjadi false dan game disudahi.

**Bagian 8: Integrasi Suara**
Sebagai implementasi akhir yang mendongkrak keasyikan platformer ini, kita membangun modul pemuat audio yang secara sistematis menyedot seluruh varian file _.wav_ atau _.ogg_ menuju ke dalam modul Python mixer. File suara diputar di beberapa metode independen: irama musik dimainkan sebagai latar belakang (-1 mengartikan diputar berulang selamanya), fungsi melepaskan peluru ditemani efek bunyi melesat, lalu kode kematian musuh terhubung pada file audio benturan.