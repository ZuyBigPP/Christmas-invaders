import pygame 
from laser import Laser

class Player(pygame.sprite.Sprite):
	def __init__(self,pos,constraint,speed):#khởi tạo người chơi
		super().__init__()
		self.image = pygame.image.load('../graphics/player2.png').convert_alpha()#Tạo hình ảnh cho đối tượng người chơi từ tệp hình ảnh
		self.rect = self.image.get_rect(midbottom = pos)#Lấy hình chữ nhật (rect) bao quanh hình ảnh người chơi và đặt nó tại vị trí pos (giữa phía dưới).
		self.speed = speed#Đặt tốc độ di chuyển của người chơi.
		self.max_x_constraint = constraint#Đặt giới hạn tọa độ x tối đa mà người chơi có thể di chuyển đến.
		self.ready = True#Biến ready được sử dụng để kiểm tra xem người chơi đã sẵn sàng bắn laser hay chưa.
		self.laser_time = 0#Thời gian hiện tại từ lúc bắn laser gần nhất.
		self.laser_cooldown = 600#Thời gian cooldown giữa các lần bắn laser, tính bằng mili giây.

		self.lasers = pygame.sprite.Group()#Tạo một nhóm sprite để quản lý các laser mà người chơi bắn ra.

		self.laser_sound = pygame.mixer.Sound('../audio/laser.wav')#Tạo âm thanh cho laser từ tệp âm thanh 
		self.laser_sound.set_volume(0.5)#Đặt âm lượng của âm thanh laser là 0.5.

	def get_input(self):#thiết lập nút bấm từ bàn phím
		keys = pygame.key.get_pressed()#Lấy danh sách trạng thái của tất cả các phím bằng chức năng có sẵn

		if keys[pygame.K_RIGHT]:#Nếu phím mũi tên phải được nhấn, di chuyển người chơi sang phải với tốc độ self.speed
			self.rect.x += self.speed
		elif keys[pygame.K_LEFT]:#Nếu phím mũi tên trái được nhấn, di chuyển người chơi sang trái với tốc độ self.speed.
			self.rect.x -= self.speed

		if keys[pygame.K_SPACE] and self.ready:# Nếu phím Space được nhấn và người chơi đã sẵn sàng bắn laser
			self.shoot_laser()# Gọi phương thức shoot_laser để thực hiện bắn laser.
			self.ready = False#Đặt biến ready thành False để ngăn người chơi bắn laser liên tục.
			self.laser_time = pygame.time.get_ticks()# Ghi lại thời điểm cuối cùng khi người chơi bắn laser.
			self.laser_sound.play()#: Phát âm thanh của laser.

	def recharge(self):#Cơ chế nạp đạn
		if not self.ready:# Kiểm tra xem người chơi có sẵn sàng bắn laser không. Nếu không (not self.ready), tức là người chơi đang trong trạng thái không sẵn sàng.
			current_time = pygame.time.get_ticks()# Lấy thời điểm hiện tại của trò chơi trong đơn vị milliseconds.
			if current_time - self.laser_time >= self.laser_cooldown: #nếu 'tgian hiện tại' - 'thời điểm bắn laser cuối cùng' >= tgian hồi đạn 
				self.ready = True#đạn sẵn sàng

	def constraint(self):#kiểm soát và giữ cho người chơi không vượt quá ranh giới bên trái và bên phải của màn hình.
		if self.rect.left <= 0:
			self.rect.left = 0
		if self.rect.right >= self.max_x_constraint:
			self.rect.right = self.max_x_constraint

	def shoot_laser(self):#tạo ra và thêm một đối tượng laser mới vào nhóm laser của người chơi
		self.lasers.add(Laser(self.rect.center,-8,self.rect.bottom))
	"""
	self.lasers.add(Laser(self.rect.center, -8, self.rect.bottom)): Tạo một đối tượng Laser mới bằng cách gọi constructor của lớp Laser
	self.rect.center: Vị trí tâm của người chơi, nơi mà laser bắt đầu.
	-8: Tốc độ di chuyển của laser theo hướng lên trên màn hình (âm là hướng lên).
	self.rect.bottom: Tọa độ y của đáy của người chơi, nơi laser bắt đầu.
"""
	def update(self):#cập nhật trạng thái cho người chơi và lasers
		self.get_input()#Kiểm tra input từ bàn phím để xác định hướng di chuyển của người chơi và xử lý việc bắn laser nếu có.
		self.constraint()# Giới hạn vị trí của người chơi trong khung màn hình. 
		self.recharge()#Kiểm tra và thiết lập trạng thái sẵn sàng bắn laser
		self.lasers.update()#Cập nhật tất cả các lasers trong nhóm laser của người chơi.