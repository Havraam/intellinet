from socket import socket
from zlib import decompress
import ctypes
import pygame

class Button:
    def __init__(self, x, y, width, height, text, color, font_size):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.color = color
        self.font = pygame.font.Font(None, font_size)
        self.text_surface = self.font.render(self.text, True, (0, 0, 0))  # Black text

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))
        text_rect = self.text_surface.get_rect(center=(self.x + self.width // 2, self.y + self.height // 2))
        screen.blit(self.text_surface, text_rect)

    def is_clicked(self, pos):
        x, y = pos
        return (self.x <= x <= self.x + self.width) and (self.y <= y <= self.y + self.height)

# Set process to be DPI aware so that the resolution wont be dependant on screen scaling
windll = ctypes.windll
user32 = windll.user32
user32.SetProcessDPIAware(1)

# Now use GetSystemMetrics in order to get resolution
WIDTH = user32.GetSystemMetrics(0)
HEIGHT = user32.GetSystemMetrics(1)

def recvall(conn, length):
    """ Retreive all pixels. """

    buf = b''
    while len(buf) < length:
        data = conn.recv(length - len(buf))
        if not data:
            return data
        buf += data
    return buf


def main(host='Erels-laptop.local', port=5000): #insert wanted computers name 
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT)) # making pygamae window 
    clock = pygame.time.Clock()
    # setting button properties
    button_width = 100
    button_height = 30
    button_color = (255, 0, 0)  # Red
    button_text = "Stop Share"
    font_size = 20
    # creating button
    button = Button(WIDTH - button_width - 10, HEIGHT - button_height - 10, button_width, button_height, button_text, button_color, font_size)

    watching = True

    sock = socket()
    sock.connect((host, port))
    share_res = sock.recv(1024).decode() #reciving target computer's resolution
    
    share_width = int((share_res.split(","))[0]) #spliting and turning share res to integer 
    share_height = int((share_res.split(","))[1])

    print (share_width + share_height)
    try:
        while watching:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    watching = False
                    break
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if button.is_clicked(event.pos):
                        watching = False  # Stop sharing on button click
            
            # Retreive the size of the pixels length, the pixels length and pixels
            size_len = int.from_bytes(sock.recv(1), byteorder='big')
            size = int.from_bytes(sock.recv(size_len), byteorder='big')
            pixels = decompress(recvall(sock, size))

            # Create the Surface from raw pixels
            img = pygame.image.fromstring(pixels, (share_width, share_height), 'RGB')
            scaled_img = pygame.transform.scale(img, (WIDTH,HEIGHT)) #scale the image

            # Display the scaled picture
            screen.blit(scaled_img, (0, 0))
            button.draw(screen)
            pygame.display.flip()
            clock.tick(60)
    except ConnectionResetError:
        print("connection closed ")
    except:
        print("something went wrong")
    finally:
        sock.close()


if __name__ == '__main__':
    main()
