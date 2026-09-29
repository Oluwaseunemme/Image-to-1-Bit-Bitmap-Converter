from PIL import Image

# Load image and convert to grayscale
img = Image.open("0924a7ef295741e916c8f42512bbe5bd.jpg").convert("L")

img = img.resize((256, 256))

# Choose a threshold: pixels <= threshold -> 1 else 0 (you can invert if you want)
threshold = 128

w, h = img.size
binary = []

for y in range(h):
    row = []
    for x in range(w):
        pixel = img.getpixel((x, y))  # 0..255
        bit = 0 if pixel <= threshold else 1 #this means any color int value above 128 is 1 while below is 0
        row.append(bit)
    binary.append(row)

for row in binary[:20]:
    print("".join(str(b) for b in row))

with open("output_bitmap.txt", "w") as f:
    for row in binary:
        f.write("".join(str(b) for b in row) + "\n")
