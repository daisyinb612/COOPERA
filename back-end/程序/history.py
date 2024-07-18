import os
from openpyxl import Workbook
from datetime import datetime

def create_xlsx_file(folder_path="./消息历史"):
   if not os.path.exists(folder_path):
       raise ValueError("The specified folder does not exist.")
   current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
   file_name = f"{current_time}.xlsx"
   file_path = os.path.join(folder_path, file_name)
   wb = Workbook()
   wb.save(file_path)
   print(f"Excel file created: {file_path}")
   return file_path