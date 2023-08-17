import hid, time, threading, cv2, os
from PyCameraList.camera_device import list_video_devices
from concurrent.futures import ThreadPoolExecutor
pool = ThreadPoolExecutor()
cam_id = 1
res = (640, 480)
fourcc = 'MJPG'
fps = 30
save_fourcc = []
frames = []
start_time, end_time = 0, 0
alive = True
dir_path = ''

def connect_cam():
    global frames, cap
    frames = []
    cap = None
    while alive:
        try:
            res_, fourcc_, fps_, cam_id_ = res, fourcc, fps, cam_id
            cap = cv2.VideoCapture(700+cam_id_)
            cap.set(5, fps)
            cap.set(3, res[0])
            cap.set(4, res[1])
            cap.set(6, cv2.VideoWriter.fourcc(*fourcc))
            w, h = cap.get(3), cap.get(4)
            if h == 480:
                sel1.select()
            elif h == 720:
                sel2.select()
            elif h == 1080:
                sel3.select()
            fcc = cap.get(6)
            if fcc == cv2.VideoWriter.fourcc(*'YUY2'):
                sel5.select()
            elif fcc == cv2.VideoWriter.fourcc(*'MJPG'):
                sel4.select()
            r = ((640*480)/(w*h))**0.5
            while (res_, fourcc_, fps_, cam_id_) == (res, fourcc, fps, cam_id) and alive:
                _, frame = cap.read()
                #print(cap.get(6)==cv2.VideoWriter.fourcc(*'YUY2'), time.time())
                #print(frame-cv2.cvtColor(cv2.cvtColor(frame, cv2.COLOR_BGR2YUV_I420), cv2.COLOR_YUV2BGR_I420))
                frames.append((frame, time.time()))
                if recording and start_time:
                    while len(frames) > 100:
                        (f, t_) = frames.pop(0)
                        if dir_path and recording and time.time()<end_time:
                            with open(f'{dir_path}/missed_frames.csv', 'a') as csv:
                                csv.write(f'{t_}\n')
                else:
                    while len(frames) > 5:
                        frames.pop(0)
                f_ = cv2.resize(frame, (round(w*r), round(h*r)))
                if not start_time or not recording:
                    cv2.imshow('cap', f_)
                else:
                    t = time.time()-start_time
                    if int(t)%2:
                        cv2.putText(f_, f'{int(t)//60}:', (30, 30), cv2.FONT_HERSHEY_COMPLEX, 1.0, (100, 100, 200), 2)
                    else:
                        cv2.putText(f_, f'{int(t)//60}', (30, 30), cv2.FONT_HERSHEY_COMPLEX, 1.0, (100, 100, 200), 2)
                    cv2.putText(f_, f'{t%60:.1f}', (60, 30), cv2.FONT_HERSHEY_COMPLEX, 1.0, (100, 100, 200), 2)
                    cv2.imshow('cap', f_)
                cv2.waitKey(1)
        except Exception as e:
            print(e)
            frames = []
        finally:
            cap = None
            time.sleep(0.1)


def connect_cms50e():
    global bvp, hr, spo2
    bvp = []
    hr = []
    spo2 = []
    while alive:
        try:
            vid, pid = 0, 0
            for i in hid.enumerate():
            #print(i)
                if i['product_string'] == 'Pulse Oximeter':
                    vid, pid = i['vendor_id'], i['product_id']
                    break
            h = hid.device()
            h.open(vid, pid)
            while (0, 0) != (vid, pid) and alive:
                recv = h.read(30)
                msgs = []
                t = time.time()
                for i in recv:
                    if i == 235:
                        msgs.append([])
                        continue
                    msgs[-1].append(i)
                for i in msgs:
                    if i[:1] == [0]:
                        _1 = (i[2], t)
                        if not bvp or t>bvp[-1][-1]:
                            bvp.append(_1)
                        if bvp and t==bvp[-1][-1]:
                            bvp[-1] = _1
                    if i[:2] == [1, 5]:
                        _2, _3 = (i[2], t), (i[3], t)
                        if not hr or t>hr[-1][-1]:
                            hr.append(_2)
                        if not spo2 or t>spo2[-1][-1]:
                            spo2.append(_3)
                if len(bvp)>100:
                    bvp.pop(0)
                if len(hr)>100:
                    hr.pop(0)
                if len(spo2)>100:
                    spo2.pop(0)
        except Exception as e:
            print(e)
        finally:
            time.sleep(0.1)
