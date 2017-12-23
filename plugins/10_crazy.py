#!/usr/bin/python2.7
# -*- coding: utf-8 -*-
import numpy as np
import gui3d
import mh
import proxy
import gui
import module3d
from gui import QtGui
from core import G
class CrazyTaskView(gui3d.TaskView):

    def __init__(self, category):
        gui3d.TaskView.__init__(self, category, 'Crazy')

        Box1 = self.addLeftWidget(gui.GroupBox('Crazy1'))
        self.SetWeight = Box1.addWidget(gui.Button("SetWeight"))

        Box2 = self.addLeftWidget(gui.GroupBox('Crazy2'))
        self.ShowInfo = Box2.addWidget(gui.Button("ShowInfo"))

        def ReadLandmarksIndexs(files):
            file = open(files, 'r')
            lines = file.readlines()
            for i in range(0, len(lines), 1):
                lines[i] = int(lines[i].replace('\n', ''))
            indexs = np.array(lines)
            return indexs

        @self.SetWeight.mhEvent
        def onClicked(event):

            mhmain_MHApplication = G.app
            human = mhmain_MHApplication.selectedHuman
            human.setWeight(0.5)
            print " human.getWeight() = ",human.getWeight()

            for modifier_class in G.Mofiler:
                if 'head-fat' in str(modifier_class.modifier.name):
                    modifier_class.my_onChange(0.1,human)
                if 'head-age' in str(modifier_class.modifier.name):
                    modifier_class.my_onChange(0.1, human)






        @self.ShowInfo.mhEvent
        def onClicked(event):

            selected_landmarks_ids = ReadLandmarksIndexs("selected_landmarks_index.txt")
            selected_vertices_ids = ReadLandmarksIndexs("selected_vertices_index.txt")
            landmarks_ids = selected_vertices_ids[selected_landmarks_ids]

            for obj in sorted(G.world, key=(lambda obj: obj.priority)):
                obj = obj.parent
                if "base" in obj.name:
                    print "obj.coord[:,0].max(0) = ", obj.coord[:, 0].max()
                    print "obj.coord.shape = ", obj.coord.shape
                    print "landmarks_ids.shape",landmarks_ids.shape
                    landmakrs_3d = obj.coord[landmarks_ids, :]
                    print "landmakrs_3d = ", landmakrs_3d




    def onShow(self, event):
        gui3d.TaskView.onShow(self, event)

def load(app):
    category = app.getCategory('Crazy')
    taskview = category.addTask(CrazyTaskView(category))

def unload(app):
    pass


