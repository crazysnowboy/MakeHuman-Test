#!/usr/bin/python2.7
# -*- coding: utf-8 -*-

import gui3d
import mh
import proxy
import gui
from gui import QtGui
from core import G
class CrazyTaskView(gui3d.TaskView):

    def __init__(self, category):
        gui3d.TaskView.__init__(self, category, 'Crazy')

        Box1 = self.addLeftWidget(gui.GroupBox('Crazy1'))
        self.Button11 = Box1.addWidget(gui.Button("Crazy11"))
        self.ClothModifier = Box1.addWidget(gui.Button("ClothModifier"))
        self.SetWeight = Box1.addWidget(gui.Button("SetWeight"))

        Box2 = self.addLeftWidget(gui.GroupBox('Crazy2'))
        self.SetView = Box2.addWidget(gui.Button("SetView"))
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
            print "G.canvas  dir = ", dir(G.canvas)

            j = 0
            for module3d_obj in sorted(G.Crazy, key=(lambda module3d_obj: module3d_obj.priority)):
                print "---------crazy-drawMeshes-----[", j, "]-----module3d_obj type = ", type(module3d_obj)
                print "---------crazy-drawMeshes-----[", j, "]-----G.world type = ", type(G.Crazy[j])

                print "module3d_obj.fvert = ", module3d_obj.fvert.shape
                print "module3d_obj.fnorm = ", module3d_obj.fnorm.shape
                print "module3d_obj.fuvs = ", module3d_obj.fuvs.shape
                print "module3d_obj.group = ", module3d_obj.group.shape
                j += 1

        @self.ClothModifier.mhEvent
        def onClicked(event):
            print "-----crazy-ClothModifier-----------"
            mhmain_MHApplication =G.app
            human = mhmain_MHApplication.selectedHuman
            # cloth_modifier = mhmain_MHApplication.modules['3_libraries_clothes_chooser']

            cloth_modifier = G.ClothesTaskView[0]

            mhclofile = "data/clothes/male_casualsuit02/male_casualsuit02.mhpxy"
            pxy = proxy.loadProxy(human, mhclofile)

            human.addClothesProxy(pxy)


        @self.SetWeight.mhEvent
        def onClicked(event):

            mhmain_MHApplication = G.app
            human = mhmain_MHApplication.selectedHuman

            # print "crazylog ----------------human = ",dir(human)

            object3d = human.mesh

            print "crazylog ----------------object3d = ",object3d

            # human.setWeight(200)
            # pos = [10,10,10]
            # human.setPosition(pos)


        @self.SetView.mhEvent
        def onClicked(event):
            print "-----SetView----------"
            mhmain_MHApplication =G.app
            mhmain_MHApplication.axisView([0.0, 90.0, 0.0])
        @self.Button22.mhEvent
        def onClicked(event):
            print "-----crazy-button-22-----------"




    def onShow(self, event):
        gui3d.TaskView.onShow(self, event)
        self.Button11.setFocus()

def load(app):
    category = app.getCategory('Crazy')
    taskview = category.addTask(CrazyTaskView(category))

def unload(app):
    pass


