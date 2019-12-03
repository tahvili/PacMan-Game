
import pygame
from typing import*
from vector import Vector2
from constants import *
from stack import Stack

class Node:

    """
     A Node is really anything you want it to be. It's a very abstract thing.
     It's basically an abstract object that contains information.
     Usually when you're talking about nodes in video games, one of the most
     important pieces of information is the position of the node.
     You can also represent a node any way you like, we're going to represent
     a node as a red circle.

    Being a neighbor to any particular node has nothing to do with proximity.
    Two nodes can be right next to each other, but if they are not linked together,
    then they are not neighbors. If two nodes are connected to each other,
    then they are connected by a path. We'll represent a path by a straight line that joins two nodes together.
    That's how we can know visually that two nodes are connected to each other.

    """
    row: int
    column: int
    portalval = 0

    def __init__(self, row, column) -> None:
        """
        When we create a Node we pass in the row and column values and then
        compute the x and y position we want to place the Node on the screen.
        We also set up the neighbors as a dictionary. This way it's really easy
        to know which node is in which direction to this Node.
        """

        self.row, self.column = row, column
        self.position = Vector2(column * WIDTH, row * HEIGHT)
        self.neighbors = {UP: None, DOWN: None, LEFT: None, RIGHT: None}
        self.portals = None
        self.portalval = 0
        self.homegrid = False
        self.restrict_entry = False
        self.pacman_start = False
        self.ghost_start = False
        self.ghost_spawn = False

    def render(self, screen) -> None:
        """
        Render the Node so it appears on the screen.
        We draw all of the paths to the neighbors first as WHITE lines, and we
        draw the Node itself as a RED circle.
        """
        for n in self.neighbors.keys():
            if self.neighbors[n] is not None:
                pygame.draw.line(screen, WHITE, self.position.to_tuple(),
                                 self.neighbors[n].position.to_tuple(), 4)
                pygame.draw.circle(screen, RED, self.position.to_tuple(True), 12)


