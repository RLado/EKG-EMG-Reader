import argparse

import serial


class ekg_packet:
    def __init__(self,num_channels=6,header_len=4):
        self.num_channels=num_channels
        self.header_len=header_len
        self.data=b''
        self.read_error=True
        #Packet data
        self.sync0=b'\xa5'
        self.sync1=b'\x5a'
        self.protocol_ver=None
        self.packet_count=0
        self.channel=[None]*num_channels
        self.tail=b'\x01'
    
    def __len__(self):
        return self.num_channels*2+self.header_len+1
    
    def parse(self):
        '''
         //Write packet header and footer
        TXBuf[0] = 0xa5;    //Sync 0
        TXBuf[1] = 0x5a;    //Sync 1
        TXBuf[2] = 2;       //Protocol version
        TXBuf[3] = 0;       //Packet counter
        TXBuf[4] = 0x02;    //CH1 High Byte
        TXBuf[5] = 0x00;    //CH1 Low Byte
        TXBuf[6] = 0x02;    //CH2 High Byte
        TXBuf[7] = 0x00;    //CH2 Low Byte
        TXBuf[8] = 0x02;    //CH3 High Byte
        TXBuf[9] = 0x00;    //CH3 Low Byte
        TXBuf[10] = 0x02;   //CH4 High Byte
        TXBuf[11] = 0x00;   //CH4 Low Byte
        TXBuf[12] = 0x02;   //CH5 High Byte
        TXBuf[13] = 0x00;   //CH5 Low Byte
        TXBuf[14] = 0x02;   //CH6 High Byte
        TXBuf[15] = 0x00;   //CH6 Low Byte 
        TXBuf[2 * NUMCHANNELS + HEADERLEN] =  0x01;	// Switches state
        '''        
        #Check if last byte is correct
        if self.data[-1:]!=self.tail:
            self.read_error=True
        else:
            self.read_error=False
            #Parse
            for i in range(0,self.num_channels*2,2):
                self.channel[i//2]=int.from_bytes(self.data[self.header_len+i:self.header_len+i+2],'big') #big endian
            self.protocol_ver=self.data[2]
            self.packet_count=self.data[3]
        
class serial_ekg:
    def __init__(self,port='/dev/ttyACM0',baudrate=57600,timeout=1,packet_num_channels=6,packet_header_len=4):
        self.ser=serial.Serial(port, baudrate, timeout=timeout)
        self.packet=ekg_packet(num_channels=packet_num_channels,header_len=packet_header_len)
    
    def read_packet(self):
        self.packet.data=b''
        last_byte=b'' #b'\x00'
        synced=False
        while len(self.packet.data)<len(self.packet):
            new_byte=self.ser.read(1)
    
            if self.packet.sync0+self.packet.sync1 in last_byte+new_byte and not synced:     #if b'\xa5Z' in last_byte+new_byte and not synced:
                #Add bytes to packet
                self.packet.data+=last_byte
                self.packet.data+=new_byte
                synced=True
            elif synced:
                self.packet.data+=new_byte
            
            last_byte=new_byte
        
        self.packet.parse()

    def __del__(self):
        try:
            self.ser.close()
        except AttributeError:
            pass

if __name__=='__main__':
    parser=argparse.ArgumentParser(description='EKG/EMG data reader in real time')
    parser.add_argument('-p','--port',type=str,required=True,metavar='',help='Serial port')
    parser.add_argument('-b','--baud',type=int,required=True,metavar='',help='Baud rate')
    args=parser.parse_args()

    ekgSer=serial_ekg(port=args.port,baudrate=args.baud,timeout=1)
    
    while True:
        ekgSer.read_packet()

        if not ekgSer.packet.read_error:
            print(ekgSer.packet.packet_count)
            print(ekgSer.packet.channel)
