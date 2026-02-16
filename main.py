from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
import os

class CleanerApp(App):
    def build(self):
        self.junk_files = []
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        layout.add_widget(Label(
            text='🧹 TELEFON TEMİZLEYİCİ',
            font_size='24sp',
            size_hint_y=None,
            height=50
        ))
        
        self.info_label = Label(
            text='Taramak için butona basın',
            font_size='16sp',
            size_hint_y=None,
            height=40
        )
        layout.add_widget(self.info_label)
        
        btn_scan = Button(text='🔍 TARA', font_size='20sp', size_hint_y=None, height=60)
        btn_scan.bind(on_press=self.scan_files)
        
        btn_clean = Button(text='🗑️ TEMİZLE', font_size='20sp', size_hint_y=None, height=60)
        btn_clean.bind(on_press=self.clean_files)
        
        layout.add_widget(btn_scan)
        layout.add_widget(btn_clean)
        
        scroll = ScrollView()
        self.result_grid = GridLayout(cols=1, spacing=5, size_hint_y=None)
        self.result_grid.bind(minimum_height=self.result_grid.setter('height'))
        scroll.add_widget(self.result_grid)
        layout.add_widget(scroll)
        
        return layout
    
    def scan_files(self, instance):
        self.result_grid.clear_widgets()
        self.junk_files = []
        paths = ['/sdcard/Download', '/sdcard/DCIM/.thumbnails']
        extensions = ['.tmp', '.cache', '.thumb']
        total_size = 0
        
        for path in paths:
            if os.path.exists(path):
                for root, dirs, files in os.walk(path):
                    for file in files:
                        if any(file.endswith(ext) for ext in extensions):
                            filepath = os.path.join(root, file)
                            try:
                                size = os.path.getsize(filepath)
                                self.junk_files.append(filepath)
                                total_size += size
                                lbl = Label(
                                    text=f'{file[:25]}... ({size//1024}KB)',
                                    size_hint_y=None,
                                    height=30,
                                    font_size='12sp'
                                )
                                self.result_grid.add_widget(lbl)
                            except:
                                pass
        
        self.info_label.text = f'{len(self.junk_files)} dosya ({total_size//1024//1024}MB)'
    
    def clean_files(self, instance):
        deleted = 0
        for filepath in self.junk_files:
            try:
                os.remove(filepath)
                deleted += 1
            except:
                pass
        self.info_label.text = f'{deleted} dosya silindi!'
        self.result_grid.clear_widgets()
        self.junk_files = []

if __name__ == '__main__':
    CleanerApp().run()
                              
