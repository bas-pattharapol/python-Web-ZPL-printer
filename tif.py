'''import socket
mysocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)         
host = "192.168.254.254" 
port = 9100   
try:           
	mysocket.connect((host, port)) #connecting to host
	data = "ภัทรพล"
	mysocket.send(b"^XA^FXNow some text^FS^FO20,130^A@N,50,70,R:TH.FNT,20,20^FDtest..."+data+"  ^FS^XZ")#using bytes
	mysocket.close () #closing connection
except:
	print("Error with the connection")

'''

from sbpl import *
from PIL import Image
import io

json_str = [
              {"host":"10.11.1.15", "port": 9100, "communication": "SG412R_Status5"},
              [
                  {"set_label_size": [440, 176]},
                  {"shift_jis": 0},
                  {"rotate_270": 0},   
                  {"comment": "==Material Name=="},
                  {"pos": [180, 200], "expansion": [1300], "ttf_write": "บี ไนซ์ จุ ดซ้อนเร้น 150 มล.x3  ีสชมพู", "font": "CmPrasanmit Bold.ttf"},                                        
                  {"comment": "==Material Name=="},
                  {"pos": [160, 280], "expansion": [1800], "ttf_write": "032-0107", "font": "CmPrasanmit Bold.ttf"},
                  {"comment": "==barcode=="},
                  {"pos": [120, 225], "itf2of5": ["7885198908021", 2, 45]},   
                  {"comment": "== ID =="},
                  {"pos": [75, 230], "expansion": [1700], "ttf_write": "7 8851989 0802 1", "font": "CmPrasanmit Bold.ttf"},                             
                  {"rotate_0": 0},      
                  {"print": 2}
              ]
          ]
          

comm = SG412R_Status5()
gen = LabelGenerator()
parser = JsonParser(gen)
parser.parse(json_str)
print(json_str)
parser.post(comm)
