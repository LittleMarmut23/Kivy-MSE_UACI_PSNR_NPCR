from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.popup import Popup
from kivy.uix.gridlayout import GridLayout
from skimage import io, img_as_float
import numpy as np

class ImageComparisonApp(App):
    def build(self):
        layout = BoxLayout(orientation='vertical')

        self.image1_path_input = TextInput(hint_text="Input path image 1")
        self.image2_path_input = TextInput(hint_text="Input path image 2")

        compare_btn = Button(text='Cetak')
        compare_btn.bind(on_press=self.compare_images)

        self.result_label = Label(text="Hasil: ")

        # Widget BoxLayout untuk menampilkan gambar dalam satu baris
        image_row = BoxLayout(orientation='horizontal')

        # Widget Image untuk gambar 1
        self.image1 = Image()  # Atur ukuran gambar di sini
        image_row.add_widget(self.image1)

        # Widget Image untuk gambar 2
        self.image2 = Image()  # Atur ukuran gambar di sini
        image_row.add_widget(self.image2)

        layout.add_widget(self.image1_path_input)
        layout.add_widget(self.image2_path_input)
        layout.add_widget(compare_btn)
        layout.add_widget(self.result_label)
        layout.add_widget(image_row)  # Tambahkan widget BoxLayout dengan kedua gambar

        return layout

    def compare_images(self, instance):
        image1_path = self.image1_path_input.text
        image2_path = self.image2_path_input.text

        if not image1_path or not image2_path:
            return

        image1 = img_as_float(io.imread(image1_path))
        image2 = img_as_float(io.imread(image2_path))

        # Pemeriksaan jumlah piksel
        if image1.shape != image2.shape:
            # Buat pesan kesalahan yang mencakup jumlah piksel
            error_message = f'Error: Jumlah piksel gambar 1 = {image1.shape[1]}x{image1.shape[0]}, gambar 2 = {image2.shape[1]}x{image2.shape[0]} berbeda.'

            # Buat popup dengan pesan kesalahan
            error_popup = Popup(title='Error', content=GridLayout(rows=2), auto_dismiss=False, size_hint=(None, None), size=(600, 150))
            error_popup.content.add_widget(Label(text=error_message))

            # Tambahkan tombol "Kembali" ke dalam popup
            back_button = Button(text='Kembali')
            back_button.bind(on_press=error_popup.dismiss)
            error_popup.content.add_widget(back_button)

            # Tampilkan popup
            error_popup.open()
            return

        mse = np.mean((image1 - image2) ** 2)
        uaci = np.sum(np.abs(image1 - image2)) / np.sum(image1 + image2)
        psnr = -10 * np.log10(mse)
        npcr = np.sum(image1 != image2) / (image1.shape[0] * image1.shape[1])

        result_text = f"Hasil:\nMSE: {mse:.4f}\nUACI: {uaci:.4f}\nPSNR: {psnr:.4f} dB\nNPCR: {npcr:.4f}"
        self.result_label.text = result_text

        self.image1.source = image1_path  # Tampilkan gambar pertama
        self.image2.source = image2_path  # Tampilkan gambar kedua

if __name__ == '__main__':
    ImageComparisonApp().run()
