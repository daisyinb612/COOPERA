class FileIndex:
   def __init__(self):
       self.index = {}
 
   def add_file(self, filename, file_list):
       """添加一个新的文件和对应的列表到索引中"""
       if filename not in self.index:
           self.index[filename] = file_list
       else:
           print(f"File {filename} already exists in the index.")
 
   def get_list(self, filename):
       """检索文件对应的列表"""
       return self.index.get(filename, "File not found in the index.")
 
   def update_list(self, filename, new_list):
       """更新文件对应的列表"""
       if filename in self.index:
           self.index[filename] = new_list
       else:
           print(f"File {filename} not found in the index.")
 
   def display_index(self):
       """显示当前索引的内容"""
       for filename, file_list in self.index.items():
           print(f"File: {filename}, List: {file_list}")

''' 
file_index = FileIndex()
file_index.add_file('file1.txt', [1, 2, 3])
file_index.add_file('file2.txt', [4, 5, 6])
file_index.display_index()
print(file_index.get_list('file1.txt'))
file_index.update_list('file1.txt', [7, 8, 9])
file_index.display_index()'''