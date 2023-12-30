
"""
Import các thư viện và module cần thiết, bao gồm cả thư viện pygame
"""
import pygame, sys                        
from player import Player   #Liên kết với file player để có thể tạo ra người chơi                
from datetime import datetime #cơ chế game
from gift import Gift, Extra   #liên kết với file gift để tạo ra những đơn vị khác  
from random import choice, randint #cơ chế game
from menu import Menu, GameOverScreen  #liên kết với file menu để khởi tạo menu cho trò chơi    
 
current_time = datetime.now() #dùng để lấy thời gian hiện tại, 
"""
đông thời sử dụng để đo lường thời gian trôi qua,
 ví dụ như để tính thời gian đã trôi qua từ một sự kiện cụ thể như bắt đầu trò chơi
"""



#khởi tạo lớp Game
class Game:
	def __init__(self): #khởi tạo được sử dụng để khởi tạo và cấu hình các thành phần cần thiết cho trò chơi
		# Player setup(Tạo người chơi)
		player_sprite = Player((screen_width / 2,screen_height),screen_width,5)
		"""
	Tạo một đối tượng người chơi(Player):
	+'pos'(position:vị trí):vị trí ban đầu của người chơi,
	  ở giữa màn hình theo chiều ngang và ở phía dưới theo chiều dọc
	  (width:chiều rộng
	   height:chiều cao)
	+'constraint':giới hạn vị trí người chơi theo chiều ngang độ rộng màn hình
	  tránh cho ảnh sprit người chơi không bị lấp vào rìa màn hình
	+'speed':tốc độ di chuyển của người chơi(5)
	Các tham số trên được khởi tạo qua đoạn code 
	"class Player(pygame.sprite.Sprite):
	def __init__(self,pos,constraint,speed)" và được liên kết sang file main

"""		
		self.player = pygame.sprite.GroupSingle(player_sprite)
		"""
	Tạo 1 nhóm sprite pygame với tên self.player:
	+Sử dụng pygame.sprite.GroupSingle để tạo nhóm chứa duy nhất một sprite là người chơi
	sau đó gán player_sprite vào
	+'self':là một tham số đặc biệt trong định nghĩa phương thức của một lớp.
	Khi bạn gọi một phương thức của một đối tượng, 
	self tự động được truyền vào phương thức và tham chiếu đến đối tượng đó. 
	Nó giúp phương thức biết đang thao tác với dữ liệu của đối tượng nào.
	+'GroupSingle: là một lớp trong thư viện Pygame, được sử dụng để quản lý sprite. 
	Nó tương tự như Group trong Pygame, nhưng chỉ chứa một sprite duy nhất. 
	Việc này có thể hữu ích khi bạn chỉ cần quản lý một sprite cụ thể.
"""


		#score setup:thiết lập cơ chế tính điểm
		self.score = 0 #điểm bắt đầu 
		self.font = pygame.font.Font('../font/Pixeled.ttf',20)
		#sử dụng chức năng Font có sẵn của pygame để vẽ văn bản trên màn hình
		#Font được tải từ tệp tin Pixeled.ttf ở thư mục ../font/ với kích thước chữ là 20.
		
		

		#Time
		self.start_time = pygame.time.get_ticks() #ghi lại thời điểm bắt đầu của một sự kiện hoặc quá trình trong trò chơi
		"""
	-Biến 'self.start_time' sau đó được sử dụng để theo dõi khoảng thời gian đã trôi qua từ thời điểm bắt đầu một sự kiện hoặc quá trình.
	-'pygame.time.get_ticks()':
	+Là một hàm của thư viện Pygame, trả về số miligiây kể từ lúc Pygame được khởi tạo.
	+Được sử dụng để đo lường khoảng thời gian giữa các sự kiện hoặc để tính toán thời gian.

"""
		
		# gift setup
		self.gift = pygame.sprite.Group() #đại diện các đơn vị hộp quà trong game
		self.gift_setup(rows = 9, cols = 9)
		#Gọi phương thức 'gift_setup' để cấu hình vị trí và loại của quà tặng
		#tham số rows(hàng) và cols(columns:cột) cho thấy các hộp quà được xếp theo kiểu 9x9
		self.gift_direction = 1
		#Biến 'self.gift_direction' được sử dụng để xác định hướng di chuyển của quà tặng trên màn hình.
		#Trong trường hợp này, quà tặng sẽ di chuyển về bên phải đầu tiên (hướng dương), và sau đó sẽ đảo hướng khi đến mép màn hình.
		

		# Audio setup
		self.laser_sound = pygame.mixer.Sound('../audio/laser.wav')
		self.laser_sound.set_volume(0.5)
		self.explosion_sound = pygame.mixer.Sound('../audio/explosion.wav')
		self.explosion_sound.set_volume(0.3)
		"""
	-'self.laser_sound' và 'self.explosion_sound' 
	là âm thanh khi người chơi bắn laser và âm thanh khi laser va chúng địch(nổ) từ file âm thanh và được đưa vào bằng chức năng có sẵn của pygame
	-'self.laser_sound.set_volume(0.5)' và 'self.explosion_sound.set_volume(0.3)' 
	dùng để đặt âm lượng cho 'self.laser_sound' và self.explosion_sound bằng 0.5/0.3(50%/30% âm lượng tối đa)
	
"""
		# Extra setup
		self.extra_group = pygame.sprite.Group()#quản lý đối tượng extra
		self.extra = Extra(choice(['right', 'left']), screen_width)
		#'choice(['right', 'left']': cho đơn vị extra chọn hướng đi trái phải ngẫu nhiên
		#'screen_width': xác định giới hạn bên phải hoặc bên trái của màn hình, tùy thuộc vào hướng được chọn.
		self.extra_group.add(self.extra)#thêm đối tượng self.extra vào nhóm sprite
