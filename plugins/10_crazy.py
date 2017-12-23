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
        self.Button11 = Box1.addWidget(gui.Button("Crazy11"))
        self.ClothModifier = Box1.addWidget(gui.Button("ClothModifier"))
        self.SetWeight = Box1.addWidget(gui.Button("SetWeight"))

        Box2 = self.addLeftWidget(gui.GroupBox('Crazy2'))
        self.SetView = Box2.addWidget(gui.Button("SetView"))
        self.ShowInfo = Box2.addWidget(gui.Button("ShowInfo"))

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



        @self.ClothModifier.mhEvent
        def onClicked(event):
            print "-----crazy-ClothModifier-----------"
            mhmain_MHApplication =G.app
            human = mhmain_MHApplication.selectedHuman
            cloth_modifier = mhmain_MHApplication.modules['3_libraries_clothes_chooser']

            mhclofile = "data/clothes/male_casualsuit02/male_casualsuit02.mhpxy"
            pxy = proxy.loadProxy(human, mhclofile)

            j = 0
            for obj in sorted(G.world, key=(lambda obj: obj.priority)):
                print "---------crazy-drawMeshes-----[", j, "]-----module3d_obj type = ", type(obj)

                print "module3d_obj.fvert = ", obj.fvert.shape
                print "module3d_obj.fnorm = ", obj.fnorm.shape
                print "module3d_obj.fuvs = ", obj.fuvs.shape
                print "module3d_obj.group = ", obj.group.shape
                j += 1

        @self.SetWeight.mhEvent
        def onClicked(event):

            mhmain_MHApplication = G.app
            human = mhmain_MHApplication.selectedHuman

            # print "crazylog ----------------human = ",dir(human)

            # object3d = human.mesh
            #
            # print "crazylog ----------------object3d = ",object3d

            human.setWeight(0.5)

            print "crazylog ----------------  human.getWeight() = ",human.getWeight()
            # pos = [10,10,10]
            # human.setPosition(pos)


        @self.SetView.mhEvent
        def onClicked(event):
            print "-----SetView----------"
            mhmain_MHApplication =G.app
            mhmain_MHApplication.axisView([0.0, 90.0, 0.0])
        @self.ShowInfo.mhEvent
        def onClicked(event):
            print "-----crazy-button-22-----------"

            mhmain_MHApplication = G.app
            human = mhmain_MHApplication.selectedHuman
            obj = human.mesh
            print "human.mesh = ",obj
            print "human.mesh.object3d = ", obj.object3d
            k=0
            for obj in sorted(G.world, key=(lambda obj: obj.priority)):
                k+=1
                obj = obj.parent
                print "obj[",k,"] = ",obj, "name =",obj.name

                if "base" in obj.name or "suit" in obj.name:

                    print "obj.coord[:,0].max(0) = ", obj.coord[:, 0].max()

                    print "obj.coord.shape = ", obj.coord.shape
                    print "obj.vnorm.shape = ", obj.vnorm.shape
                    print "obj.vtang.shape = ", obj.vtang.shape
                    print "obj.color.shape = ", obj.color.shape
                    print "obj.vface.shape = ", obj.vface.shape
                    print "obj.nfaces.shape = ", obj.nfaces.shape


                    print "obj.texco.shape = ", obj.texco.shape
                    print "obj.utexc.shape = ", obj.utexc


                    print "obj.fvert.shape = ", obj.fvert.shape
                    print "obj.fnorm.shape = ", obj.fnorm.shape
                    print "obj.fuvs.shape = ", obj.fuvs.shape
                    print "obj.group.shape = ", obj.group.shape
                    print "obj.face_mask.shape = ", obj.face_mask.shape


                    print "obj.group = ", obj.group

                    group_0 = obj.group[obj.group==0]
                    print "group_0.shape = ", group_0.shape

                    if hasattr(obj,"face_mask"):
                        false_mask_false = obj.face_mask[obj.face_mask == False]
                        if hasattr(false_mask_false, "shape"):
                            print "false_mask_false = ", false_mask_false.shape

                        false_mask_true = obj.face_mask[obj.face_mask == True]
                        if hasattr(false_mask_true, "shape"):
                            print "false_mask_true = ", false_mask_true.shape

                        if hasattr(obj,"group"):
                            indexs= np.where(obj.face_mask == True)
                            print "indexs =",indexs[0]
                            True_Group = obj.group[indexs[0]]
                            Group_id = np.unique(True_Group)
                            print "true group id = ", True_Group

            # obj.face_mask = True


    def onShow(self, event):
        gui3d.TaskView.onShow(self, event)
        self.Button11.setFocus()

def load(app):
    category = app.getCategory('Crazy')
    taskview = category.addTask(CrazyTaskView(category))

def unload(app):
    pass


