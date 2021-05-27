import pygame

class Frame:
	def __init__(self,movement,image,imageofs,rect,hurtboxes,hitboxes,damage):
		self.movement = movement #relative movement that occurs at start of frame
		self.image = image #image of frame
		self.imageofs = imageofs #image offset relative to parent position
		self.rect = pygame.rect.Rect(rect[0],rect[1],rect[2],rect[3]) #rect used for floor/wall collisions. [0,0] is parent position.
		self.hurtboxes = [] #areas where you can be hurt. [0,0] is parent position.
		for hurtbox in hurtboxes:
			self.hurtboxes.append(pygame.rect.Rect(hurtbox[0],hurtbox[1],hurtbox[2],hurtbox[3]))
		
		self.hitboxes = [] #areas where you can do damage. [0,0] is parent position.
		for hitbox in hitboxes:
			self.hitboxes.append(pygame.rect.Rect(hitbox[0],hitbox[1],hitbox[2],hitbox[3]))
		
		self.damage = damage #damage dealt if enemy hit on this frame

class Animation:
	def __init__(self,frames,durations,loop,sound):
		self.frames = frames #list of Frame objects
		self.durations = durations #list of Frame lengths
		self.loop = loop #whether the animation loops or not
		self.sound = sound #sound effect to play during the animation. Can be None for no sound.
		self.counter = -1 #counts up every in-game frame. Start at -1 so that we don't skip first game frame
		self.curframe = 0 #current Frame of the animation
	
	def framedata(self): #retrieves current Frame object
		return self.frames[self.curframe]
	
	def update(self): #call every in-game frame. Returns True if the animation went to the next Frame object
		self.counter += 1
		if self.counter>=self.durations[self.curframe]: #if finished the duration of current Frame
			self.counter = 0
			self.curframe += 1
			if self.curframe>=len(self.frames): #if reached end of animation
				if self.loop: #start over
					self.counter=0
					self.curframe=0
					return True
				self.curframe -= 1 #we want the animation to hang on the last Frame if it goes over
				return False
			else:
				return True
		return False

class Character(pygame.sprite.Sprite):
	def __init__(self,pos,startanimation):
		pygame.sprite.Sprite.__init__(self)
		self.pos = pos #position of character on screen
		anim = Animation(startanimation[0],startanimation[1],startanimation[2],startanimation[3]) #create new Animation object
		self.curanim = anim #current animation playing
		
		frame0 = self.curanim.framedata()
		self.rect = frame0.rect #rect used for floor/wall collisions relative to pos
		self.image = frame0.image #current display image
		self.imageofs = frame0.imageofs #image offset relative to pos
		self.hurtboxes = frame0.hurtboxes #areas where you can be hurt. [0,0] is pos.
		self.hitboxes = frame0.hitboxes #areas where you can do damage. [0,0] is pos.
		self.damage = frame0.damage #damage dealt if enemy hit on this frame
	
	def update(self):
		nextframe = self.curanim.update()
		if nextframe: #only need to change values if the frame actually changed
			frame0 = self.curanim.framedata()
			self.pos[0]+=frame0.movement[0] #update pos (rect and hit/hurtboxes are relative to pos so no need to change them)
			self.pos[1]+=frame0.movement[1]
			self.rect = frame0.rect #rect used for floor/wall collisions relative to pos
			self.image = frame0.image #current display image
			self.imageofs = frame0.imageofs #image offset relative to pos
			self.hurtboxes = frame0.hurtboxes #areas where you can be hurt. [0,0] is pos.
			self.hitboxes = frame0.hitboxes #areas where you can do damage. [0,0] is pos.
			self.damage = frame0.damage #damage dealt if enemy hit on this frame

	def setanimation(self,newanim): #where newanim points to an entry in animation_database
		anim = Animation(newanim[0],newanim[1],newanim[2],newanim[3]) #create new Animation object
		self.curanim = anim
		
		frame0 = self.curanim.framedata()
		self.rect = frame0.rect #rect used for floor/wall collisions relative to pos
		self.image = frame0.image #current display image
		self.imageofs = frame0.imageofs #image offset relative to pos
		self.hurtboxes = frame0.hurtboxes #areas where you can be hurt. [0,0] is pos.
		self.hitboxes = frame0.hitboxes #areas where you can do damage. [0,0] is pos.
		self.damage = frame0.damage #damage dealt if enemy hit on this frame
