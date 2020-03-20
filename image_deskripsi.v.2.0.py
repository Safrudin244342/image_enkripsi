from PIL import Image
from tkinter import Tk,Button,Label,Entry
from tkinter.ttk import Progressbar
from tkinter.filedialog import askopenfilename,asksaveasfilename
from hashlib import sha512
from tkinter.messagebox import showinfo,askquestion
from stegano import lsb
import threading
import os

class setting_gui_main():
    def __init__(self,root):
        self.root = root
        self.root.title("Deskripsi Image 2.0")
        self.root.resizable(False, False)
        self.root.geometry("400x250")
        self.root.protocol('WM_DELETE_WINDOW',self.quit)
        self.set_gui()
        self.deklarasi_variable()

    def deklarasi_variable(self):
        self.en_save_file = ""
        self.en_input_file = ""

    def set_gui(self):
        #membuat kolom input file
        Button(self.root,text="Search",command=self.input_img_file).place(x=10,y=10)
        self.en_input_text = Label(self.root,text="Cari gambar yang akan di deskripsi")
        self.en_input_text.place(x=90,y=15)
        # membuat kolom input file
        Button(self.root, text="Search",command=self.save_img_file).place(x=10, y=50)
        self.en_save_text = Label(self.root, text="Lokasi file akan disimpan")
        self.en_save_text.place(x=90, y=55)
        #membuat kolom password
        Label(self.root,text="Password : ").place(x=10, y=90)
        self.txt_password = Entry(self.root)
        self.txt_password.place(x=90, y=90)
        #membuat btn enkripsi
        Button(self.root,text="Deskripsi",command=self.deskripsi_img).place(x=150, y=120)
        #menampilkan proses enkripsi
        Label(self.root,text="Proses : ").place(x=10, y=170)
        self.proses_en = Progressbar(self.root,orient="horizontal",length=270,mode="determinate")
        self.proses_en.place(x=80 ,y=170)
        #menampilkan copyright
        Label(self.root,text="Create By : Ahmad").place(x=140,y=195)
        Label(self.root,text="Email : Ahmadaris355@gmail.com").place(x=80,y=220)

    def input_img_file(self):
        self.en_input_file = askopenfilename(filetypes=(("PNG","*.png"),))
        self.en_input_text['text'] = self.en_input_file

    def save_img_file(self):
        self.en_save_file = asksaveasfilename(filetypes=(("PNG","*.png"),))
        #cek apakah file save telah ber-ektensi
        cek = self.en_save_file.split(".")
        if cek[len(cek) - 1] != "png":
            self.en_save_file = self.en_save_file + ".png"
        self.en_save_text['text'] = self.en_save_file

    def deskripsi_img(self):
        #mulai mengenkripsi gambar

        #cek apakah semua kolom telah diisi
        if len(self.en_save_file) > 0 and len(self.en_input_file) > 0 and len(self.txt_password.get()) > 0:
            img = Image.open(self.en_input_file)
            password = self.txt_password.get()
            t = threading.Thread(target=self.deskirpsi_img_proses, args=(img, password))
            t.start()
        elif len(self.en_input_file) == 0:
            showinfo("Peringatan","Belum ada gambar yang dipilih")
        elif len(self.en_save_file) == 0:
            showinfo("Peringatan","Lokasi simpan file belum dipilih")
        elif os.path.isfile(self.en_save_file):
            showinfo("Peringatan","Gambar tidak bisa diakses")
        elif len(self.txt_password.get()) == 0:
            showinfo("Peringatan","Password belum diisi")

    #proses enkripsi gambar
    def deskirpsi_img_proses(self,img,password):
        # deklarasi semua variable
        data_pixel = []
        # membuat gambar deskripsi

        #membaca password yang tersimpan di gambar
        pass_img = lsb.reveal(self.en_input_file)
        pass_des = sha512()
        password = self.txt_password.get()
        pass_des.update(password.encode("utf-8"))
        pass_des = pass_des.hexdigest()

        #cek apakah password sama
        if pass_img == pass_des and img.mode == "RGBA":
            # melakukan perulangan untuk membaca setiap pixel
            width, height = img.size
            pass_ke = 0
            warna = 0
            ord_huruf = 0
            # melakukan perulangan sesuai lebar gambar
            for lebar in range(width - 1):
                isi = []
                isi_isi = []

                # mengambil setiap huruf dari password
                if pass_ke == len(password):
                    pass_ke = 0

                # menentukan warna dominan setiap baris
                nilai_warna = ""
                if warna == 0:
                    nilai_warna = "R"
                    warna += 1
                elif warna == 1:
                    nilai_warna = "G"
                    warna += 1
                elif warna == 2:
                    nilai_warna = "B"
                    warna = 0

                ord_huruf = ord(password[pass_ke])
                pass_ke += 1
                i = 0
                # melakukan perulangan sesuai tinggi gambar
                for tinggi in range(height - 1):
                    if i <= ord_huruf:

                        # mendapatkan setiap pixel dari gambar
                        x, y, z, a = img.getpixel((lebar, tinggi))

                        # enkripsi setiap pixel
                        hash = self.rand_deskripsi(x, y, z, a, nilai_warna)

                        # membuat gambar utuk setiap pixel yang telah di enkripsi
                        isi_pixel = Image.new("RGBA", (1, 1), hash)

                        # memasukkan pixel kedalam array
                        isi_isi.append(isi_pixel)

                        i += 1
                    elif i > ord_huruf:
                        # mendapatkan setiap pixel dari gambar
                        x, y, z, a = img.getpixel((lebar, tinggi))
                        # enskripsi setip pixel
                        hash = self.rand_deskripsi(x, y, z, a, nilai_warna)

                        # membuat gambar untuk setiap pixel
                        isi_pixel = Image.new("RGBA", (1, 1), hash)

                        # memasukkan pixel ke dalam array
                        isi_isi.append(isi_pixel)

                        i = 0

                        # membalik array agar gambar teracak
                        isi_isi.reverse()

                        # memasukkan array kedalam array baris
                        for pixel in isi_isi:
                            isi.append(pixel)

                        # mengosongkan array pixel
                        isi_isi = []

                # melakukan aksi untuk array yang belum di masukkan kedalam array baris
                isi_isi.reverse()
                for pixel in isi_isi:
                    isi.append(pixel)

                # menampilkan proses yang sedang berjalan
                self.update_proses_bar(lebar, width)

                # memasukkan array baris ke array gambar
                data_pixel.append(isi)

            # membuat gambar backgroud
            backgroud = Image.new("RGBA", (width - 1, height - 1), (255, 255, 255, 255))

            # membuat image baru
            for lebar in range(width - 1):
                for tinggi in range(height - 1):
                    backgroud.paste(data_pixel[lebar][tinggi], (lebar, tinggi))

            # menyimpan gambar hasil enkripsi
            backgroud.save(self.en_save_file)

            showinfo("Pemberitahuan", "Gambar telah di deskripsi, tersimpan di\n" + self.en_save_file)
            self.proses_en['value'] = 0

            self.proses_en['value'] = 0
            self.txt_password.delete(0, 'end')
            self.en_save_text['text'] = "Lokasi file enkripsi akan disimpan"
            self.en_input_text['text'] = "Cari gambar yang akan di enkripsi"
        elif pass_des != pass_img:
            showinfo("Warning","Password salah!")
        else:
            showinfo("Warning","Gambar input tidak bisa diolah!")

    def rand_deskripsi(self,x, y, z, a, nilai_warna):
        x_hasil = x
        y_hasil = y
        z_hasil = z
        if nilai_warna == "R":
            x_hasil = a
        elif nilai_warna == "G":
            y_hasil = a
        elif nilai_warna == "B":
            z_hasil = a
        hash = (x_hasil, y_hasil, z_hasil)
        return hash

    def update_proses_bar(self,proses,width):
        presentase = int((proses/width) * 100)
        self.proses_en['value'] = presentase

    def quit(self):
        self.berjalan = False
        cek = askquestion("pemberitahuan", "Apakah Kamu yakin akan keluar?")
        if cek == "yes":
            self.root.destroy()


root = Tk()
setting_gui_main(root)
root.mainloop()