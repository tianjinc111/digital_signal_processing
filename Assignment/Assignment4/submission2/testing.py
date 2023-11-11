class Node :

  def __init__(self, value) :
    self.data = value
    self.left = self.right = None
  

class BinaryTree :

  def __init__(self) :
    self.root = None
  
  def in_order(self, node) :
    if (node != None) :
      self.in_order(node.left)
      print(node.data, end="  ")
      self.in_order(node.right)
    
  
  def pre_order(self, node) :
    if (node != None) :
      print(node.data, end="  ")
      self.pre_order(node.left)
      self.pre_order(node.right)
    
  
  def post_order(self, node) :
    if (node != None) :
      self.post_order(node.left)
      self.post_order(node.right)
      print(node.data, end="  ")
    
  
  def swap(self, first, second) :
    value = first.data
    first.data = second.data
    second.data = value
  
  def maxHeap(self, head) :
    if (head == None):
      return
    self.maxHeap(head.left)
    self.maxHeap(head.right)
    if (head.left != None and head.left.data > head.data) :
      self.swap(head, head.left)
      self.maxHeap(head)
    
    if (head.right != None and head.right.data > head.data) :
      self.swap(head, head.right)
      self.maxHeap(head)
    

def main() :
  obj = BinaryTree()
  # Make A Binary Tree
  #
  #          5
  #         /  \
  #        4    7
  #       /    /  \
  #      3    6    10
  #       \    \
  #        9    8


                #20
            #13      5

        #10    12   8    1 

    #9     3  11  2 6 21

  #  A = <20, 13, 5, 10, 12, 8, 1, 9, 3, 11, 2, 6, 21>
  obj.root = Node(20)
  obj.root.left = Node(13)
  obj.root.right = Node(5)
  obj.root.right.right = Node(10)
  obj.root.right.left = Node(6)
  obj.root.left.left = Node(3)
  obj.root.right.left.right = Node(8)
  obj.root.left.left.right = Node(9)
  print("\nBefore Convert ")
  print("In-order Data : ")
  obj.in_order(obj.root)
  print("\nPre-order Data : ")
  obj.pre_order(obj.root)
  print("\nPost-order Data : ")
  obj.post_order(obj.root)
  obj.maxHeap(obj.root)
  print("\nAfter Convert ")
  print("In-order Data : ")
  obj.in_order(obj.root)
  print("\nPre-order Data : ")
  obj.pre_order(obj.root)
  print("\nPost-order Data : ")
  obj.post_order(obj.root)


if __name__ == "__main__":
  main()