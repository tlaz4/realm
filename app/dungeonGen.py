import random

class binaryTree():
	def __init__(self, value):
		self.left = None
		self.right = None
		self.value = value

	def getLeftChild(self):
		return self.left

	def getRightChild(self):
		return self.right

	def split(self):
		# split room into 2 children, check if rooms width to height ratio is okay, else try to split again
		while True:
			children = self.value.generateChildRoom()
			if(self.tooSmallRatio(children)):
				pass
				#print("Too small of ratio")
			else:
				self.left = binaryTree(children[0])
				self.right = binaryTree(children[1])
				return

	def tooSmallRatio(self, children):
		if(children[0].height / children[0].width < 0.40 or children[1].height / children[1].width < 0.40
		or children[0].width / children[0].height < 0.40 or children[1].width / children[1].height < 0.40):
			return True
		else: 
			return False

	def getValue(self):
		return self.value.returnCoords()

class room():
	def __init__(self, height, width, x, y):
		self.height = height
		self.width = width
		self.x = x
		self.y = y
		self.center = (self.x + self.width / 2, self.y + self.height /2)
		
	def generateChildRoom(self):
		split = random.randint(0, 1)
		
		if split == 1:
			rndX = random.randint(1, self.x + self.width)
			splitWidth1 = (self.width - rndX) + self.x
			splitWidth2 = self.width - splitWidth1
			# solve issue of division by zero, not sure why it is occuring but this is a temp fix
			if splitWidth1 == 0:
				splitWidth1 += 1
			if splitWidth2 == 0:
				splitWidth2 += 1
			#print(rndX, split, self.center, splitWidth1, splitWidth2, self.height)
			return [room(self.height, splitWidth2, self.x, self.y),
				room(self.height, splitWidth1, rndX, self.y)]

		else:
			rndY = random.randint(1, self.y + self.height)
			splitHeight1 = (self.height - rndY) + self.y
			splitHeight2 = self.height - splitHeight1
			#print("height", splitHeight1, splitHeight2)
			#print(rndY, split, self.center, splitHeight1, splitHeight2, self.width)
			return [room(splitHeight2, self.width, self.x, self.y),
					room(splitHeight1, self.width, self.x, rndY)]

	def getCoords(self):
		#print(self.height, self.width, self.x, self.y, self.center)
		pass

	def returnCoords(self):
		return [self.height, self.width, self.x, self.y, self.center]
		
def createNodes(node, depth):
	if depth == 0:
		return
	else:
		node.split()
		createNodes(node.getLeftChild(), depth - 1)
		createNodes(node.getRightChild(), depth - 1)

	
def traverseTree(node, childRooms):
	# for the purpose of this traversal, only append the final children of tree to a list
	# for simplicity once last child node is recieved, hollow it? since node is a leaf containing the room
	if node.getLeftChild() == None or node.getRightChild == None:
		childRooms.append(node)
		# this makes the function slightly more efficient and makes more sense for final product
		#childRooms.append(hollowRoom(node.getValue()))
		return
	
	else:
		traverseTree(node.getLeftChild(), childRooms)
		traverseTree(node.getRightChild(), childRooms)

# perhaps this should be a function of the room class? could work on itself instead of passing a node
def hollowRoom(node):
	# return a new room based on the node by randomly "hollowing" it
	hollowedRoomX = node[2] + random.randint(0, node[1] // 3)
	hollowedRoomY = node[3] + random.randint(0, node[0] // 3)
	hollowedRoomW = node[1] - (hollowedRoomX - node[2])
	hollowedRoomH = node[0] - (hollowedRoomY - node[3])
	return room(hollowedRoomH, hollowedRoomW, hollowedRoomX, hollowedRoomY)

def getDungeon():
	# three global lists, we can shorten this to one list
	childRooms = []
	roomCoords = []
	hollowedRooms = []

	# create the root room as a root of a binary tree
	rootRoom = room(100, 100, 0, 0)
	root = binaryTree(rootRoom)

	# recursively divide the root by the value passed, creating a full tree, and then traverse it to reach
	# final children, adding the child rooms to a list
	createNodes(root, 4)
	traverseTree(root, childRooms)

	# possibly eliminate this function, we can simply hollow rooms directly
	# mainly used for display purposes on how rooms are recursively generated
	for aRoom in childRooms:
		roomCoords.append(aRoom.getValue())
		#print(roomCoords)

	for coord in roomCoords:
		hollowedRooms.append(hollowRoom(coord).returnCoords())

	return (roomCoords, hollowedRooms)