import matplotlib.pyplot as plt
import matplotlib
#import cv2

matplotlib.rcParams['interactive'] == True
matplotlib.use('MacOSX')

def coordinates_process():
    temp_1 = []
    temp_2 = []
    position_x = []
    position_y = []
	
    coordinates = open('coordinates.txt')
    lines = coordinates.readlines()
	
    for line in lines:
        temp_1.append((line.split(' ')))

    count = open('times.txt')
    lines_count = count.readlines()
	
    for line_count in lines_count:
        temp_2.append((line_count.split(' ')))

    for i in range(len(temp_1)):
        for j in range(len(temp_1[i])):
            position_x.append(int(temp_1[i][j]))

    for i in range(len(temp_2)):
        for j in range(len(temp_2[i])):
            position_y.append(int(temp_2[i][j]))

    del position_y[len(position_x):]

    return position_x, position_y
   
    #plt.plot(position_y, position_x)
    #plt.title('Pendulum Graph')
    #plt.xlabel('Position update instance')
    #plt.ylabel('Position with respect to balance')
    #plt.savefig('graph.png')
    #graph = 'graph.png'

    #img = plt.imread(graph)
    #for i in range(1000):
        #plt.imshow(img)
    #plt.show()
