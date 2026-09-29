# 🖼️ Image to 1-Bit Bitmap Converter

A simple Python image-processing project that converts an image into a **1-bit black-and-white bitmap** represented as a 2D array of `0`s and `1`s.

The project demonstrates a basic image-processing pipeline:

**RGB Image → Grayscale → Resize → Threshold → Binary Bitmap**

The resulting bitmap can be saved as text and later converted into a format suitable for displaying images on **low-resolution OLED displays and other embedded graphics systems**.

## 🔍 How It Works

### 1. Load the image

The image is loaded using the Python Imaging Library (PIL/Pillow):

```python
img = Image.open("my-selfie.jpg").convert("L")
```

The `"L"` mode converts the image to grayscale, where each pixel has an intensity value between:

* `0` → Black
* `255` → White

Conceptually, grayscale conversion combines the original **8-bit Red, Green, and Blue channels** into a single intensity value using a weighted combination of RGB values. Green contributes more strongly because the human eye is more sensitive to green.

---

### 2. Resize the image

```python
img = img.resize((256, 256))
```

The image is resized to a fixed resolution.

This is particularly useful for embedded systems because displays usually have a fixed number of pixels.

For example:

```text
128 × 64 OLED  →  128 × 64 pixels
128 × 32 OLED  →  128 × 32 pixels
256 × 64 OLED  →  256 × 64 pixels
```

---

### 3. Apply a threshold

A threshold determines whether each grayscale pixel becomes a `0` or `1`.

```python
threshold = 128
```

The conversion is performed using:

```python
bit = 0 if pixel <= threshold else 1
```

Therefore:

```text
Pixel ≤ 128  →  0
Pixel > 128  →  1
```

The result is a **1-bit approximation** of the original image.

Instead of storing 256 possible grayscale values, each pixel now requires only **one bit**.

---

### 4. Build the 2D bitmap

The program loops through every pixel using its `x` and `y` coordinates:

```python
for y in range(h):
    row = []

    for x in range(w):
        pixel = img.getpixel((x, y))
        bit = 0 if pixel <= threshold else 1
        row.append(bit)

    binary.append(row)
```

The result is essentially a 2D matrix:

```text
[
  [0, 0, 1, 1, 1, 0, ...],
  [0, 1, 1, 0, 0, 1, ...],
  [1, 1, 1, 1, 0, 0, ...],
  ...
]
```

Each element represents one pixel.

---

## 📄 Output

The generated bitmap is written to:

```text
output_bitmap.txt
```

Each line represents one row of pixels.

Example:

```text
0000011111110000
0000111111111000
0001110000111100
0011100000011100
...
```

This makes the bitmap easy to inspect and understand before converting it into a more compact embedded format.

## ⚡ Why 1-Bit Images Are Useful in Embedded Systems

Many microcontroller displays, especially monochrome OLEDs, don't need full RGB image data.

For example, a `128 × 64` monochrome display contains:

```text
128 × 64 = 8192 pixels
```

With 1 bit per pixel:

```text
8192 bits ÷ 8 = 1024 bytes
```

So the complete image requires only about **1 KB** of bitmap data.

Compare that with an RGB image using 24 bits per pixel:

```text
8192 × 24 = 196,608 bits
              ≈ 24 KB
```

This is a major reduction in memory usage.

---

# 🔌 Using the Bitmap With a Microcontroller

The same concept can be used to generate image data for microcontrollers such as:

* ESP32
* ESP32-C3
* Arduino UNO
* Arduino Nano
* STM32
* RP2040
* Other embedded systems

For example, an image intended for a `128 × 64` OLED can first be converted to a `128 × 64` 1-bit bitmap.

The bitmap can then be packed into bytes and stored in program memory:

```cpp
const uint8_t imageBitmap[] PROGMEM = {
    0x00, 0x00, 0x3C, 0x42,
    0x81, 0xA5, 0x81, 0x42,
    // ...
};
```

The microcontroller can then send these bytes to an OLED controller such as an **SSD1306**.

Libraries such as Adafruit SSD1306 and U8g2 can use bitmap data to draw images, icons, logos, and custom graphics.

---

## 🧠 From Pixels to Bytes

The current Python program produces individual bits:

```text
10110010
```

Eight pixels can be packed into one byte:

```text
10110010
   ↓
0xB2
```

This is much more memory-efficient than storing each pixel as a separate character.

For example:

```text
8 pixels:

1 0 1 1 0 0 1 0

Packed byte:

10110010
```

A complete image can therefore be converted from:

```text
2D array of pixels
        ↓
1-bit pixels
        ↓
8 pixels per byte
        ↓
byte array
        ↓
microcontroller
        ↓
OLED display
```

## 🚀 Possible Improvements

This project can be extended to automatically generate embedded-ready bitmap arrays.

Possible improvements include:

* Support arbitrary image sizes
* Automatically resize to OLED resolution
* Invert black and white
* Add configurable threshold from the command line
* Generate C/C++ `uint8_t` arrays
* Generate Arduino `PROGMEM` bitmap data
* Support horizontal and vertical byte orientation
* Add dithering for better-looking images
* Support grayscale bitmap generation
* Generate bitmap data compatible with SSD1306/U8g2
* Create a simple GUI for selecting images and thresholds

For example, the final workflow could become:

```text
my-image.jpg
     ↓
Python image processor
     ↓
Grayscale conversion
     ↓
Resize to OLED resolution
     ↓
Threshold / dithering
     ↓
1-bit bitmap
     ↓
Pack 8 pixels → 1 byte
     ↓
Generate C/C++ array
     ↓
ESP32 / Arduino
     ↓
OLED
```

## 🛠️ Requirements

Install Pillow with:

```bash
pip install pillow
```

Then run:

```bash
python image_to_bitmap.py
```

Make sure the input image is available as:

```text
my-selfie.jpg
```

The generated bitmap will be saved as:

```text
output_bitmap.txt
```

## 📚 What This Project Demonstrates

This small project demonstrates several fundamental concepts:

* Digital image representation
* RGB → grayscale conversion
* Pixel manipulation
* Thresholding
* Binary image processing
* 2D arrays
* Coordinate-based image traversal
* Bit-level data representation
* Memory optimization
* Embedded graphics
* OLED bitmap generation

The main idea is simple:

> **An image can be reduced from millions of possible colors to a single bit per pixel, allowing it to be efficiently represented and displayed by resource-constrained microcontrollers.**
