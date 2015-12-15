# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtBluetooth
from PIL import Image,ImageDraw,ImageFont
import binascii
import time
from functools import reduce


class MetawatchThread(QtCore.QObject):
  connected = QtCore.pyqtSignal()
  disconnected = QtCore.pyqtSignal()
  readyRead = QtCore.pyqtSignal()
  error = QtCore.pyqtSignal(str)

  def __init__(self, device, postman, parent=None):
    super(MetawatchThread, self).__init__(parent)
    self.postman = postman
    self.device = device
    self.dev = QtBluetooth.QBluetoothSocket(QtBluetooth.QBluetoothServiceInfo.RfcommProtocol)
    self.dev.readyRead.connect(self.readyRead.emit)
    self.CRC = CRC_CCITT()
    self.loop = QtCore.QEventLoop()
    self.timer = QtCore.QTimer()
    self.timer.setSingleShot(True)
    self.timer.timeout.connect(self.loop.quit)


  def connect(self):
    addr = QtBluetooth.QBluetoothAddress(self.device.address)
    print('connecting to', addr)
    self.dev.connected.connect(self.connected)
    self.dev.disconnected.connect(self.disconnected)
    self.dev.error.connect(self.onError)
    self.dev.connectToService(addr, QtBluetooth.QBluetoothUuid.SerialPort)


  def disconnect(self):
    self.dev.disconnectFromService()


  def onError(self, E):
    self.error.emit(self.dev.errorString())


  def buzz(self):
    msg = self.pack(b'\x23\x00\x01\xf4\x01\xf4\x01\x01')
    self.write(msg)
    self.postman.Post.emit(
        "MetawatchThread",
        self.device.getName(),
        str(binascii.hexlify(msg), 'utf-8'))


  def setButtonEnabled(self, button, value = True):
    #documentation says first butten, then modus
    msg = self.pack(b'\x46\x00\x00' + button + b'\x00\x34' + button)
    self.write(msg)
    self.postman.Post.emit(
        "MetawatchThread",
        self.device.getName(),
        str(binascii.hexlify(msg), 'utf-8'))


  def setButtonsEnabled(self, value = True):
    self.timer.start(100)
    self.loop.exec()
    self.setButtonEnabled(b'\x00')
    self.setButtonEnabled(b'\x01')
    self.setButtonEnabled(b'\x02')
    self.setButtonEnabled(b'\x03')
    self.setButtonEnabled(b'\x04')
    self.setButtonEnabled(b'\x05')
    self.setButtonEnabled(b'\x06')


  def pack(self, message):
    text=b'\x01'+bytes([len(message)+4])+message;
    crc=self.CRC.checksum(text);
    text=text+(crc&0xFF).to_bytes(1, byteorder='little')+(crc>>8).to_bytes(1, byteorder='little') #Little Endian
    return text


  def write(self, text):
    self.dev.write(text)
    self.timer.start(10)
    self.loop.exec()


  def writebuffer(self, mode, row1, data1, row2=None, data2=None):
    """Writes image data to the Draw Buffer.
    You'll need to send activatedisplay() to swap things over when done."""
    option=mode; #idle screen, single row.
    if row2:
      option = option | 0x10;

    packet=b'\x40' +  bytes([option]) + bytes([row1]) + data1[0:12] + b'\x00'
    if row2:
      packet= packet + bytes([row2]) + data2[0:11]
    self.write(self.pack(packet))


  def writeImage(self, mode=0, image="dalek.bmp", live=False, from_y=0, to_y=96, from_x=0, to_x=96):
    """Write a 1bpp BMP file to the watch in the given mode."""
    im=Image.open(image);
    pix=im.load();
    for y in range(max(from_y, 0), min(to_y, 96)):
      rowdat=b'';
      for x in range(max(from_x, 0), min(to_x, 96),8):
        byte=0;
        for pindex in range(0,8):
          pixel=pix[x+pindex,y];
          if (pixel > 0):
            pixel = 1
          byte =((byte>>1)|(pixel<<7))
        rowdat = rowdat + bytes([byte])
      self.writebuffer(mode, y, rowdat)
    self.write(self.pack(b'\x43\x00')) #swap DisplayBuffer


  def writeText(self,mode=0,text='', pos_x=0, pos_y=0):
    image = Image.new("L",(96,96), 'black')
    (zeilen, spalten) = self.draw_word_wrap(image,text,pos_x,pos_y)
    image.save('tmp.bmp','BMP')
    image.close()
    self.write(self.pack(b'\x42\x00\x01')) #remove Clock (Fullscreen)
    self.writeImage(mode,"tmp.bmp",live=False, from_y=pos_y, to_y=pos_y + (zeilen * 11))


  def draw_word_wrap(self, img, text, xpos=0, ypos=0, max_width=95):
    font=ImageFont.load_default()

    draw = ImageDraw.Draw(img)
    (text_size_x, text_size_y) = draw.textsize(text, font=font)
    remaining = max_width
    space_width, space_height = draw.textsize(' ', font=font)
    output_text = []
    for word in text.split(None):
      word_width, word_height = draw.textsize(word, font=font)
      if word_width + space_width > remaining:
        output_text.append(word)
        remaining = max_width - word_width
      else:
        if not output_text:
          output_text.append(word)
        else:
          output = output_text.pop()
          output += ' %s' % word
          output_text.append(output)
      remaining = remaining - (word_width + space_width)
    for text in output_text:
      draw.text((xpos, ypos), text, font=font, fill='white')
      ypos += text_size_y
    return (len(output_text), reduce(max, [len(s) for s in output_text]))


  def readAll(self):
    return self.dev.readAll()


class CRC_CCITT:
    def __init__(self, inverted=True):
        self.inverted=inverted
        self.tab=256*[[]]
        for i in range(256):
            crc=0
            c = i << 8
            for j in range(8):
                if (crc ^ c) & 0x8000:
                    crc = ( crc << 1) ^ 0x1021
                else:
                    crc = crc << 1
                c = c << 1
                crc = crc & 0xffff
            self.tab[i]=crc

    def update_crc(self, crc, c):
        c=0x00ff & (c % 256)
        if self.inverted: c=self.flip(c)
        tmp = ((crc >> 8) ^ c) & 0xffff
        crc = (((crc << 8) ^ self.tab[tmp])) & 0xffff
        return crc

    def checksum(self,str):
        crcval=0xFFFF
        for c in str:
            crcval=self.update_crc(crcval, c)
        return crcval

    def flip(self,c):
        l=[0, 8, 4, 12, 2, 10, 6, 14, 1, 9, 5, 13, 3, 11, 7, 15]
        return ((l[c&0x0F]) << 4) + l[(c & 0xF0) >> 4]
