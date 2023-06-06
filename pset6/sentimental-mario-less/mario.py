# TODO
from cs50 import get_int
# get_height
while True:
    height = get_int("Height: ")
    if height >= 1 and height <= 8:
        break

for i in range(height):
    # spaces
    print((height - 1 - i) * " ", end="")
    # hashes
    print((i + 1) * "#")