t1 = threading.Thread(target=connect_cms50e, daemon=True)
t2 = threading.Thread(target=connect_cam, daemon=True)
t1.start()
t2.start()

import tkinter as tk
from tkinter import ttk
window = tk.Tk()
window.title('PHYS-recoder')
window.geometry('200x400+300+300')
window.resizable(False, False)
value_c = tk.StringVar()
c_list = ttk.Combobox(window, textvariable=value_c)
c_list['values'] = [i[1] for i in list_video_devices()]
c_list.current(0)
c_list.configure(state='readonly')
c_list.place(x=5, y=30)
lb1 = tk.Label(window, text='BVP:', font=('Times',10))
lb1.place(x=0, y=0)
lb2 = tk.Label(window, text='×', font=('Times',10), fg='red')
lb2.place(x=30, y=0)
lb3 = tk.Label(window, text='CAM:', font=('Times',10))
lb3.place(x=60, y=0)
lb4 = tk.Label(window, text='×', font=('Times',10), fg='red')
lb4.place(x=97, y=0)


diff = 25
lb5 = tk.Label(window, text='name', font=('Times',15))
lb5.place(x=10, y=30+diff)

text1 = tk.Entry(window)
text1.insert(tk.INSERT, 'p001')
text1.place(x=5, y=60+diff)

lb6 = tk.Label(window, text='video', font=('Times',15))
lb6.place(x=10, y=80+diff)

text2 = tk.Entry(window)
text2.insert(tk.INSERT, 'v01')
text2.place(x=5, y=110+diff)

lb7 = tk.Label(window, text='duration', font=('Times',15))
lb7.place(x=10, y=130+diff)

text3 = tk.Entry(window)
text3.place(x=5, y=160+diff)
text3.insert(tk.INSERT, '0')

recording = False
def b_record():
    global recording
    if not (frames and time.time()-frames[-1][-1]<0.2):
        recording = False
        b1.config(text='start')
        return
    recording = not recording
    b1.config(text='start' if not recording else 'stop')
    if recording:
        try:
            t3.join()
        except Exception:
            pass
        t3 = threading.Thread(target=record, daemon=True)
        t3.start()

b1 = tk.Button(window, text='start', command=b_record, width=15, height=1)
b1.place(x=40, y=335+diff)

def write(x):
    cv2.imwrite(x[1], x[0], [cv2.IMWRITE_PNG_COMPRESSION, 1])

