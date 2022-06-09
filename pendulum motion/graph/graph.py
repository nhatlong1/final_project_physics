import matplotlib.pyplot as plt
import cv2




def coordinates_process():
	temp_1 = []
	temp_2 = []
	poistion_x = []
	poistion_y = []
	

	coordinates = open('C:/Users/MCM/Documents/final_cs101/pendulum motion/graph/coordinates.txt')
	y = coordinates.readlines()
	for i in y:
		temp_1.append((i.split(' ')))

	count = open('C:/Users/MCM/Documents/final_cs101/pendulum motion/graph/times.txt')
	x = count.readlines()
	for i in x:
		temp_2.append((i.split(' ')))

	for i in range(len(temp_1)):
		for j in range(len(temp_1[i])):
			poistion_x.append(int(temp_1[i][j]))

	for i in range(len(temp_2)):
		for j in range(len(temp_2[i])):
			poistion_y.append(int(temp_2[i][j]))

	del poistion_y[len(poistion_x):]

	plt.plot(poistion_y,poistion_x)
	plt.title('Pendulum Graph')
	plt.xlabel('x')
	plt.ylabel('y')
	plt.savefig('graph.png')
	graph = 'graph.png'

	img = cv2.imread(graph)
	for i in range(1000):
		cv2.imshow('test', img)
	# plt.imshow(img)
# coordinates_process()