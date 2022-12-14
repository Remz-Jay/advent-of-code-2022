from src.definitions import INPUT_DIR
import logging
from anytree import Node, RenderTree


class Day7:
    file = None
    ans1 = 0
    ans2 = []
    free_space = 70000000

    def __init__(self):
        self.file = open(f"{INPUT_DIR}/day7.txt", "r")
        dirstack = [None]
        for line in self.file:
            if line.startswith('$'):
                bits = line.split()
                if bits[1] == 'cd':
                    if bits[2] == '..':
                        dirstack.pop()
                    else:
                        if bits[2] == '/':
                            dirstack[0] = Node('root', parent=dirstack[-1], type='Dir', size=0)
                        else:
                            dirstack.append(Node(bits[2], parent=dirstack[-1], type='Dir', size=0))
            elif not line.startswith('dir'):
                bits = line.split()
                Node(bits[1], parent=dirstack[-1], type='File', size=bits[0])

        for pre, fill, node in RenderTree(dirstack[0]):
            logging.info("%s%s %s %s" % (pre, node.name, node.type, node.size))
        self.free_space -= self.get_dir_size(dirstack[0])
        self.traverse_tree(dirstack[0])

    def __del__(self):
        self.file.close()

    def traverse_tree(self, node):
        size = self.get_dir_size(node)
        if self.free_space + size > 30000000:
            self.ans2.append((size, node))
        if size < 100000:
            self.ans1 += size
        for n in node.children:
            if n.type == "Dir":
                self.traverse_tree(n)

    def get_dir_size(self, node):
        size = 0
        for n in node.children:
            if n.type == "Dir":
                size += self.get_dir_size(n)
            else:
                size += int(n.size)
        return size

    def solve1(self):
        logging.info("Executing Solve1")
        return self.ans1

    def solve2(self):
        logging.info("Executing Solve2")
        self.ans2.sort(key=lambda a: a[0])
        return self.ans2[0][0]


if __name__ == '__main__':
    d = Day7()
    print(f"ans1: {d.solve1()}")
    print(f"ans2: {d.solve2()}")