#------------------------------------------------------------------------------
	#Hàm setup các hộp quà
	def gift_setup(self,rows,cols,x_distance = 60,y_distance = 48,x_offset = 70, y_offset = 100):
		"""
	rows: Số lượng hàng trong lưới quà tặng.
	cols: Số lượng cột trong lưới quà tặng.
	x_distance (mặc định là 60): Khoảng cách giữa các quà tặng theo chiều ngang.
	y_distance (mặc định là 48): Khoảng cách giữa các quà tặng theo chiều dọc.
	x_offset (mặc định là 70): Vị trí bắt đầu của lưới quà tặng theo chiều ngang.
	y_offset (mặc định là 100): Vị trí bắt đầu của lưới quà tặng theo chiều dọc.	
"""
		for row_index, row in enumerate(range(rows)):#Dùng vòng lặp để duyệt các giá trị và chỉ số của từng hàng
			for col_index, col in enumerate(range(cols)):#Dùng vòng lặp lồng vào vòng lặp hàng để duyệt qua từng cột trong mỗi hàng.
				x = col_index * x_distance + x_offset
				y = row_index * y_distance + y_offset
				"""
	Dùng để	 tính toán vị trí (coordinates) của mỗi ô trong lưới dựa trên chỉ số của hàng (row_index) và cột (col_index).
	-x = col_index * x_distance + x_offset:
 	+col_index là chỉ số của cột trong lưới.
	+x_distance là khoảng cách giữa các ô theo chiều ngang trong lưới.
	+x_offset là vị trí bắt đầu của lưới theo chiều ngang.
	+Tính toán x để xác định vị trí theo chiều ngang của ô hiện tại trong lưới.
	-y = row_index * y_distance + y_offset:
	+row_index là chỉ số của hàng trong lưới.
	+y_distance là khoảng cách giữa các ô theo chiều dọc trong lưới.
	+y_offset là vị trí bắt đầu của lưới theo chiều dọc.
	+Tính toán y để xác định vị trí theo chiều dọc của ô hiện tại trong lưới.		
"""
				if row_index == 0: gift_sprite = Gift('yellow',x,y)
				elif row_index == 1: gift_sprite = Gift('green',x,y)
				elif row_index == 2: gift_sprite = Gift('blue',x,y)
				elif row_index == 3: gift_sprite = Gift('white',x,y)
				elif row_index == 4: gift_sprite = Gift('black',x,y)
				elif row_index == 5: gift_sprite = Gift('human',x,y)
				elif row_index == 6: gift_sprite = Gift('ring',x,y)
				else: gift_sprite = Gift('red',x,y)
				"""
if row_index == 0: gift_sprite = Gift('yellow', x, y):

Nếu chỉ số của hàng là 0, tạo một đối tượng quà tặng (gift_sprite) thuộc lớp Gift với tên là 'yellow' và vị trí (x, y) đã được tính toán trước đó.
elif row_index == 1: gift_sprite = Gift('green', x, y):

Nếu chỉ số của hàng là 1, tạo một đối tượng quà tặng với tên 'green'.
elif row_index == 2: gift_sprite = Gift('blue', x, y):

Nếu chỉ số của hàng là 2, tạo một đối tượng quà tặng với tên 'blue'.
elif row_index == 3: gift_sprite = Gift('white', x, y):

Tương tự như trên, nhưng với tên 'white'.
elif row_index == 4: gift_sprite = Gift('black', x, y):

Tương tự, nhưng với tên 'black'.
elif row_index == 5: gift_sprite = Gift('human', x, y):

Tạo một đối tượng quà tặng với tên 'human'.
elif row_index == 6: gift_sprite = Gift('no', x, y):

Tạo một đối tượng quà tặng với tên 'no'.
elif row_index == 6: gift_sprite = Gift('ring', x, y):

Lưu ý rằng có một sự trùng lặp trong các điều kiện trước đó (row_index == 6). Dòng mã này có thể bị trôi lệch và không bao giờ được thực hiện.
else: gift_sprite = Gift('red', x, y):

Nếu không phải bất kỳ điều kiện nào trước đó đều đúng, tạo một đối tượng quà tặng với tên 'red'.
"""
				self.gift.add(gift_sprite)
		#Thêm đối tượng quà tặng đã tạo vào nhóm sprite self.gift, nhóm này được sử dụng để quản lý tất cả các đối tượng quà tặng trong trò chơi.
