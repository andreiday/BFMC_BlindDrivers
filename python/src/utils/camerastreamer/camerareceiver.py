# Copyright (c) 2019, Bosch Engineering Center Cluj and BFMC organizers
# All rights reserved.

# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:

# 1. Redistributions of source code must retain the above copyright notice, this
#    list of conditions and the following disclaimer.

# 2. Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.

# 3. Neither the name of the copyright holder nor the names of its
#    contributors may be used to endorse or promote products derived from
#    this software without specific prior written permission.

# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE
import sys
import time
import socket
import numpy as np
import cv2
from threading import Thread
from src.utils.templates.workerprocess import WorkerProcess
sys.path.append('.')

class CameraReceiver(WorkerProcess):
    # ===================================== INIT =========================================
    def __init__(self, inPs, outPs):
        """Process used for receiving frames from unity. It receives the images from unity and pipes through the output pipe. 
        The idea is to apply the imageprocessing algorithms on the simulation frames and then send data back to unity to be used in ML agents.

        Parameters
        ----------
        inPs : list(Pipe)
            List of input pipes
        outPs : list(Pipe)
            List of output pipes
        """
        super(CameraReceiver, self).__init__(inPs, outPs)

        self.port = 1234
        self.serverIp = '0.0.0.0'

        self.imgSize = (480, 640, 3)
    # ===================================== RUN ==========================================
    def run(self):
        """Apply the initializers and start the threads.
        """
        self._init_socket()
        super(CameraReceiver, self).run()

    # ====================== =============== INIT SOCKET ==================================
    def _init_socket(self):
        """Initialize the socket.
        """
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.server_socket.bind((self.serverIp, self.port))

    # ===================================== INIT THREADS =================================
    def _init_threads(self):
        """Initialize the read thread to receive the video.
        """
        readTh = Thread(name='StreamReceiving', target=self._read_stream, args=(self.outPs, ))
        self.threads.append(readTh)

    # ===================================== READ STREAM ==================================
    def _read_stream(self, outPs):
        """Read the image from input stream, decode it and show it.

        Parameters
        ----------
        outPs : list(Pipe)
            output pipes (not used at the moment)
        """
        print("Init read stream")
        try:
            while True:
                # decode image
                data, addr = self.server_socket.recvfrom(65534)
                stamp = time.time()

                if data:
                # ----------------------- read image -----------------------
                    frame = np.frombuffer(data, np.uint8)
                    frame = cv2.imdecode(frame, cv2.IMREAD_COLOR)
                    #frame = np.reshape(frame, self.imgSize)
                    #frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
                    
                    #
                    # # ----------------------- show images -------------------
                    
                    cv2.namedWindow('udpVid', cv2.WINDOW_NORMAL)
                    cv2.imshow('udpVid', frame)

                    for p in self.outPs:
                        p.send([[stamp], frame])

                    if cv2.waitKey(1) & 0xFF == ord('q'):
                        break
                else:
                    print("Empty data")
        except Exception as e:
            print("Found exception ", str(e))
        finally:
            self.server_socket.close()

        '''
        try:
            while True:

                # decode image
                data, addr = self.server_socket.recvfrom(65534)

                # bts = self.connection.recvfrom()
                # print(image)
                # print(addr)
                #image = Image.open(BytesIO(data))
                frame = np.frombuffer(
            data, dtype=np.uint8).reshape(self.imgSize)
                # image = BytesIO(data)
                # image.show()
                # image_len = struct.unpack('<L', self.connection.read(struct.calcsize('<L')))[0]
                # bts = self.connection.read(image_len)

                # ----------------------- read image -----------------------
                # image = np.frombuffer(BytesIO(data), np.uint8)
                # image = cv2.imdecode(image, cv2.IMREAD_COLOR)
                # image = np.reshape(image, self.imgSize)
                # image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
                #
                # # ----------------------- show images -------------------
                cv2.namedWindow('Image', cv2.WINDOW_NORMAL)
                cv2.imshow('Image', frame)

                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
        except:
            pass
        finally:
            #self.connection.close()
            self.server_socket.close()
        '''
