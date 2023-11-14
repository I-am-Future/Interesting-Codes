# image quad tree

import numpy as np
import cv2
from matplotlib import pyplot as plt

class QTNode:
    def __init__(self, startX, endX, startY, endY, img, children = None) -> None:
        self.startX = startX
        self.endX = endX
        self.startY = startY
        self.endY = endY
        self.img = img
        self.children = children
        self.color = None


MIN_SIZE = 10
MAX_VAR = 500
MIN_LEVEL = 3

def buildTree(node: QTNode, level = 0):
    if (node.endX - node.startX < MIN_SIZE) or (node.endY - node.startY < MIN_SIZE):
        node.color = node.img[node.startX: node.endX, node.startY: node.endY, :].mean(axis=0).mean(axis=0)
        return 
    
    imgVar = np.var(node.img[node.startX: node.endX, node.startY: node.endY, :])
    # calculate per-channel var
    # imgVar = node.img[node.startX: node.endX, node.startY: node.endY, :].var(axis=0).var(axis=0)

    # when variance is too large, do splitting
    # or when level is low, do splitting
    if level < MIN_LEVEL or imgVar > MAX_VAR:
    # if (imgVar > MAX_VAR).any():
        # do splitting
        midX = (node.startX + node.endX) // 2
        midY = (node.startY + node.endY) // 2
        node.children = []
        node.children.append(QTNode(node.startX, midX, node.startY, midY, node.img))
        node.children.append(QTNode(node.startX, midX, midY, node.endY, node.img))
        node.children.append(QTNode(midX, node.endX, node.startY, midY, node.img))
        node.children.append(QTNode(midX, node.endX, midY, node.endY, node.img))

        # do buildTree in children
        for child in node.children:
            buildTree(child, level + 1)
    else:
        # calculate the color
        node.color = node.img[node.startX: node.endX, node.startY: node.endY, :].mean(axis=0).mean(axis=0)


def coloring(node: QTNode, img: np.ndarray):
    if node.children is None:
        img[node.startX: node.endX, node.startY: node.endY, :] = node.color.astype(np.uint8)
    else:
        for child in node.children:
            coloring(child, img)


def main(img_path):
    img = cv2.imread(img_path)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    if img is None:
        print('Read img failed!')

    # resize proportionally to height=512
    h = img.shape[0]
    ratio = 512 / h
    img = cv2.resize(img, (int(img.shape[1] * ratio), 512))

    h, w, _ = img.shape
    root = QTNode(0, h, 0, w, img)
    buildTree(root)

    result = np.zeros_like(img, dtype=np.uint8)
    coloring(root, result)

    plt.imshow(result)
    plt.show()

if __name__ == '__main__':
    main('cat.jpg')

    main('monalisa.png')