#------------------------------------------------------------------------------------
	def gift_position_checker(self):# kiểm tra vị trí của quà tặng và điều chỉnh hướng di chuyển của chúng dựa trên vị trí tương đối đối với màn hình.
		all_gift = self.gift.sprites()#Lấy tất cả các đối tượng quà tặng hiện tại trong nhóm sprite 'self.gift' và lưu chúng vào danh sách 'all_gift'.
		for gift in all_gift:#Duyệt qua từng đối tượng trong danh sách 'all_gift
			if gift.rect.right >= screen_width:
				self.gift_direction = -1 
			elif gift.rect.left <= 0:
				self.gift_direction = 1
	"""
	-'if gift.rect.right >= screen_width:':
	+Nếu phần phải (right) của hình chữ nhật giới hạn của quà tặng vượt qua biên phải của màn hình 'screen_width', 
	có nghĩa là quà tặng đã di chuyển ra khỏi màn hình từ phải sang trái.
	+Khi điều này xảy ra, cập nhật hướng di chuyển 'self.gift_direction' thành -1, nghĩa là quà tặng sẽ di chuyển về bên trái.
	-'elif gift.rect.left <= 0:':
	+Ngược lại, nếu phần trái (left) của hình chữ nhật giới hạn của quà tặng vượt qua biên trái của màn hình (0),
	có nghĩa là quà tặng đã di chuyển ra khỏi màn hình từ trái sang phải.
	+Khi điều này xảy ra, cập nhật hướng di chuyển 'self.gift_direction' thành 1, nghĩa là quà tặng sẽ di chuyển về bên phải.
"""
	def collision_checks(self):#kiểm tra va chạm giữa các đối tượng trong trò chơi
