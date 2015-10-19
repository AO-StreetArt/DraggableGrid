# -*- coding: utf-8 -*-
"""
Created on Mon Oct 19 01:11:35 2015

@author: alex
"""
from kivy.app import App
from Magnet import Magnet
from kivy.properties import ObjectProperty, BooleanProperty, ListProperty, NumericProperty
from kivy.uix.image import Image
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock
from kivy.uix.label import Label
from kivy.lang import Builder

Builder.load_file('draggableimages.kv')

class DraggingGrid(GridLayout):
    cells=ListProperty([])
    
    def __init__(self, **kwargs):

        super(DraggingGrid, self).__init__(**kwargs)
        self.cols=3
        for i in range(0, 9):
            cell=BoxLayout()
            self.cells.append(cell)
            self.add_widget(cell)

#This class defines a draggable image
class DraggableImage(Magnet):
    img = ObjectProperty(None, allownone=True)
    app = ObjectProperty(None)
    grid = ObjectProperty(None)
    cell = ObjectProperty(None)
    start_cell = NumericProperty(0)

    def on_img(self, *args):
        self.clear_widgets()
        if self.img:
            Clock.schedule_once(lambda *x: self.add_widget(self.img), 0)

    def on_touch_down(self, touch, *args):
        if self.collide_point(*touch.pos):
            if touch.is_double_tap:
                pass
            else:
                touch.grab(self)
                self.remove_widget(self.img)
                self.app.root.add_widget(self.img)
                self.center = touch.pos
                self.img.center = touch.pos
            return True

        return super(DraggableImage, self).on_touch_down(touch, *args)

    def on_touch_move(self, touch, *args):

        if touch.grab_current == self:
            self.img.center = touch.pos
        return super(DraggableImage, self).on_touch_move(touch, *args)

    def on_touch_up(self, touch, *args):
        if touch.grab_current == self:
            if self.grid.collide_point(*touch.pos):
                for cel in self.grid.cells:
                    if cel.collide_point(*touch.pos):
                        self.cell.remove_widget(self)
                        self.app.root.remove_widget(self.img)
                        self.cell=cel
                        self.cell.add_widget(self)
                        self.add_widget(self.img)
                        touch.ungrab(self)
                        return True
                self.app.root.remove_widget(self.img)
                self.cell=1
                self.add_widget(self.img)
                touch.ungrab(self)
                return True
        return super(DraggableImage, self).on_touch_up(touch, *args)
        
class DraggableImageExampleWidget(GridLayout):
    drag_grid=ObjectProperty(None)
        
class DraggableImageExampleApp(App):
    def build(self):
        root = DraggableImageExampleWidget()
        image = Image(source='drag_node_small.png')
        drag = DraggableImage(img=image, app=self, grid=root.drag_grid, cell=root.drag_grid.cells[0])
        root.drag_grid.cells[0].add_widget(drag)
        return root
  
if __name__ == '__main__':
    DraggableImageExampleApp().run()