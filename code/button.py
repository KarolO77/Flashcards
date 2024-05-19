from pygame.mouse import get_pressed

class Button():
	def __init__(self, pos, image, text=None):
		self.rect = image.get_rect(topleft = pos)
		self.width = image.get_width()
		self.height = image.get_height()
		self.image = image
		self.pos = pos

		self.key = text
		self.text = text
		self.text_pos = (pos[0]+self.width/2,pos[1]+self.height/2)

		self.is_clicked = False

	def update_pos(self, pos, text_pos=False):
		self.pos = pos
		self.rect = self.image.get_rect(topleft = pos)
		if text_pos:
			self.text_pos = text_pos
		else:
			self.text_pos = (pos[0]+self.width/2,pos[1]+self.height/2)


	def clicked(self, mouse_pos):

		if self.rect.collidepoint(mouse_pos):
			if get_pressed()[0] == 1 and self.is_clicked == False:
				self.is_clicked = True

		if get_pressed()[0] == 0:
			self.is_clicked = False

		return self.is_clicked