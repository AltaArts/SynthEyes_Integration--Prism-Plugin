# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'Synth_SceneExport.ui'
##
## Created by: Qt User Interface Compiler version 6.10.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from qtpy.QtCore import *  # type: ignore
from qtpy.QtGui import *  # type: ignore
from qtpy.QtWidgets import *  # type: ignore

class Ui_wg_Synth_SceneExport(object):
    def setupUi(self, wg_Synth_SceneExport):
        if not wg_Synth_SceneExport.objectName():
            wg_Synth_SceneExport.setObjectName(u"wg_Synth_SceneExport")
        wg_Synth_SceneExport.setEnabled(True)
        wg_Synth_SceneExport.resize(399, 910)
        self.verticalLayout = QVBoxLayout(wg_Synth_SceneExport)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.w_name = QWidget(wg_Synth_SceneExport)
        self.w_name.setObjectName(u"w_name")
        self.horizontalLayout_5 = QHBoxLayout(self.w_name)
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.horizontalLayout_5.setContentsMargins(9, 0, 18, 0)
        self.l_name = QLabel(self.w_name)
        self.l_name.setObjectName(u"l_name")

        self.horizontalLayout_5.addWidget(self.l_name)

        self.e_name = QLineEdit(self.w_name)
        self.e_name.setObjectName(u"e_name")
        self.e_name.setMinimumSize(QSize(0, 0))
        self.e_name.setMaximumSize(QSize(9999, 16777215))

        self.horizontalLayout_5.addWidget(self.e_name)

        self.l_class = QLabel(self.w_name)
        self.l_class.setObjectName(u"l_class")
        font = QFont()
        font.setBold(True)
        self.l_class.setFont(font)

        self.horizontalLayout_5.addWidget(self.l_class)


        self.verticalLayout.addWidget(self.w_name)

        self.gb_general = QGroupBox(wg_Synth_SceneExport)
        self.gb_general.setObjectName(u"gb_general")
        self.lo_general = QVBoxLayout(self.gb_general)
        self.lo_general.setObjectName(u"lo_general")
        self.w_comment = QWidget(self.gb_general)
        self.w_comment.setObjectName(u"w_comment")
        self.horizontalLayout_16 = QHBoxLayout(self.w_comment)
        self.horizontalLayout_16.setSpacing(0)
        self.horizontalLayout_16.setObjectName(u"horizontalLayout_16")
        self.horizontalLayout_16.setContentsMargins(9, 0, 9, 0)
        self.l_comment = QLabel(self.w_comment)
        self.l_comment.setObjectName(u"l_comment")
        self.l_comment.setMinimumSize(QSize(40, 0))
        self.l_comment.setMaximumSize(QSize(95, 16777215))

        self.horizontalLayout_16.addWidget(self.l_comment)

        self.horizontalSpacer_8 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_16.addItem(self.horizontalSpacer_8)

        self.e_comment = QLineEdit(self.w_comment)
        self.e_comment.setObjectName(u"e_comment")

        self.horizontalLayout_16.addWidget(self.e_comment)


        self.lo_general.addWidget(self.w_comment)

        self.w_context = QWidget(self.gb_general)
        self.w_context.setObjectName(u"w_context")
        self.horizontalLayout_10 = QHBoxLayout(self.w_context)
        self.horizontalLayout_10.setObjectName(u"horizontalLayout_10")
        self.horizontalLayout_10.setContentsMargins(9, 0, 9, 0)
        self.label_4 = QLabel(self.w_context)
        self.label_4.setObjectName(u"label_4")

        self.horizontalLayout_10.addWidget(self.label_4)

        self.horizontalSpacer_5 = QSpacerItem(37, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_10.addItem(self.horizontalSpacer_5)

        self.l_context = QLabel(self.w_context)
        self.l_context.setObjectName(u"l_context")

        self.horizontalLayout_10.addWidget(self.l_context)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_10.addItem(self.horizontalSpacer)

        self.b_context = QPushButton(self.w_context)
        self.b_context.setObjectName(u"b_context")

        self.horizontalLayout_10.addWidget(self.b_context)

        self.cb_context = QComboBox(self.w_context)
        self.cb_context.setObjectName(u"cb_context")

        self.horizontalLayout_10.addWidget(self.cb_context)


        self.lo_general.addWidget(self.w_context)

        self.w_taskname = QWidget(self.gb_general)
        self.w_taskname.setObjectName(u"w_taskname")
        self.horizontalLayout_4 = QHBoxLayout(self.w_taskname)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.horizontalLayout_4.setContentsMargins(9, 5, 9, 5)
        self.l_tasklabel = QLabel(self.w_taskname)
        self.l_tasklabel.setObjectName(u"l_tasklabel")

        self.horizontalLayout_4.addWidget(self.l_tasklabel)

        self.l_taskName = QLabel(self.w_taskname)
        self.l_taskName.setObjectName(u"l_taskName")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.l_taskName.sizePolicy().hasHeightForWidth())
        self.l_taskName.setSizePolicy(sizePolicy)
        self.l_taskName.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.horizontalLayout_4.addWidget(self.l_taskName)

        self.b_changeTask = QPushButton(self.w_taskname)
        self.b_changeTask.setObjectName(u"b_changeTask")
        self.b_changeTask.setEnabled(True)
        self.b_changeTask.setFocusPolicy(Qt.FocusPolicy.NoFocus)

        self.horizontalLayout_4.addWidget(self.b_changeTask)


        self.lo_general.addWidget(self.w_taskname)

        self.w_range = QWidget(self.gb_general)
        self.w_range.setObjectName(u"w_range")
        self.horizontalLayout_6 = QHBoxLayout(self.w_range)
        self.horizontalLayout_6.setSpacing(0)
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.horizontalLayout_6.setContentsMargins(9, 0, 9, 0)
        self.label_3 = QLabel(self.w_range)
        self.label_3.setObjectName(u"label_3")

        self.horizontalLayout_6.addWidget(self.label_3)

        self.horizontalSpacer_2 = QSpacerItem(37, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_6.addItem(self.horizontalSpacer_2)

        self.cb_rangeType = QComboBox(self.w_range)
        self.cb_rangeType.setObjectName(u"cb_rangeType")

        self.horizontalLayout_6.addWidget(self.cb_rangeType)


        self.lo_general.addWidget(self.w_range)

        self.f_frameRange_2 = QWidget(self.gb_general)
        self.f_frameRange_2.setObjectName(u"f_frameRange_2")
        self.gridLayout = QGridLayout(self.f_frameRange_2)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(9, 0, 9, 0)
        self.l_rangeEnd = QLabel(self.f_frameRange_2)
        self.l_rangeEnd.setObjectName(u"l_rangeEnd")
        self.l_rangeEnd.setMinimumSize(QSize(30, 0))
        self.l_rangeEnd.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout.addWidget(self.l_rangeEnd, 1, 5, 1, 1)

        self.sp_rangeEnd = QSpinBox(self.f_frameRange_2)
        self.sp_rangeEnd.setObjectName(u"sp_rangeEnd")
        self.sp_rangeEnd.setMaximum(99999)
        self.sp_rangeEnd.setValue(1100)

        self.gridLayout.addWidget(self.sp_rangeEnd, 1, 6, 1, 1)

        self.sp_rangeStart = QSpinBox(self.f_frameRange_2)
        self.sp_rangeStart.setObjectName(u"sp_rangeStart")
        self.sp_rangeStart.setMaximum(99999)
        self.sp_rangeStart.setValue(1001)

        self.gridLayout.addWidget(self.sp_rangeStart, 0, 6, 1, 1)

        self.l_rangeStart = QLabel(self.f_frameRange_2)
        self.l_rangeStart.setObjectName(u"l_rangeStart")
        self.l_rangeStart.setMinimumSize(QSize(30, 0))
        self.l_rangeStart.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout.addWidget(self.l_rangeStart, 0, 5, 1, 1)

        self.l_rangeStartInfo = QLabel(self.f_frameRange_2)
        self.l_rangeStartInfo.setObjectName(u"l_rangeStartInfo")

        self.gridLayout.addWidget(self.l_rangeStartInfo, 0, 0, 1, 1)

        self.horizontalSpacer_7 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer_7, 0, 4, 1, 1)

        self.l_rangeEndInfo = QLabel(self.f_frameRange_2)
        self.l_rangeEndInfo.setObjectName(u"l_rangeEndInfo")

        self.gridLayout.addWidget(self.l_rangeEndInfo, 1, 0, 1, 1)


        self.lo_general.addWidget(self.f_frameRange_2)

        self.w_master = QWidget(self.gb_general)
        self.w_master.setObjectName(u"w_master")
        self.horizontalLayout_20 = QHBoxLayout(self.w_master)
        self.horizontalLayout_20.setSpacing(0)
        self.horizontalLayout_20.setObjectName(u"horizontalLayout_20")
        self.horizontalLayout_20.setContentsMargins(9, 0, 9, 0)
        self.l_master = QLabel(self.w_master)
        self.l_master.setObjectName(u"l_master")

        self.horizontalLayout_20.addWidget(self.l_master)

        self.horizontalSpacer_29 = QSpacerItem(113, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_20.addItem(self.horizontalSpacer_29)

        self.chb_master = QCheckBox(self.w_master)
        self.chb_master.setObjectName(u"chb_master")
        self.chb_master.setChecked(True)

        self.horizontalLayout_20.addWidget(self.chb_master)


        self.lo_general.addWidget(self.w_master)

        self.w_outPath = QWidget(self.gb_general)
        self.w_outPath.setObjectName(u"w_outPath")
        self.horizontalLayout_11 = QHBoxLayout(self.w_outPath)
        self.horizontalLayout_11.setSpacing(0)
        self.horizontalLayout_11.setObjectName(u"horizontalLayout_11")
        self.horizontalLayout_11.setContentsMargins(9, 0, 9, 0)
        self.l_outPath = QLabel(self.w_outPath)
        self.l_outPath.setObjectName(u"l_outPath")

        self.horizontalLayout_11.addWidget(self.l_outPath)

        self.horizontalSpacer_6 = QSpacerItem(113, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_11.addItem(self.horizontalSpacer_6)

        self.cb_outPath = QComboBox(self.w_outPath)
        self.cb_outPath.setObjectName(u"cb_outPath")
        self.cb_outPath.setMinimumSize(QSize(124, 0))

        self.horizontalLayout_11.addWidget(self.cb_outPath)


        self.lo_general.addWidget(self.w_outPath)


        self.verticalLayout.addWidget(self.gb_general)

        self.gb_export = QGroupBox(wg_Synth_SceneExport)
        self.gb_export.setObjectName(u"gb_export")
        self.gb_export.setCheckable(False)
        self.lo_export = QVBoxLayout(self.gb_export)
        self.lo_export.setObjectName(u"lo_export")
        self.lo_export.setContentsMargins(9, 9, 9, 9)
        self.w_outType = QWidget(self.gb_export)
        self.w_outType.setObjectName(u"w_outType")
        self.horizontalLayout_9 = QHBoxLayout(self.w_outType)
        self.horizontalLayout_9.setSpacing(0)
        self.horizontalLayout_9.setObjectName(u"horizontalLayout_9")
        self.horizontalLayout_9.setContentsMargins(9, 5, 9, 5)
        self.l_outType = QLabel(self.w_outType)
        self.l_outType.setObjectName(u"l_outType")

        self.horizontalLayout_9.addWidget(self.l_outType)

        self.horizontalSpacer_3 = QSpacerItem(113, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_9.addItem(self.horizontalSpacer_3)

        self.cb_outType = QComboBox(self.w_outType)
        self.cb_outType.setObjectName(u"cb_outType")
        self.cb_outType.setMinimumSize(QSize(124, 0))

        self.horizontalLayout_9.addWidget(self.cb_outType)


        self.lo_export.addWidget(self.w_outType)

        self.lo_exportSettingsBox = QHBoxLayout()
        self.lo_exportSettingsBox.setObjectName(u"lo_exportSettingsBox")
        self.lo_exportSettingsBox.setContentsMargins(9, -1, 9, -1)
        self.chb_exportSettings = QCheckBox(self.gb_export)
        self.chb_exportSettings.setObjectName(u"chb_exportSettings")

        self.lo_exportSettingsBox.addWidget(self.chb_exportSettings)


        self.lo_export.addLayout(self.lo_exportSettingsBox)

        self.w_exportSettings = QWidget(self.gb_export)
        self.w_exportSettings.setObjectName(u"w_exportSettings")
        self.lo_exportSettings = QVBoxLayout(self.w_exportSettings)
        self.lo_exportSettings.setObjectName(u"lo_exportSettings")

        self.lo_export.addWidget(self.w_exportSettings)

        self.lo_sceneHierarchyBox = QHBoxLayout()
        self.lo_sceneHierarchyBox.setObjectName(u"lo_sceneHierarchyBox")
        self.lo_sceneHierarchyBox.setContentsMargins(9, -1, 9, -1)
        self.chb_sceneHierarchy = QCheckBox(self.gb_export)
        self.chb_sceneHierarchy.setObjectName(u"chb_sceneHierarchy")

        self.lo_sceneHierarchyBox.addWidget(self.chb_sceneHierarchy)


        self.lo_export.addLayout(self.lo_sceneHierarchyBox)

        self.w_sceneHierarchy = QWidget(self.gb_export)
        self.w_sceneHierarchy.setObjectName(u"w_sceneHierarchy")
        self.lo_sceneHierarchy = QVBoxLayout(self.w_sceneHierarchy)
        self.lo_sceneHierarchy.setObjectName(u"lo_sceneHierarchy")
        self.lo_exportAll = QHBoxLayout()
        self.lo_exportAll.setObjectName(u"lo_exportAll")
        self.lo_exportAll.setContentsMargins(9, -1, 9, -1)
        self.chb_customExport = QCheckBox(self.w_sceneHierarchy)
        self.chb_customExport.setObjectName(u"chb_customExport")
        self.chb_customExport.setChecked(True)

        self.lo_exportAll.addWidget(self.chb_customExport)

        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.lo_exportAll.addItem(self.horizontalSpacer_4)

        self.b_refreshExports = QPushButton(self.w_sceneHierarchy)
        self.b_refreshExports.setObjectName(u"b_refreshExports")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.b_refreshExports.sizePolicy().hasHeightForWidth())
        self.b_refreshExports.setSizePolicy(sizePolicy1)
        self.b_refreshExports.setMinimumSize(QSize(30, 0))
        self.b_refreshExports.setMaximumSize(QSize(30, 16777215))

        self.lo_exportAll.addWidget(self.b_refreshExports)


        self.lo_sceneHierarchy.addLayout(self.lo_exportAll)

        self.gb_shotList = QGroupBox(self.w_sceneHierarchy)
        self.gb_shotList.setObjectName(u"gb_shotList")
        self.lo_shotList = QVBoxLayout(self.gb_shotList)
        self.lo_shotList.setObjectName(u"lo_shotList")
        self.lo_shotList.setContentsMargins(15, 10, 15, 10)
        self.lw_shots = QListWidget(self.gb_shotList)
        self.lw_shots.setObjectName(u"lw_shots")
        self.lw_shots.setMinimumSize(QSize(0, 75))
        self.lw_shots.setMaximumSize(QSize(16777215, 75))

        self.lo_shotList.addWidget(self.lw_shots)


        self.lo_sceneHierarchy.addWidget(self.gb_shotList)

        self.gb_meshList = QGroupBox(self.w_sceneHierarchy)
        self.gb_meshList.setObjectName(u"gb_meshList")
        self.lo_meshList = QVBoxLayout(self.gb_meshList)
        self.lo_meshList.setObjectName(u"lo_meshList")
        self.lo_meshList.setContentsMargins(15, 10, 15, 10)
        self.lw_meshes = QListWidget(self.gb_meshList)
        self.lw_meshes.setObjectName(u"lw_meshes")

        self.lo_meshList.addWidget(self.lw_meshes)


        self.lo_sceneHierarchy.addWidget(self.gb_meshList)


        self.lo_export.addWidget(self.w_sceneHierarchy)


        self.verticalLayout.addWidget(self.gb_export)

        self.gb_previous = QGroupBox(wg_Synth_SceneExport)
        self.gb_previous.setObjectName(u"gb_previous")
        self.horizontalLayout_13 = QHBoxLayout(self.gb_previous)
        self.horizontalLayout_13.setObjectName(u"horizontalLayout_13")
        self.horizontalLayout_13.setContentsMargins(9, 9, 9, 9)
        self.scrollArea = QScrollArea(self.gb_previous)
        self.scrollArea.setObjectName(u"scrollArea")
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 348, 69))
        self.horizontalLayout_12 = QHBoxLayout(self.scrollAreaWidgetContents)
        self.horizontalLayout_12.setObjectName(u"horizontalLayout_12")
        self.l_pathLast = QLabel(self.scrollAreaWidgetContents)
        self.l_pathLast.setObjectName(u"l_pathLast")

        self.horizontalLayout_12.addWidget(self.l_pathLast)

        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        self.horizontalLayout_13.addWidget(self.scrollArea)

        self.b_pathLast = QToolButton(self.gb_previous)
        self.b_pathLast.setObjectName(u"b_pathLast")
        self.b_pathLast.setEnabled(True)
        self.b_pathLast.setArrowType(Qt.ArrowType.DownArrow)

        self.horizontalLayout_13.addWidget(self.b_pathLast)


        self.verticalLayout.addWidget(self.gb_previous)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)

        QWidget.setTabOrder(self.e_name, self.b_context)
        QWidget.setTabOrder(self.b_context, self.cb_context)
        QWidget.setTabOrder(self.cb_context, self.cb_rangeType)
        QWidget.setTabOrder(self.cb_rangeType, self.sp_rangeStart)
        QWidget.setTabOrder(self.sp_rangeStart, self.sp_rangeEnd)
        QWidget.setTabOrder(self.sp_rangeEnd, self.chb_master)
        QWidget.setTabOrder(self.chb_master, self.cb_outPath)
        QWidget.setTabOrder(self.cb_outPath, self.cb_outType)
        QWidget.setTabOrder(self.cb_outType, self.scrollArea)
        QWidget.setTabOrder(self.scrollArea, self.b_pathLast)

        self.retranslateUi(wg_Synth_SceneExport)

        QMetaObject.connectSlotsByName(wg_Synth_SceneExport)
    # setupUi

    def retranslateUi(self, wg_Synth_SceneExport):
        wg_Synth_SceneExport.setWindowTitle(QCoreApplication.translate("wg_Synth_SceneExport", u"Export", None))
        self.l_name.setText(QCoreApplication.translate("wg_Synth_SceneExport", u"Name:", None))
        self.l_class.setText(QCoreApplication.translate("wg_Synth_SceneExport", u"Scene Export", None))
        self.gb_general.setTitle(QCoreApplication.translate("wg_Synth_SceneExport", u"General", None))
        self.l_comment.setText(QCoreApplication.translate("wg_Synth_SceneExport", u"Comment:", None))
        self.label_4.setText(QCoreApplication.translate("wg_Synth_SceneExport", u"Context:", None))
        self.l_context.setText("")
        self.b_context.setText(QCoreApplication.translate("wg_Synth_SceneExport", u"Select", None))
        self.l_tasklabel.setText(QCoreApplication.translate("wg_Synth_SceneExport", u"Productname:", None))
        self.l_taskName.setText("")
        self.b_changeTask.setText(QCoreApplication.translate("wg_Synth_SceneExport", u"change", None))
        self.label_3.setText(QCoreApplication.translate("wg_Synth_SceneExport", u"Framerange:", None))
        self.l_rangeEnd.setText(QCoreApplication.translate("wg_Synth_SceneExport", u"1100", None))
        self.l_rangeStart.setText(QCoreApplication.translate("wg_Synth_SceneExport", u"1001", None))
        self.l_rangeStartInfo.setText(QCoreApplication.translate("wg_Synth_SceneExport", u"Start:", None))
        self.l_rangeEndInfo.setText(QCoreApplication.translate("wg_Synth_SceneExport", u"End:", None))
        self.l_master.setText(QCoreApplication.translate("wg_Synth_SceneExport", u"Update Master Version:", None))
        self.chb_master.setText("")
        self.l_outPath.setText(QCoreApplication.translate("wg_Synth_SceneExport", u"Location:", None))
        self.gb_export.setTitle(QCoreApplication.translate("wg_Synth_SceneExport", u"Export", None))
        self.l_outType.setText(QCoreApplication.translate("wg_Synth_SceneExport", u"Output Type:", None))
        self.chb_exportSettings.setText(QCoreApplication.translate("wg_Synth_SceneExport", u"Export Settings", None))
        self.chb_sceneHierarchy.setText(QCoreApplication.translate("wg_Synth_SceneExport", u"Scene Hierarchy", None))
        self.chb_customExport.setText(QCoreApplication.translate("wg_Synth_SceneExport", u"Customize Export", None))
        self.b_refreshExports.setText("")
        self.gb_shotList.setTitle(QCoreApplication.translate("wg_Synth_SceneExport", u"Shots", None))
        self.gb_meshList.setTitle(QCoreApplication.translate("wg_Synth_SceneExport", u"Meshes", None))
        self.gb_previous.setTitle(QCoreApplication.translate("wg_Synth_SceneExport", u"Last export", None))
        self.l_pathLast.setText(QCoreApplication.translate("wg_Synth_SceneExport", u"None", None))
        self.b_pathLast.setText(QCoreApplication.translate("wg_Synth_SceneExport", u"...", None))
    # retranslateUi

