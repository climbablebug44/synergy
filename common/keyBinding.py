class temp:
  
  keys = ['W', 'S', 'A', 'D', 'P', 'C', 'U', 'I', 'Space', 'E', 'B', 'Q', 'Done']
  
  def __init__(self):
    self.arr = temp.keys
  
  def funct1(self):
    file1 = open("file.txt",w+")
    file1.write(self.arr)
    file1.close() 
  
  def funct2(self, repl):
    self.arr = repl
    file1 = open("file.txt",w+")
    file1.write(self.arr)
    file1.close() 