def record():
    global bvp, hr, spo2, frames, recording, start_time,end_time, f_n, dir_path
    f_n, dir_path = 0, ''
    start_time = 0
    bvp, hr, spo2, frames = bvp[-1:], hr[-1:], spo2[-1:], frames[-1:]
    if not os.path.exists(text1.get()):
        os.mkdir(text1.get())
    dir_path_ = f'{text1.get()}/{text2.get()}'
    if not os.path.exists(dir_path_):
        os.mkdir(dir_path_)
    dir_path = dir_path_
    with open(f'{dir_path}/missed_frames.csv', 'w') as csv:
        csv.write('timestamp\n')
    with open(f'{dir_path}/info.txt', 'w') as txt:
        txt.write(f'cam model: {list_video_devices()[cam_id][1]}\n')
        fcc = cap.get(6)
        if fcc == cv2.VideoWriter.fourcc(*'YUY2'):
            txt.write('cam codec: YUY2\n')
        elif fcc == cv2.VideoWriter.fourcc(*'MJPG'):
            txt.write('cam codec: MJPG\n')
        else:
            txt.write('cam codec: UNKNOW\n')
        txt.write(f'size: {int(cap.get(3))}x{int(cap.get(4))}\n')
        date = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
        txt.write(f'date: {date}')
    dur = float(text3.get())
    try:
    #video_outs = [cv2.VideoWriter(f'{dir_path}/video.avi' if i[0] !='a' else f'{dir_path}/video.mp4', cv2.VideoWriter.fourcc(*i), fps, res) for i in save_fourcc]
        video_outs = []
        writers = []
        tasks = []
        png = False
        for i in save_fourcc:
            if i=='avc1':
                p = f'{dir_path}/video_ZIP_H264.avi'
            if i=='I420':
                p = f'{dir_path}/video_RAW_YUV420.avi'
            if i=='RGBA':
                p = f'{dir_path}/video_RAW_RGBA.avi'
            if i=='MJPG':
                p = f'{dir_path}/video_ZIP_MJPG.avi'
            if i=='FFV1':
                p = f'{dir_path}/video_ZIP_RAW_BGRA.avi'
            if i=='PNGS':
                png = f'{dir_path}/pictures_ZIP_RAW_RGB/'
                if not os.path.exists(png):
                    os.mkdir(png)
                def png_write(p, n):
                    f = []
                    for i in p:
                        f.append((i[0], f'{png}{n:08}.png'))
                        n += 1
                    list(pool.map(write, f))
                continue
            writer = cv2.VideoWriter(p, fourcc=cv2.VideoWriter.fourcc(*i), fps=fps, frameSize=res)
            def f(x, writer=writer):
                global recording
                try:
                    for i in x:
                        writer.write(i)
                except Exception:
                    recording = False
            video_outs.append(f)
            writers.append(writer)
        if not save_fourcc:
            return
        with open(f'{dir_path}/BVP.csv', 'w') as f_bvp, open(f'{dir_path}/HR.csv', 'w') as f_hr, open(f'{dir_path}/SpO2.csv', 'w') as f_spo2,  open(f'{dir_path}/frames_timestamp.csv', 'w') as f_frames:
            f_bvp.write('timestamp,bvp\n')
            f_hr.write('timestamp,hr\n')
            f_spo2.write('timestamp,spo2\n')
            f_frames.write('frame,timestamp\n')
            start_time = time.time()
            end_time = float(dur)+start_time if int(dur) else 10**15
            while (frames[0][1]<end_time or not dur) and alive:
                t = time.time()
                if frames[-1][-1] >= end_time:
                    f = lambda x:x[-1]<end_time
                    bvp_, hr_, spo2_, frames_ = list(filter(f, bvp[:-1])), list(filter(f, hr[:-1])), list(filter(f, spo2[:-1])), list(filter(f, frames[:-1]))
                    recording = False
                else:
                    bvp_, hr_, spo2_, frames_ = bvp[:-1], hr[:-1], spo2[:-1], frames[:-1]
                    bvp, hr, spo2, frames = bvp[len(bvp_):], hr[len(hr_):], spo2[len(spo2_):], frames[len(frames_):]
                for b,ts in bvp_:
                    f_bvp.write(f'{ts},{b}\n')
                for h,ts in hr_:
                    f_hr.write(f'{ts},{h}\n')
                for s,ts in spo2_:
                    f_spo2.write(f'{ts},{s}\n')
                f_ = [i[0] for i in frames_]
                for i in video_outs:
                    tasks.append(pool.submit(i, f_))
                if png:
                    png_write(frames_, f_n)
                for _, ts in frames_:
                    f_frames.write(f'{f_n},{ts}\n')
                    f_n += 1
                for i in tasks:
                    i.result()
                tasks.clear()
                if not recording:
                    break
        time.sleep(max(t+0.1-time.time(), 0))
        recording = False
        for i in writers:
            i.release()
    except Exception as e:
        print(e)
    finally:
        dir_path = ''
        recording = False
t3 = threading.Thread(target=record, daemon=True)

lb8 = tk.Label(window, text='REC:', font=('Times',10))
lb8.place(x=123, y=0)
lb9 = tk.Label(window, text='×', font=('Times',10), fg='red')
lb9.place(x=155, y=0)

