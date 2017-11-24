#!/usr/bin/python2.7
# -*- coding: utf-8 -*-

import gui3d
import mh
import gui
from gui import QtGui
from core import G
class CrazyTaskView(gui3d.TaskView):

    def __init__(self, category):
        gui3d.TaskView.__init__(self, category, 'Crazy')

        Box1 = self.addLeftWidget(gui.GroupBox('Crazy1'))
        self.Button11 = Box1.addWidget(gui.Button("Crazy11"))
        self.Button12 = Box1.addWidget(gui.Button("Crazy12"))
        self.Button13 = Box1.addWidget(gui.Button("Crazy13"))

        Box2 = self.addLeftWidget(gui.GroupBox('Crazy2'))
        self.Button21 = Box2.addWidget(gui.Button("Crazy21"))
        self.Button22 = Box2.addWidget(gui.Button("Crazy22"))

        @self.Button11.mhEvent
        def onClicked(event):
            print "-----crazy-button-11-----------"
            mhmain_MHApplication =G.app

            print "mhmain_MHApplication.selectedGroup  = ",mhmain_MHApplication.selectedGroup
            print "mhmain_MHApplication.selectedHuman  = ", mhmain_MHApplication.selectedHuman
            print "mhmain_MHApplication.modelCamera  = ", mhmain_MHApplication.modelCamera


            for i in range(0,len(G.cameras),1):
                proj, mv = G.cameras[i].getMatrices(1)

                print "proj[",i,"]  = ", proj
                print "mv[",i,"]  = ", mv

            print "G.canvas  = ", G.canvas

            j = 0
            for module3d_obj in sorted(G.Crazy, key=(lambda module3d_obj: module3d_obj.priority)):
                print "---------crazy-drawMeshes-----[", j, "]-----module3d_obj type = ", type(module3d_obj)
                print "---------crazy-drawMeshes-----[", j, "]-----G.world type = ", type(G.Crazy[j])

                print "module3d_obj.fvert = ", module3d_obj.fvert.shape
                print "module3d_obj.fnorm = ", module3d_obj.fnorm.shape
                print "module3d_obj.fuvs = ", module3d_obj.fuvs.shape
                print "module3d_obj.group = ", module3d_obj.group.shape
                j += 1

        @self.Button12.mhEvent
        def onClicked(event):
            print "-----crazy-button-12-----------"
            mhmain_MHApplication =G.app
            cloth_modifier = mhmain_MHApplication.modules['3_libraries_clothes_chooser']
            print "---crazylog--plugins-----",dir(cloth_modifier)

        @self.Button13.mhEvent
        def onClicked(event):

            mhmain_MHApplication = G.app
            human = mhmain_MHApplication.selectedHuman

            print "crazylog ----------------human = ",dir(human)

            human.setWeight(200)


        @self.Button21.mhEvent
        def onClicked(event):
            print "-----crazy-button-21-----------"
            mhmain_MHApplication =G.app
            mhmain_MHApplication.axisView([0.0, 90.0, 0.0])
        @self.Button22.mhEvent
        def onClicked(event):
            print "-----crazy-button-22-----------"
            mhmain_MHApplication =G.app
            mhmain_MHApplication.axisView([90.0, 0.0, 0.0])



    def onShow(self, event):
        gui3d.TaskView.onShow(self, event)
        self.Button11.setFocus()

def load(app):
    category = app.getCategory('Crazy')
    taskview = category.addTask(CrazyTaskView(category))

def unload(app):
    pass