#Cụ thể là va chạm giữa tia laser người chơi bắn ra với các đơn vị gift và extra
		
		# player lasers
		if self.player.sprite.lasers: #kiểm tra xem người chơi đã bắn ít 1 tia laser hay chưa
			for laser in self.player.sprite.lasers:#Nếu đúng thì vòng lặp sẽ được thực hiện
	
				# gift collisions:khi laser va chạm với các đơn vị hộp quà
				gift_hit = pygame.sprite.spritecollide(laser,self.gift,True)
				#'pygame.sprite.spritecollide':Hàm có sẵn trong thư viện pygame kiểm tra va chạm
				#'laser' và 'self.gift' là 2 đối tượng kiểm tra khi va chạm với nhau và loại bỏ lẫn nhau bởi tham số 'True
				if gift_hit:#Xử lí kh có va chạm
					for gift in gift_hit:#Mỗi đối tượng được duyệt qua được xác nhận là bị laser bắn
						self.score += gift.value#Cộng điểm cho người chơi
					laser.kill()#laser biến mất sau khi va chạm với hộp quà
					self.explosion_sound.play()#âm thanh báo hiệu khi laser va với quà

				# extra collision:khi va chạm
				if pygame.sprite.spritecollide(laser,self.extra_group,False):#ssex không bị loại bỏ khi va chạm bởi tham số False
					self.score -= 500 #Trừ 500 điểm khi bắn trúng
					laser.kill()#####




	def display_score(self):#Hiển thị và cập nhật điểm liên tục trong quá trình chơi
		score_surf = self.font.render(f'score: {self.score}',False,'white')#1
		score_rect = score_surf.get_rect(topleft = (10,-10))#2
		screen.blit(score_surf,score_rect)#3
	"""
	1. tạo một bề mặt văn bản để hiển thị điểm số của người chơi
	-'self.font': Đây là đối tượng Font của pygame,
	được khởi tạo trước đó trong lớp Game để sử dụng font từ một tệp tin ttf ('../font/Pixeled.ttf') và có kích thước 20.
	-'render()': chức năng có sẵn, được sử dụng để tạo bề mặt văn bản từ một chuỗi.
	-'f'score: {self.score}':Chuỗi văn bản được tạo ra, chứa thông tin điểm số của người chơi.
	 Biểu diễn f-string được sử dụng để chèn giá trị của 'self.score' vào chuỗi.
	-'False' sẽ bớt tốn tài nguyên hơn 'True'
	-Màu chữ là trắng(white)
	2. tạo một hình chữ nhật (Rect) để định vị vị trí của bề mặt văn bản trên màn hình
	-'get_rect':chức năng có sẵn, trả về một hình chữ nhật có kích thước bằng với kích thước của bề mặt.
	-'topleft=(10, -10)': Tham số này đặt vị trí của góc trái trên của hình chữ nhật trên màn hình.
	  Trong trường hợp này, được đặt tại tọa độ (10, -10).
	3. Vẽ bề mặt văn bản lên màn hình tại vị trí đã được xác định bởi hình chữ nhật.
	"""
	#Time
	def countdown(self, seconds):#đểm ngược thời gian chơi
		global game_over #thay đổi giá trị của 'game_over' ở mức độ toàn cục
		elapsed_time = pygame.time.get_ticks() - self.start_time 
		#'elapsed_time': Là thời gian đã trôi qua tính bằng milliseconds từ thời điểm bắt đầu đồng hồ đếm ngược đến thời điểm hiện tại.
		#'pygame.time.get_ticks()': Trả về số milliseconds kể từ khi Pygame được khởi động hoặc tại thời điểm cuối cùng hàm tick() được gọi. Điều này đo lường thời gian chạy của trò chơi.
		#'self.start_time':tính thời gian trôi qua, bắt đầu đểm ngược
		self.time = seconds * 1000 - elapsed_time #xác định thời gian còn lại trong đồng hồ đếm ngược.
		#'seconds': Là thời gian ban đầu (truyền vào phương thức) mà đồng hồ đếm ngược sẽ đếm ngược từ.
		#'* 1000': Chuyển đổi thời gian từ giây sang milliseconds, vì pygame.time.get_ticks() trả về thời gian tính bằng milliseconds
		if self.time <= 0:
			game_over = True #kết thúc trò chơi khi hết thời gian
		time_surf = self.font.render(f'time: {str(int(self.time / 1000) + 1)}', False, 'white')
		time_rect = time_surf.get_rect(topleft = (650, -10))
		screen.blit(time_surf, time_rect)

		
	
	 #Score
	def score_end(self):#điểm sau khi chơi xong
		score_surf = self.font.render(f'Your score: {self.score}',False,'white')###
		score_rect = score_surf.get_rect(topleft = (200,200))#vị trí hiển thị
		screen.blit(score_surf,score_rect)####

	

	def run(self):
		self.player.update() #cập nhật vị trí và trạng thái của người chơi dựa trên các sự kiện người chơi nhập vào.
		self.gift.update(self.gift_direction)# cập nhật vị trí của các quà và hướng di chuyển của chúng dựa trên self.gift_direction.
		self.gift_position_checker()#kiểm tra xem quà đã đến các biên của màn hình chưa và điều chỉnh hướng di chuyển nếu cần thiết.
		self.collision_checks()#tra xem có xung đột nào giữa các đối tượng như lasers, quà, và extra hay không. Nếu có xung đột, thực hiện các hành động tương ứng như giảm điểm, hủy bỏ đối tượng, hoặc kích hoạt âm thanh.
		self.extra_group.update(screen_width)# cập nhật vị trí của extra và kiểm tra xem chúng có đi ra khỏi màn hình hay không.
		self.extra_group.draw(screen)#vẽ extra lên màn hình
		self.player.sprite.lasers.draw(screen)# Vẽ tất cả các lasers của người chơi lên màn hình.
		self.player.draw(screen)#Vẽ người chơi lên màn hình.	
		self.gift.draw(screen)#Vẽ tất cả các quà lên màn hình.
		self.display_score()#hiển thị điểm số lên màn hình.
		self.countdown(60)#hiển thị và kiểm tra thời gian đếm ngược.
		if self.score <= 0:
			self.score = 0#Kiểm tra xem điểm số có dưới 0 hay không và nếu có, đặt nó thành 0 để tránh hiển thị điểm số âm.


