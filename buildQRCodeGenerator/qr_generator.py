import math
from PIL import Image

class QRCodeGenerator:
    def __init__(self, data, ec_level='M'):
        self.data = data
        self.ec_level = ec_level
        self.version = 4
        self.mode = self.determine_mode()
        self.size = 21 + (self.version - 1) * 4
        self.modules = [[False for _ in range(self.size)] for _ in range(self.size)]
        self.bit_stream = self.encode_data()
        self.error_correct()
        self.build_qr()
        self.apply_best_mask()
        self.add_format_and_version()
        self.save_image()

    def determine_mode(self):
        if all(c.isdigit() for c in self.data):
            return 'numeric'
        if all(c in '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ $%*+-./: ' for c in self.data):
            return 'alphanumeric'
        return 'byte'

    def encode_data(self):
        mode_ind = {'numeric': '0001', 'alphanumeric': '0010', 'byte': '0100'}[self.mode]
        char_count_bits = {'numeric': 10, 'alphanumeric': 9, 'byte': 8}[self.mode]
        char_count = format(len(self.data), f'0{char_count_bits}b')
        data_bits = self.encode_data_bits()
        bit_string = mode_ind + char_count + data_bits
        total_bits = self.get_total_data_bits()
        if len(bit_string) > total_bits:
            raise ValueError("Data too long")
        bit_string += '0000'  
        while len(bit_string) % 8 != 0:
            bit_string += '0'
        while len(bit_string) < total_bits:
            bit_string += '1110110000010001'  
        return bit_string[:total_bits]

    def get_total_data_bits(self):
        data_codewords = {'L': 80, 'M': 64, 'Q': 48, 'H': 36}[self.ec_level]
        return data_codewords * 8

    def encode_data_bits(self):
        if self.mode == 'numeric':
            return self.encode_numeric()
        elif self.mode == 'alphanumeric':
            return self.encode_alphanumeric()
        else:
            return self.encode_byte()

    def encode_numeric(self):
        bits = ''
        for i in range(0, len(self.data), 3):
            group = self.data[i:i+3]
            if len(group) == 3:
                val = int(group)
                bits += format(val, '010b')
            elif len(group) == 2:
                val = int(group)
                bits += format(val, '07b')
            else:
                val = int(group)
                bits += format(val, '04b')
        return bits

    def encode_alphanumeric(self):
        table = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ $%*+-./: '
        bits = ''
        for i in range(0, len(self.data), 2):
            if i+1 < len(self.data):
                val = table.index(self.data[i]) * 45 + table.index(self.data[i+1])
                bits += format(val, '011b')
            else:
                val = table.index(self.data[i])
                bits += format(val, '06b')
        return bits

    def encode_byte(self):
        bits = ''
        for c in self.data:
            bits += format(ord(c), '08b')
        return bits

    def error_correct(self):
        self.final_bits = self.bit_stream

    def build_qr(self):
        # Place finder patterns
        self.place_finder(0, 0)
        self.place_finder(self.size - 7, 0)
        self.place_finder(0, self.size - 7)
        # Separators
        for i in range(8):
            self.modules[i][7] = False
            self.modules[7][i] = False
            self.modules[self.size - 8 + i][7] = False
            self.modules[7][self.size - 8 + i] = False
            self.modules[i][self.size - 8] = False
            self.modules[self.size - 8][i] = False
        # Alignment patterns
        self.place_alignment(6, 6)
        self.place_alignment(6, 26)
        self.place_alignment(26, 6)
        # Timing patterns
        for i in range(8, self.size - 8):
            self.modules[i][6] = (i % 2 == 0)
            self.modules[6][i] = (i % 2 == 0)
        # Dark module
        self.modules[8][self.size - 8] = True
        # Reserve format areas
        for i in range(9):
            if i != 6:
                self.modules[8][i] = None
                self.modules[i][8] = None
                self.modules[self.size - 1 - i][8] = None
                self.modules[8][self.size - 1 - i] = None
        # Place data
        self.place_data()

    def place_finder(self, x, y):
        for i in range(7):
            for j in range(7):
                if (i in [0,6] or j in [0,6]) or (2 <= i <= 4 and 2 <= j <= 4):
                    self.modules[x+i][y+j] = True
                else:
                    self.modules[x+i][y+j] = False

    def place_alignment(self, x, y):
        if self.modules[x][y] is not None:
            return
        for i in range(-2, 3):
            for j in range(-2, 3):
                if i == 0 and j == 0:
                    self.modules[x+i][y+j] = True
                elif abs(i) == 2 or abs(j) == 2:
                    self.modules[x+i][y+j] = True
                else:
                    self.modules[x+i][y+j] = False

    def place_data(self):
        bit_index = 0
        for col in range(self.size - 1, -1, -1):
            if col == 6:  
                continue
            if (self.size - 1 - col) % 2 == 0:  
                for row in range(self.size - 1, -1, -1):
                    if row == 6:  
                        continue
                    if self.modules[row][col] is False:
                        if bit_index < len(self.final_bits):
                            self.modules[row][col] = self.final_bits[bit_index] == '1'
                            bit_index += 1
            else:  
                for row in range(self.size):
                    if row == 6:
                        continue
                    if self.modules[row][col] is False:
                        if bit_index < len(self.final_bits):
                            self.modules[row][col] = self.final_bits[bit_index] == '1'
                            bit_index += 1

    def apply_best_mask(self):
        mask = lambda i, j: (i + j) % 2 == 0
        for i in range(self.size):
            for j in range(self.size):
                if self.modules[i][j] is not None and self.modules[i][j] is not False:
                    self.modules[i][j] ^= mask(i, j)

    def add_format_and_version(self):
        format_info = '101010000010010'  
        for i in range(15):
            bit = format_info[i] == '1'
            if i < 8:
                self.modules[8][i if i < 6 else i+1] = bit
            else:
                self.modules[14 - (i-8)][8] = bit
        for i in range(15):
            bit = format_info[i] == '1'
            if i < 7:
                self.modules[self.size - 1 - i][8] = bit
            else:
                self.modules[8][self.size - 15 + i] = bit

    def save_image(self):
        img = Image.new('L', (self.size + 8, self.size + 8), 255)
        pixels = img.load()
        for i in range(self.size):
            for j in range(self.size):
                val = self.modules[i][j]
                if val is None:
                    pixels[i+4, j+4] = 255
                else:
                    pixels[i+4, j+4] = 0 if val else 255
        img.save('qr_code.png')

if __name__ == '__main__':
    import sys
    data = sys.argv[1] if len(sys.argv) > 1 else 'data:text/html,<h1>Hey Hi Pavan Gowda T s here</h1>'
    qr = QRCodeGenerator(data)