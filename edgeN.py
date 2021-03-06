from PIL import Image
import random
import math
#import Queue




class pixel:
    def __init__(self, r, g, b):
       self.r = r
       self.g = g
       self.b = b

def createMatrix(nums, image, WIDTH, HEIGHT, pt):
    (pr, pc) = pt
    matrix = {}
    for r in range(pr-150, pr+150):
        for c in range(pc-150, pc+150):
            if(r <= 0 or r >= HEIGHT-1 or c <= 0 or c >= WIDTH-1):
                continue
            p = nums[WIDTH*r + c]
            matrix[(r,c)] = pixel(p[0], p[1], p[2])

    return matrix

def calculateAverageColor(matrix, r, c):
	(avgR, avgG, avgB) = (0, 0, 0)
	for i in range(r-5, r+5):
		for j in range(c-5, c+5):
			avgR += matrix[(i, j)].r
			avgG += matrix[(i, j)].g
			avgB += matrix[(i, j)].b

	return (int(avgR/100.0), int(avgG/100.0), int(avgB/100.0))

def cropppedImage(matrix, center, avg, WIDTH, HEIGHT):
	(r, c) = center
	(avgR, avgG, avgB) = avg
	selectedObj = {}
	for i in range(r-150, r+150):
		for j in range(c-150, c+150):
			if(i <= 0 or i >= HEIGHT-1 or j <= 0 or j >= WIDTH-1):
				continue
			(r1, g1, b1) = (matrix[(i,j)].r, matrix[(i,j)].g, matrix[(i,j)].b)
			(dr, dg, db) = (abs(matrix[(i, j)].r -  avgR), abs(matrix[(i, j)].g -  avgG), abs(matrix[(i, j)].b -  avgB))
			dominantColor = max(avgR, avgG, avgB)
			threshold = {}
			threshold[avgR] = 50
			threshold[avgG] = 50
			threshold[avgB] = 50
			threshold[dominantColor] = 65

			if(dr <= threshold[avgR] and dg <= threshold[avgG] and db <= threshold[avgB]):
				selectedObj[(i,j)] = 1
			else:
				selectedObj[(i,j)] = 0

	for i in range(r-150, r+150):
		seen = (False, 0, c-150)
		for j in range(c-150, c+150):
			if(i <= 0 or i >= HEIGHT-1 or j <= 0 or j >= WIDTH-1):
				continue
			if(selectedObj[(i,j)] == 1):
				if(seen[0]):
					for p in range(seen[2], j):
						selectedObj[(i,p)] = 1
					seen = (True, seen[1], j)
				else:
					seen = (False, seen[1] + 1, j)
					if(seen[1] >= 4):
						seen = (True, seen[1], seen[2])

	return selectedObj

def grabObject(backgroundImg, x, y):
	im = Image.open(backgroundImg, 'r')
	WIDTH, HEIGHT = im.size
	pixel_values = list(im.getdata())

	###################################################   This is where we edit the pixels
	image = {}
	matrix = createMatrix(pixel_values, image, WIDTH, HEIGHT, (y,x))


	(avgR, avgG, avgB) = calculateAverageColor(matrix, y, x)
	selectedObj = cropppedImage(matrix, (y,x), (avgR, avgG, avgB), WIDTH, HEIGHT)


	im = Image.new("RGBA", (300, 300))
	pix = im.load()

	for r in range(y-150, y+150):
		for c in range(x-150, x+150):
			if(0 < r and r < HEIGHT -1 and 0 < c and c < WIDTH-1 and selectedObj[(r,c)] == 1):
				red = matrix[(r,c)].r
				green = matrix[(r,c)].g
				blue = matrix[(r,c)].b
				a = 255
			else:
				(red, green, blue, a) = (100, 100, 100, 0)
			pix[c - (x-150), r - (y-150)] = (red, green, blue, a)

	im.save("output.png", "PNG")


# grabObject("../../../Desktop/startPage.jpg", 1154, 514)





