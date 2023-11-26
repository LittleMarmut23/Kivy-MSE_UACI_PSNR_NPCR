from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
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

        layout.add_widget(self.image1_path_input)
        layout.add_widget(self.image2_path_input)
        layout.add_widget(compare_btn)
        layout.add_widget(self.result_label)

        return layout

    def compare_images(self, instance):
        image1_path = self.image1_path_input.text
        image2_path = self.image2_path_input.text

        if not image1_path or not image2_path:
            return

        image1 = img_as_float(io.imread(image1_path))
        image2 = img_as_float(io.imread(image2_path))

        mse = np.mean((image1 - image2) ** 2)
        uaci = np.sum(np.abs(image1 - image2)) / np.sum(image1 + image2)
        psnr = -10 * np.log10(mse)
        npcr = np.sum(image1 != image2) / (image1.shape[0] * image1.shape[1])

        result_text = f"Hasil:\nMSE: {mse:.4f}\nUACI: {uaci:.4f}\nPSNR: {psnr:.4f} dB\nNPCR: {npcr:.4f}"
        self.result_label.text = result_text

if __name__ == '__main__':
    ImageComparisonApp().run()