if __name__ == '__main__': #chạy khi là file chính
	pygame.init()#khởi tạo pygame
	screen_width = 800 #chiều rộng cửa sổ 
	screen_height = 800 #Chiều cao cửa sổ
	screen = pygame.display.set_mode((screen_width,screen_height))#Tạo cửa sổ trò chơi có kích thước được đặt trước.
	clock = pygame.time.Clock() #Tạo đối tượng Clock để giới hạn tốc độ khung hình của trò chơi.
	game = Game()#Tạo một đối tượng Game, tức là khởi động trò chơi.
	
	menu = Menu(screen)#Tạo đối tượng Menu và truyền vào màn hình để vẽ giao diện menu.
	selected_option = menu.run_menu()#Chạy menu và lấy lựa chọn của người chơi từ menu.
	if selected_option == 0:  # Nếu người chơi chọn "Play"
		game = Game() #thì tạo game mới
	if selected_option == 1: # Nếu người chơi chọn "Quit"
		pygame.quit() #thì kết thúc chương trình bằng cách thoát pygame và thoát khỏi Python.
		sys.exit()

	game_over_screen = GameOverScreen()#Tạo đối tượng GameOverScreen để hiển thị màn hình kết thúc trò chơi.
	game_over = False #Khởi tạo biến game_over với giá trị False, đại diện cho việc trò chơi chưa kết thúc.
	background_end = pygame.image.load('../graphics/background2.png').convert()#Tải hình nền cho màn hình kết thúc trò chơi.
	optimize = True# tối ưu hóa hình nền của màn hình chơi

	while True:
		for event in pygame.event.get():# Duyệt qua từng sự kiện trong danh sách.
			if event.type == pygame.QUIT:#Kiểm tra nếu sự kiện là sự kiện đóng cửa sổ (pygame.QUIT), tức là người chơi muốn kết thúc trò chơi.
				pygame.quit()#Dừng thư viện pygame.
				sys.exit()#Thoát khỏi chương trình Python.
			
			

		if game_over:
			screen.blit(background, (0, 0))#Vẽ hình nền của màn hình kết thúc trò chơi lên cửa sổ.
			game_over_screen.draw(screen)#Vẽ hình nền của màn hình kết thúc trò chơi lên cửa sổ.
			replay_clicked = game_over_screen.handle_event(event)#Xử lý sự kiện để kiểm tra xem người chơi có click vào nút "Replay" không và lưu kết quả.
			game.score_end()#Hiển thị điểm số cuối cùng của người chơi.
			if replay_clicked: #nêú ấn chơi lại
				game = Game() #tạo ván mới
				game_over = False# Đặt trạng thái kết thúc trò chơi về False để tiếp tục vòng lặp chính.
				optimize = True#Đặt lại biến optimize để tái tạo hình nền cho màn hình chơi.
		else:
			if optimize == True:#Kiểm tra xem hình nền của màn hình chơi đã được tối ưu hóa chưa.
				background = pygame.image.load("../graphics/background4.png").convert()#Tải hình nền mới cho màn hình chơi và chuyển định dạng nó để tối ưu hóa.
				optimize = False#optimize = False: Đặt lại biến optimize để không cần tối ưu hóa nữa.
			screen.blit(background, (0,0))#Vẽ hình nền của màn hình chơi lên cửa sổ.
			game.run()#Gọi phương thức run() của đối tượng Game để cập nhật và vẽ mọi thứ trên màn hình chơi.
		
		pygame.display.flip()#Cập nhật màn hình.
		clock.tick(60)
#Giới hạn tốc độ khung hình của trò chơi để không làm tăng quá mức tài nguyên hệ thống. Ở đây, mỗi giây sẽ có tối đa 60 khung hình.
