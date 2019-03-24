import can
from Tkinter import *
import Tkinter
import time
log_path = "/home/pi/can_log.txt"
can_addr = 3
start_data = 7
bus = can.interface.Bus(channel='can0', bustype='socketcan_native')


root = Tkinter.Tk()
canvas = Tkinter.Canvas(root, width = 500, height = 500)
canvas.pack()
canvas.create_oval(5, 100, 55, 150) #Radar Ready
canvas.create_oval(5, 150, 55, 200) #camera Ready
canvas.create_oval(5, 200, 55, 250) #ACU Ready
canvas.create_oval(5, 250, 55, 300) #Lon Ctrl
canvas.create_oval(5, 300, 55, 350) #Lat Ctrl
canvas.create_oval(200, 150, 300, 250) #Lat Ctrl

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

l_cam.place(x = 65, y = 115)
l_rad.place(x = 65, y = 165)
l_acu.place(x = 65, y = 215)
l_lon.place(x = 65, y = 265)
l_lat.place(x = 65, y = 315)
l_sta.place(x = 210, y = 120)
l_vsp.place(x = 170, y = 260)
l_ssp.place(x = 270, y = 260)
l_vsd.place(x = 180, y = 310)
l_ssd.place(x = 280, y = 310)

root.update()


while 1 :

    raw_data = bus.recv(1.0)

    data = str(raw_data).split()
#print(data)
    if data[can_addr] == '0200':
        now = time.localtime()
        datetime = str(now.tm_year) +"-"+ str(now.tm_mon) +"-"+ str(now.tm_mday) +"-"+ str(now.tm_hour) +"-"+ str(now.tm_min) +"-"+ str(now.tm_sec)
        f = open(log_path, "a+")
        log_data = data.append(datetime)
        f.write(str(data) + "\n")
        f.close()
        one_byte = bin(int(data[start_data], 16))[2:].zfill(8)
        two_byte = bin(int(data[start_data + 1], 16))[2:].zfill(8)
        thr_byte = bin(int(data[start_data + 2], 16))[2:].zfill(8)
        fou_byte = bin(int(data[start_data + 3], 16))[2:].zfill(8)
        fiv_byte = bin(int(data[start_data + 4], 16))[2:].zfill(8)
        six_byte = bin(int(data[start_data + 5], 16))[2:].zfill(8)
        sev_byte = bin(int(data[start_data + 6], 16))[2:].zfill(8)
        eig_byte = bin(int(data[start_data + 7], 16))[2:].zfill(8)
        
        bit_data = str(one_byte) + str(two_byte) + str(thr_byte) + str(fou_byte) + str(fiv_byte) + str(six_byte) + str(sev_byte) + str(eig_byte)
#print (bit_data)

        autoOn = int(bit_data[0],2)
        Acc_On = int(bit_data[1],2)
        break_On = int(bit_data[2],2)
        PRND = int(bit_data[3:3+4-1],2)
        SAS_pos = int(bit_data[8:8+16-1],2)
        acc_pos = int(bit_data[24:24+8-1],2)
        break_pos = int(bit_data[32:32+8-1],2)
        print 'autoOn' , str(autoOn) , 'Acc_On' , str(Acc_On) , 'break_On' , str(break_On) , 'PRND' , str(PRND), 'SAS_pos', str(SAS_pos), 'acc_pos' , str(acc_pos), 'break_pos', str(break_pos)
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
#print (bit_data)

        act_kph = int(bit_data[0:8-1],2)
        set_kph = int(bit_data[8:8+8-1],2)
        state = int(bit_data[16:16+8-1],2)
        radar = int(bit_data[24],2)
        camera = int(bit_data[25],2)
        ACU = int(bit_data[26],2)
        lon_con = int(bit_data[27],2)
        lat_con = int(bit_data[28],2)
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
            canvas.create_oval(100, 300, 150, 350, fill = 'green') #Radar Ready
        if state == 0 :
            canvas.create_oval(200, 150, 300, 250, fill = 'gray') #Lat Ctrl
        elif state == 1 :
            canvas.create_oval(200, 150, 300, 250, fill = 'green') #Radar Ready
        elif state == 2 :
            canvas.create_oval(200, 150, 300, 250, fill = 'yellow') #Radar Ready
        elif state == 3 :
            canvas.create_oval(200, 150, 300, 250, fill = 'red') #Radar Ready
        l_vsd = Tkinter.Label(root, text = str(act_kph), font=("",40))
        l_ssd = Tkinter.Label(root, text = str(set_kph), font=("",40))
        l_vsd.place(x = 180, y = 310)
        l_ssd.place(x = 280, y = 310)
        root.update()


