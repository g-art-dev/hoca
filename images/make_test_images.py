from PIL import Image

size = (256, 256)
basename = "test_image"


def make_image(basename, size, step):
    image = Image.new("RGBA", size)
    image_data = image.load()
    for x in range(size[0]):
        for y in range(size[1]):
            r = (x // step) * step
            g = (y // step) * step
            b = 255 - r
            a = 255 - g
            image_data[x, y] = (r, g, b, a)

    image.save(f"{basename}_step={step}.png")


for step in (1, 16, 64):
    make_image(basename, size, step)