class NodeGroup:
    """
    This class links all the Nodes and ther pathhs to create a sort of
    Nodegroup to visually represent the pacman board for pacman to move around
    in.
    """
    nodeList: List[Node]
    level: int
    grid: List
    nodeStack: Stack
    portalSymbols: List
    nodeSymbols: List

    def __init__(self, level: int) -> None:
        """
        Initialises the  Node Group.
        """

        self.nodeList = []
        self.homeList = []
        self.level = level
        self.grid = self.read_maze_file(level)
        self.homegrid = self.get_home_grid()
        self.nodeStack = Stack()
        self.portalSymbols = ["z"]
        self.pathSymbols = ["p", "P"]
        self.nodeSymbols = ["+", "H", "S", "n", "N", "Y"] + self.portalSymbols
        self.create_node_list(self.grid, self.nodeList)
        self.create_node_list(self.homegrid, self.homeList)
        self.create_portals()
        self.set_home_nodes()

    def read_maze_file(self, textfile: Any) -> Any:
        """
        Get information from files.
        """
        f = open(textfile, "r")
        lines = [line.rstrip('\n') for line in f]
        grid = [line.split(' ') for line in lines]
        return grid

    def get_home_grid(self) -> List:
        """
        Returns the the positions of the ghost home in a list.
        """

        return [['0', '0', '+', '0', '0'], ['0', '0', '|', '0', '0'], ['+', '0', '|', '0', '+'], ['+', '-', 'S', '-', '+'], ['+', '0', '0', '0', '+']]

    def create_node_list(self, grid: List, nodeList: List) -> None:
        """
        This method creates a map based on text file passed into the
        function
        """
        startNode = self.get_first_node(grid)
        self.nodeStack.push(startNode)
        while not self.nodeStack.is_empty():
            node = self.nodeStack.pop()
            self.add_node(node, nodeList)
            left = self.get_path(LEFT, node.row, node.column - 1, nodeList, grid)
            right = self.get_path(RIGHT, node.row, node.column + 1, nodeList, grid)
            top = self.get_path(UP, node.row - 1, node.column, nodeList, grid)
            bottom = self.get_path(DOWN, node.row + 1, node.column, nodeList, grid)
            node.neighbors[LEFT] = left
            node.neighbors[RIGHT] = right
            node.neighbors[UP] = top
            node.neighbors[DOWN] = bottom
            self.add_to_stack(left, nodeList)
            self.add_to_stack(right, nodeList)
            self.add_to_stack(top, nodeList)
            self.add_to_stack(bottom, nodeList)

    def get_first_node(self, grid: List) -> Any:
        """
        This method will go into the grid list and find the first instance of a Node.
        This serves as our starting point before we go into the while loop.
        """
        rows = len(grid)
        cols = len(grid[0])
        nodeFound = False
        for i in range(rows):
            for j in range(cols):
                if grid[i][j] in self.nodeSymbols:
                    node = Node(i, j)
                    if grid[i][j] in self.portalSymbols:
                        node.portalval = grid[i][j]
                    return node
        return None

    def get_node(self, x: int, y: int, nodeList: List) -> Any:
        """
        This method simply looks for a node in the nodeList at the specified x and y position.
        If a node at this position exists, then it returns that Node object.
        If it doesn't exist, then it will return None.
        """
        for node in nodeList:
            if node.position.x == x and node.position.y == y:
                return node

        return None

    def get_node_from_node(self, node: Any, nodeList: List) -> Any:
        """
        what this method does is look for the specified node in the nodeList.
        If the node exists in the nodeList, then the method will return the Node
        object from the nodeList. If it doesn't exist in the nodeList, then it
        will just return the node that was initially inputted.
        This is needed in order to avoid having duplicate Nodes, because we will
        visit a node more than once.
        """

        if node is not None:
            for inode in nodeList:
                if node.row == inode.row and node.column == inode.column:
                    return inode

        return node

    def get_path(self, direction: Any, row: int, col: int, nodeList: List,
                 grid: Any) -> Any:
        """
        This method returns either a Node object or None. It follows a path in
        the specified direction and returns the Node object that is connected to
        the current node we're dealing with if there is one and if it already
        doesn't exist in the nodeList.
        """
        tempNode = self.follow_path(direction, row, col, grid)
        return self.get_node_from_node(tempNode, nodeList)

    def add_node(self, node: Any, nodeList: List) -> None:
        """
        This method simply adds a Node object to the nodeList if it already does
        not exist in the nodeList.
        """
        nodeInList = self.node_in_list(node, nodeList)
        if not nodeInList:
            nodeList.append(node)

    def add_to_stack(self, node: Any, nodeList: List) -> None:
        """
        This method adds a node to the stack if it already hasn't been added to
        the nodeList.
        """
        if node is not None and not self.node_in_list(node, nodeList):
            self.nodeStack.push(node)

    def node_in_list(self, node: Any, nodeList: List) -> bool:
        """
        This method is similar to the get_node method but instead of returning
        Nodes or None, it will return either True or False whether the specified
        node is in the nodeList or not.
        """
        for i in nodeList:
            if node.position.x == i.position.x and node.position.y == \
                    i.position.y:
                return True
        return False

    def create_portals(self) -> None:
        """
        Since we have already created all the nodes in the list, all we have to
        do is loop through and create a new link/path between the portals on the
        screen using the portal val variable.
        """
        d = {}
        for i in range(len(self.nodeList)):
            if self.nodeList[i].portalval != 0:
                if self.nodeList[i].portalval not in d.keys():
                    d[self.nodeList[i].portalval] = [i]
                else:
                    d[self.nodeList[i].portalval] += [i]
        for key in d.keys():
            node1, node2 = d[key]
            self.nodeList[node1].portals = self.nodeList[node2]
            self.nodeList[node2].portals = self.nodeList[node1]

    def set_home_nodes(self) -> None:
        """
        Creates nodes from the home_list.
        """

        for node in self.nodeList:
            if node.homegrid:
                node1 = node
                break
        node2 = node1.neighbors[LEFT]
        mid = (node1.position + node2.position) / 2
        mid = Vector2(int(mid.x), int(mid.y))
        vec = Vector2(self.homeList[0].position.x, self.homeList[0].position.y)
        for node in self.homeList:
            node.position -= vec
            node.position += mid
        node1.neighbors[LEFT] = self.homeList[0]
        node2.neighbors[RIGHT] = self.homeList[0]
        self.homeList[0].neighbors[RIGHT] = node1
        self.homeList[0].neighbors[LEFT] = node2
        self.homeList[0].restrict_entry = True
        self.homeList[0].ghost_start = True

    def path_to_follow(self, direction: Any, row: int, col: int, path: str,
                       grid: List) -> Any:
        """
        Looks for certain items in the grid, until we run into a node
        with a different value
        """
        tempSymbols = [path] + self.nodeSymbols + self.pathSymbols

        if grid[row][col] in tempSymbols:
            print(grid[row][col])
            while grid[row][col] not in self.nodeSymbols:
                if direction is RIGHT:
                    col += 1
                elif direction is LEFT:
                    col -= 1
                elif direction is UP:
                    row -= 1
                elif direction is DOWN:
                    row += 1
            node = Node(row, col)
            if grid[row][col] == "H":
                node.homegrid = True
            if grid[row][col] == "S":
                node.ghost_spawn = True
            if grid[row][col] == "Y":
                node.pacman_start = True
            if grid[row][col] in self.portalSymbols:
                node.portalval = grid[row][col]
            return node
        else:
            return None

    def follow_path(self, direction: Any, row: int, col: int, grid: List) ->Any:
        """
        Follows path in all four directions
        """
        rows = len(grid)
        columns = len(grid[0])

        if direction == LEFT and col >= 0:
            return self.path_to_follow(LEFT, row, col, '-', grid)
        elif direction == RIGHT and col < columns:
            return self.path_to_follow(RIGHT, row, col, "-", grid)
        elif direction == UP and row >= 0:
            return self.path_to_follow(UP, row, col, "|", grid)
        elif direction == DOWN and row < rows:
            return self.path_to_follow(DOWN, row, col, "|", grid)
        else:
            return None

    def render(self, screen) -> None:
        """
        draw all the nodes and paths in the NodeList
        """
        for node in self.nodeList:
            node.render(screen)
        for node in self.homeList:
            node.render(screen)

