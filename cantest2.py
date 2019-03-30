import can
import os
from Tkinter import *
import Tkinter
import time
import subprocess
log_path = "/home/pi/cantest/log.txt"
can_addr = 3
start_data = 7

sl = 8
SAS_sl = 16

autoOn_sb = 0
Acc_On_sb = 8
break_On_sb = 16
PRND_sb = 24
SAS_pos_sb = 32
acc_pos_sb = 48
break_pos_sb = 56

act_kph_sb = 0
set_kph_sb = 8
state_sb = 16
radar_sb = 24
camera_sb = 32
ACU_sb = 40
lon_con_sb = 48
lat_con_sb = 56

prv_state = 0

bus = can.interface.Bus(channel='can0', bustype='socketcan_native', bitrate = 500000)

os.system("sudo /sbin/ip link set can0 up type can bitrate 500000")

#time.sleep(5)
root = Tkinter.Tk()
canvas = Tkinter.Canvas(root, width = 500, height = 500)
canvas.pack()
canvas.create_oval(5, 100, 55, 150) #Radar Ready
canvas.create_oval(5, 150, 55, 200) #camera Ready
canvas.create_oval(5, 200, 55, 250) #ACU Ready
canvas.create_oval(5, 250, 55, 300) #Lon Ctrl
canvas.create_oval(5, 300, 55, 350) #Lat Ctrl
canvas.create_oval(200, 150, 300, 250) #Auto Driving

l_cam = Tkinter.Label(root, text = 'Camera Ready')
l_rad = Tkinter.Label(root, text = 'Rader Ready')
l_acu = Tkinter.Label(root, text = 'ACU Ready')
l_lon = Tkinter.Label(root, text = 'LON CTRL')
l_lat = Tkinter.Label(root, text = 'LAT CTRL')
l_sta = Tkinter.Label(root, text = 'Auto Driving')
l_vsp = Tkinter.Label(root, text = 'Vehicle\nSpeed[KPH]')
l_ssp = Tkinter.Label(root, text = 'Set\nSpeed[KPH]')
l_vsd = Tkinter.Label(root, text = '0', font=("",40))
l_ssd = Tkinter.Label(root, text = '0', font=("",40))

l_rad.place(x = 65, y = 115)
l_cam.place(x = 65, y = 165)
l_acu.place(x = 65, y = 215)
l_lon.place(x = 65, y = 265)
l_lat.place(x = 65, y = 315)
l_sta.place(x = 210, y = 120)
l_vsp.place(x = 170, y = 260)
l_ssp.place(x = 270, y = 260)
l_vsd.place(x = 160, y = 310)
l_ssd.place(x = 270, y = 310)

root.update()

