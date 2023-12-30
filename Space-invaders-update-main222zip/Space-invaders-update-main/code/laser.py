import pygame 

class Laser(pygame.sprite.Sprite):#định nghĩa lớp laser
	def __init__(self,pos,speed,screen_height):#khởi tạo lớp laser với tham số
		"""
		pos: Vị trí ban đầu của laser (tọa độ x, y).
		speed: Tốc độ di chuyển của laser (theo chiều dọc).
		screen_height: Chiều cao của màn hình để xác định khi nào laser nên bị hủy.
		"""
		super().__init__()#Gọi phương thức khởi tạo của lớp cơ sở (pygame.sprite.Sprite) để thiết lập một số thuộc tính cơ bản.
		self.image = pygame.Surface((4,20))#hình dạng laser có kich thước 4x20
		self.image.fill('white')#Đổ màu trắng vào bề mặt để tạo một laser trắng.
		self.rect = self.image.get_rect(center = pos)#Tạo một hình chữ nhật (Rect) cho laser và đặt vị trí của nó ở trung tâm được xác định bởi pos.
		self.speed = speed# Lưu tốc độ di chuyển của laser.
		self.height_y_constraint = screen_height# Lưu chiều cao của màn hình để kiểm tra khi nào laser nên bị hủy.

	def destroy(self):#kiểm tra xem laser có nên bị hủy không.
		if self.rect.y <= -50 or self.rect.y >= self.height_y_constraint + 50:
			self.kill()#nêú laser bay quá màn hình sẽ bị hủy

	def update(self):#cập nhật vị trí của laser và kiểm tra xem nó có nên bị hủy không.
		self.rect.y += self.speed#Di chuyển laser theo chiều dọc với tốc độ đã được đặt trước đó.
		self.destroy()#Gọi phương thức destroy để kiểm tra xem laser có nên bị hủy không.
