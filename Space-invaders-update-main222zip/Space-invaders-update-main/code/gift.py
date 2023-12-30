import pygame

class Gift(pygame.sprite.Sprite):
	def __init__(self,name,x,y):#khởi tạo gift
		super().__init__()
		file_path = '../graphics/' + name + '.png'#xây dựng đường dẫn tới tệp hình ảnh của quà dựa trên tên quà.
		self.image = pygame.image.load(file_path).convert_alpha()#tải hình ảnh của quà và chuyển đổi alpha để hỗ trợ đồ họa trong suốt.
		self.rect = self.image.get_rect(topleft = (x,y))#tạo hình chữ nhật xác định vị trí và kích thước của quà.

		if name == 'red': self.value = 100#kiểm tra tên của quà và gán giá trị tương ứng cho thuộc tính value.
		elif name == 'ring': self.value = 200
       
		else: self.value = 300

	def update(self,direction):# cập nhật trạng thái của đối tượng sprite
		self.rect.x += direction# cập nhật tọa độ x của quà dựa vào hướng di chuyển. Nếu direction là dương (1), quà sẽ di chuyển sang phải; nếu direction là âm (-1), quà sẽ di chuyển sang trái.

class Extra(pygame.sprite.Sprite):
    def __init__(self, side, screen_width):#khởi tạo extra
        super().__init__()
        self.image = pygame.image.load('../graphics/extra22.png').convert_alpha()#Là hình ảnh đại diện cho đối tượng "Extra" được tải từ đường dẫn
        
        if side == 'right':#Kiểm tra xem giá trị của biến side có phải là 'right' không.
            self.rect = self.image.get_rect(topleft=(screen_width + 50, 600))# Nếu side là 'right', thì tạo một hình chữ nhật (rectangle) với góc trái trên cùng là (screen_width + 50, 600). 
            #Điều này đặt đối tượng ở phía bên phải của màn hình, nằm ngoài khung nhìn ban đầu.
            self.direction = -1  # Ban đầu di chuyển sang trái
        else:
            self.rect = self.image.get_rect(topleft=(-50, 600))#
            self.direction = 1  # Ban đầu di chuyển sang phải

        self.speed = 7#tốc độ

    def update(self, screen_width):#cập nhật trạng thái của đối tượng Extra
        self.rect.x += self.speed * self.direction
#Cập nhật vị trí ngang (hoành độ) của đối tượng Extra dựa trên tốc độ (self.speed) và hướng di chuyển (self.direction). Nếu self.direction là 1, đối tượng di chuyển sang phải; nếu là -1, đối tượng di chuyển sang trái.
        # Kiểm tra nếu chạm vào biên trái hoặc biên phải thì đổi hướng di chuyển
        if self.rect.left <= 0:
            self.direction = 1  # Đổi hướng sang phải
        elif self.rect.right >= screen_width:
            self.direction = -1  # Đổi hướng sang trái