lb10 = tk.Label(window, text='size', font=('Times',15))
lb10.place(x=0, y=180+diff)

v1 = tk.StringVar()
sel1 = tk.Radiobutton(window, text='480p', variable=v1, value='640x480')
sel1.place(x=5, y=200+diff)
sel2 = tk.Radiobutton(window, text='720p', variable=v1, value='1280x720')
sel2.place(x=65, y=200+diff)
sel3 = tk.Radiobutton(window, text='1080p', variable=v1, value='1920x1080')
sel3.place(x=125, y=200+diff)
sel1.select()

lb11 = tk.Label(window, text='camera codec', font=('Times',15))
lb11.place(x=0, y=220+diff)
v2 = tk.StringVar()
sel4 = tk.Radiobutton(window, text='MJPG', variable=v2, value='MJPG')
sel4.place(x=5, y=240+diff)
sel5 = tk.Radiobutton(window, text='YUY2', variable=v2, value='YUY2')
sel5.place(x=65, y=240+diff)
sel5.select()

lb12 = tk.Label(window, text='file codec', font=('Times',15))
lb12.place(x=0, y=260+diff)
ck1_v = tk.StringVar()
ck2_v = tk.StringVar()
ck3_v = tk.StringVar()
ck4_v = tk.StringVar()
ck5_v = tk.StringVar()
ck6_v = tk.StringVar()
ck1 = tk.Checkbutton(window, text='H264', onvalue='avc1', offvalue='', variable=ck1_v)
ck2 = tk.Checkbutton(window, text='I420', onvalue='I420', offvalue='', variable=ck2_v)
ck3 = tk.Checkbutton(window, text='RGBA', onvalue='RGBA', offvalue='', variable=ck3_v)
ck4 = tk.Checkbutton(window, text='MJPG', onvalue='MJPG', offvalue='', variable=ck4_v)
ck5 = tk.Checkbutton(window, text='PNGS', onvalue='PNGS', offvalue='', variable=ck5_v)
ck6 = tk.Checkbutton(window, text='FFV1', onvalue='FFV1', offvalue='', variable=ck6_v)
ck1.place(x=5, y=280+diff)
ck2.place(x=65, y=280+diff)
ck3.place(x=125, y=280+diff)
ck4.place(x=5, y=300+diff)
ck5.place(x=65, y=300+diff)
ck6.place(x=125, y=300+diff)
ck6.select()

def f_lb():
    global res, fourcc, fps, save_fourcc, cam_id
    if bvp and time.time()-bvp[-1][-1]<0.2:
        lb2.config(text='√', font=('Times',10), fg='green')
    else:
        lb2.config(text='×', font=('Times',10), fg='red')
    if frames and time.time()-frames[-1][-1]<0.2:
        lb4.config(text='√', font=('Times',10), fg='green')
    else:
        lb4.config(text='×', font=('Times',10), fg='red')
    if recording:
        lb9.config(text='√', font=('Times',10), fg='green')
    else:
        lb9.config(text='×', font=('Times',10), fg='red')
    video_devices = [i[1] for i in list_video_devices()]
    c_list['values'] = video_devices
    if video_devices:
        cam_id = video_devices.index(c_list.get())
    b1.config(text='start' if not recording else 'stop')
    res = [int(i) for i in v1.get().split('x')]
    fourcc = v2.get()
    if fourcc == 'MJPG':
        fps = 30
    elif fourcc == 'YUY2':
        if res == [1920, 1080]:
            fps = 5
        if res == [1280, 720]:
            fps = 10
        if res == [640, 480]:
            fps = 30
    save_fourcc = [i for i in (ck1_v.get(), ck2_v.get(), ck3_v.get(), ck4_v.get(), ck5_v.get(), ck6_v.get()) if i]
    window.after(100, f_lb)
f_lb()
if __name__ == '__main__':
    window.mainloop()
    alive = False
    try:
        t1.join()
        t2.join()
        t3.join()
    except Exception:
        pass

    try:
        pool.shutdown()
    except Exception:
        pass