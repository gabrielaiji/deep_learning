from matplotlib import pyplot as plt
from PIL import Image

class RectangleBuilder:

    def __init__(self, path):
        self.count = 0
        self.path = path
        self.im = Image.open(path)
        self.fig = plt.figure()
        self.cid = self.fig.canvas.mpl_connect('button_press_event', self)

        self.x1 = 0
        self.x2 = 0
        self.y1 = 0
        self.y2 = 0

        self.ax = self.fig.add_subplot(111)
        self.ax.imshow(self.im)
        self.ax.set_title('click to build line segments')
        print("Close the plot window to go the next image to crop")
        plt.show()


    def __call__(self, event):
        #print('click', event)
        #if event.inaxes!=self.line.axes: return
        self.count +=1

        if(self.count ==1):
            self.x1 = event.xdata
            self.y1 = event.ydata
        elif (self.count ==2):
            self.x2 = event.xdata
            self.y2 = event.ydata

            self.xmin = min(self.x1, self.x2)
            self.xmax = max(self.x1, self.x2)

            self.ymin = min(self.y1, self.y2)
            self.ymax = max(self.y1, self.y2)


            self.line, = self.ax.plot([self.xmin, self.xmin, self.xmax, self.xmax, self.xmin], [self.ymin,self.ymax,self.ymax,self.ymin,self.ymin], color="r")
            self.line.figure.canvas.draw()
        else:
            #self.ax.lines.pop(0)
            self.line.remove()
            self.count = 1
            self.x1 = event.xdata
            self.y1 = event.ydata

            

    def getRect(self):
        return (self.xmin, self.ymin, self.xmax, self.ymax)



"""
path = '../data/global/combat/hariyama_carte_2.png'

im = Image.open(path)
#line, = ax.plot([0], [0])  # empty line

rectangle = RectangleBuilder(path)
crop_rectangle = rectangle.getRect()

cropped_im = im.crop(crop_rectangle)
cropped_im.save("test.png")
"""
#print("project after the input.")



