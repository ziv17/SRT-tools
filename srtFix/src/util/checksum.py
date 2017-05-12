'''
Created on May 11, 2017

@author: Ziv
'''
import struct, os

def hashFile(name):
  try:
    longlongformat='<q'  # little-endian long long
    bytesize=struct.calcsize(longlongformat)
    f=open(name, "rb")
    filesize=os.path.getsize(name)
    tHash=filesize
    if filesize<65536*2:
      return "SizeError"
    for x in range(65536/bytesize):
      buffer=f.read(bytesize)
      (l_value,)=struct.unpack(longlongformat, buffer)
      tHash+=l_value
      tHash=tHash & 0xFFFFFFFFFFFFFFFF  # to remain as 64bit number
    f.seek(max(0, filesize-65536), 0)
    for x in range(65536/bytesize):
      buffer=f.read(bytesize)
      (l_value,)=struct.unpack(longlongformat, buffer)
      tHash+=l_value
      tHash=tHash & 0xFFFFFFFFFFFFFFFF
    f.close()
    returnedhash="%016x"%tHash
    return returnedhash
  except(IOError):
    return "IOError"
