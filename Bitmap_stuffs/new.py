b = "11111111"
n_bits = len(b)
width = (n_bits + 3) // 4  # number of hex digits
hex_str = f"0x{int(b, 2):0{width}X}"
print(hex_str)  # '55'