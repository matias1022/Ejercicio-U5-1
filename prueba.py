import hashlib 
if __name__ == "__main__": 
 # cifrado de la clave utilizando md5 
 clave = '38309459' 
 result = hashlib.md5(bytes(clave, encoding='utf-8')) 
 # muestra la clave cifrada en hexadecimal, esta es la que se guarda en base de datos 
 print(result)
 print(result.hexdigest())