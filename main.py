import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import messagebox, filedialog
from pytube import YouTube
from threading import Thread

def download_video():
    url = url_entry.get()
    if not url:
        messagebox.showerror("Erro", "Por favor, insira a URL do vídeo do YouTube.")
        return

    def start_download():
        try:
            yt = YouTube(url, on_progress_callback=progress_function)
            stream = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()
            save_path = filedialog.askdirectory()
            if save_path:
                progress_bar['value'] = 0
                stream.download(save_path)
                messagebox.showinfo("Sucesso", "Vídeo baixado com sucesso!")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao baixar o vídeo: {e}")

    Thread(target=start_download).start()

def progress_function(stream, chunk, bytes_remaining):
    total_size = stream.filesize
    bytes_downloaded = total_size - bytes_remaining
    percentage_of_completion = bytes_downloaded / total_size * 100
    progress_bar['value'] = percentage_of_completion
    root.update_idletasks()

# Criando a janela principal com ttkbootstrap
root = ttk.Window(themename="cosmo")
root.title("YouTube Video Downloader")
root.geometry("600x300")

# Criando widgets com ttkbootstrap
url_label = ttk.Label(root, text="URL do Vídeo:", bootstyle="primary")
url_label.pack(pady=10)

url_entry = ttk.Entry(root, width=50, bootstyle="info")
url_entry.pack(pady=5)

download_button = ttk.Button(root, text="Baixar Vídeo", command=download_video, bootstyle="success")
download_button.pack(pady=20)

# Barra de progresso
progress_bar = ttk.Progressbar(root, bootstyle="info-striped", length=400)
progress_bar.pack(pady=20)

# Iniciando o loop principal da interface gráfica
root.mainloop()