while  1:
    try :
        bus = can.interface.Bus(channel='can0', bustype='socketcan_native', bitrate = 500000)

        os.system("sudo /sbin/ip link set can0 up type can bitrate 500000")
        os.system("sudo ip link set can0 type can restart")
        raw_data = bus.recv(3.0)

        data = str(raw_data).split()
        print(data)
        if data[can_addr] == '0200':
            now = time.localtime()
            datetime = str(now.tm_year) +"-"+ str(now.tm_mon) +"-"+ str(now.tm_mday) +"-"+ str(now.tm_hour) +"-"+ str(now.tm_min) +"-"+ str(now.tm_sec)
            """ 
            f = open(log_path, "a+")
            log_data = data.append(datetime)
            f.write(str(data) + "\n")
            f.close()
            """
            one_byte = bin(int(data[start_data], 16))[2:].zfill(8)
            two_byte = bin(int(data[start_data + 1], 16))[2:].zfill(8)
            thr_byte = bin(int(data[start_data + 2], 16))[2:].zfill(8)
            fou_byte = bin(int(data[start_data + 3], 16))[2:].zfill(8)
            fiv_byte = bin(int(data[start_data + 4], 16))[2:].zfill(8)
            six_byte = bin(int(data[start_data + 5], 16))[2:].zfill(8)
            sev_byte = bin(int(data[start_data + 6], 16))[2:].zfill(8)
            eig_byte = bin(int(data[start_data + 7], 16))[2:].zfill(8)
        
            bit_data = str(one_byte) + str(two_byte) + str(thr_byte) + str(fou_byte) + str(fiv_byte) + str(six_byte) + str(sev_byte) + str(eig_byte)
            print (bit_data)

            autoOn = int(bit_data[autoOn_sb : autoOn_sb + sl],2)
            Acc_On = int(bit_data[Acc_On_sb : Acc_On_sb + sl],2)
            break_On = int(bit_data[break_On_sb : break_On_sb + sl],2)
        
            PRND = int(bit_data[PRND_sb : PRND_sb + sl],2) 
            if PRND > 0b11111111111111 :
                PRND = -0b1000000000000000 - PRND
            #SAS_pos = int(bit_data[SAS_pos_sb : SAS_pos_sb + SAS_sl],2) 
            sas_pos = str(bit_data[SAS_pos_sb + 8 : SAS_pos_sb + 16]) + str(bit_data[SAS_pos_sb : SAS_pos_sb + 8]) 
            SAS_pos = int(sas_pos,2)
            acc_pos = int(bit_data[acc_pos_sb : acc_pos_sb + sl],2) 
            break_pos = int(bit_data[break_pos_sb : break_pos_sb + sl],2) 
            print 'autoOn' , str(autoOn) , 'Acc_On' , str(Acc_On) , 'break_On' , str(break_On) , 'PRND' , str(PRND), 'SAS_pos', str(SAS_pos), 'acc_pos' , str(acc_pos), 'break_pos', str(break_pos)
        

            f = open(log_path, "a+")
            log_data_str = str(datetime) + "\t" + str(autoOn) + "\t" + str(Acc_On) + "\t" + str(break_On) + "\t" + str(PRND) + "\t" + str(SAS_pos) + "\t" + str(acc_pos) + "\t" + str(break_pos)
            f.write(str(log_data_str) + "\n")
            f.close()

        if data[can_addr] == '0201' :
            one_byte = bin(int(data[start_data], 16))[2:].zfill(8)
            two_byte = bin(int(data[start_data + 1], 16))[2:].zfill(8)
            thr_byte = bin(int(data[start_data + 2], 16))[2:].zfill(8)
            fou_byte = bin(int(data[start_data + 3], 16))[2:].zfill(8)
            fiv_byte = bin(int(data[start_data + 4], 16))[2:].zfill(8)
            six_byte = bin(int(data[start_data + 5], 16))[2:].zfill(8)
            sev_byte = bin(int(data[start_data + 6], 16))[2:].zfill(8)
            eig_byte = bin(int(data[start_data + 7], 16))[2:].zfill(8)
        
            bit_data = str(one_byte) + str(two_byte) + str(thr_byte) + str(fou_byte) + str(fiv_byte) + str(six_byte) + str(sev_byte) + str(eig_byte)
            print (bit_data)

            act_kph = int(bit_data[act_kph_sb :act_kph_sb + sl],2)
            set_kph = int(bit_data[set_kph_sb : set_kph_sb + sl],2)
            state = int(bit_data[state_sb : state_sb + sl],2) 
            radar = int(bit_data[radar_sb : radar_sb +sl],2)
            camera = int(bit_data[camera_sb : camera_sb + sl],2)
            ACU = int(bit_data[ACU_sb : ACU_sb + sl],2)
            lon_con = int(bit_data[lon_con_sb : lon_con_sb + sl],2)
            lat_con = int(bit_data[lat_con_sb : lat_con_sb + sl],2)
            print 'act_kph' , str(act_kph) , 'set_kph' , str(set_kph) , 'state' , str(state) , 'radar' , str(radar), 'camera', str(camera), 'ACU' , str(ACU), 'lon_con', str(lon_con), 'lat_con', str(lat_con)


            if radar == 0 :
                canvas.create_oval(5, 100, 55, 150, fill = 'gray') #Radar Ready
            else :
                canvas.create_oval(5, 100, 55, 150, fill = 'green') #Radar Ready
            if camera == 0 :
                canvas.create_oval(5, 150, 55, 200, fill = 'gray') #Radar Ready
            else :
                canvas.create_oval(5, 150, 55, 200, fill = 'green') #Radar Ready
            if ACU == 0 :
                canvas.create_oval(5, 200, 55, 250, fill = 'gray') #Radar Ready
            else :
                canvas.create_oval(5, 200, 55, 250, fill = 'green') #Radar Ready
            if lon_con == 0 :
                canvas.create_oval(5, 250, 55, 300, fill = 'gray') #Radar Ready
            else :
                canvas.create_oval(5, 250, 55, 300, fill = 'green') #Radar Ready
            if lat_con == 0 :
                canvas.create_oval(5, 300, 55, 350, fill = 'gray') #Radar Ready
            else :
                canvas.create_oval(5, 300, 55, 350, fill = 'green') #Radar Ready
            if state == 0 :
                canvas.create_oval(200, 150, 300, 250, fill = 'gray') #Lat Ctrl
            elif state == 1 :
                canvas.create_oval(200, 150, 300, 250, fill = 'green') #Radar Ready
            elif state == 2 :
                canvas.create_oval(200, 150, 300, 250, fill = 'yellow') #Radar Ready
            elif state == 3 :
                canvas.create_oval(200, 150, 300, 250, fill = 'red') #Radar Ready
            
            l_vsd = Tkinter.Label(root, text =  str(act_kph).zfill(3), font=("",40))
            l_ssd = Tkinter.Label(root, text =  str(set_kph).zfill(3), font=("",40))
            
            #l_vsd = Tkinter.Label(root, text =  str(act_kph), font=("",40))
            #l_ssd = Tkinter.Label(root, text =  str(set_kph), font=("",40))
            
            l_vsd.place(x = 160, y = 310)
            l_ssd.place(x = 270, y = 310)
            root.update()
            if state == 0:
                if prv_state == 1 or prv_state == 2 or prv_state == 3:
                    proc = subprocess.Popen("sudo omxplayer /home/pi/cantest/disengaged.wav", stdout = subprocess.PIPE, shell = True)
                prv_state = 0
            
            if state == 1:
                if prv_state == 0:
                    proc = subprocess.Popen("sudo omxplayer /home/pi/cantest/Init.wav", stdout = subprocess.PIPE, shell = True)
                prv_state = 1
            if state == 2 :
#if prv_state != 2 :
#proc = subprocess.Popen("sudo python /home/pi/cantest/grab.py", stdout = subprocess.PIPE, shell = True)
#proc = subprocess.Popen("sudo omxplayer /home/pi/cantest/grabSteer.wav", stdout = subprocess.PIPE, shell = True)
                os.system("omxplayer grabSteer.wav")
                prv_state = 2
            if state == 3 :
#if prv_state != 3 :
                os.system("omxplayer grabSteer.wav")
                    #proc = subprocess.Popen("sudo python /home/pi/cantest/grab.py", stdout = subprocess.PIPE, shell = True)
#               proc = subprocess.Popen("sudo omxplayer /home/pi/cantest/grabSteer.wav", stdout = subprocess.PIPE, shell = True)
                prv_state = 3

            bus.flush_tx_buffer()
            bus.shutdown()
    except KeyboardInterrupt :
        break
    except : 
        pass


