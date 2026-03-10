# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'Synth_Render_StMap.ui'
##
## Created by: Qt User Interface Compiler version 6.10.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from qtpy.QtCore import *  # type: ignore
from qtpy.QtGui import *  # type: ignore
from qtpy.QtWidgets import *  # type: ignore

class Ui_wg_Synth_Render_StMap(object):
    def setupUi(self, wg_Synth_Render_StMap):
        if not wg_Synth_Render_StMap.objectName():
            wg_Synth_Render_StMap.setObjectName(u"wg_Synth_Render_StMap")
        wg_Synth_Render_StMap.resize(400, 657)
        self.verticalLayout = QVBoxLayout(wg_Synth_Render_StMap)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.f_name = QWidget(wg_Synth_Render_StMap)
        self.f_name.setObjectName(u"f_name")
        self.horizontalLayout_4 = QHBoxLayout(self.f_name)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.horizontalLayout_4.setContentsMargins(9, 0, 18, 0)
        self.l_name = QLabel(self.f_name)
        self.l_name.setObjectName(u"l_name")

        self.horizontalLayout_4.addWidget(self.l_name)

        self.e_name = QLineEdit(self.f_name)
        self.e_name.setObjectName(u"e_name")

        self.horizontalLayout_4.addWidget(self.e_name)

        self.l_class = QLabel(self.f_name)
        self.l_class.setObjectName(u"l_class")
        font = QFont()
        font.setBold(True)
        self.l_class.setFont(font)

        self.horizontalLayout_4.addWidget(self.l_class)


        self.verticalLayout.addWidget(self.f_name)

        self.gb_imageRender = QGroupBox(wg_Synth_Render_StMap)
        self.gb_imageRender.setObjectName(u"gb_imageRender")
        self.verticalLayout_2 = QVBoxLayout(self.gb_imageRender)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.w_comment = QWidget(self.gb_imageRender)
        self.w_comment.setObjectName(u"w_comment")
        self.horizontalLayout_19 = QHBoxLayout(self.w_comment)
        self.horizontalLayout_19.setSpacing(0)
        self.horizontalLayout_19.setObjectName(u"horizontalLayout_19")
        self.horizontalLayout_19.setContentsMargins(9, 0, 9, 0)
        self.l_comment = QLabel(self.w_comment)
        self.l_comment.setObjectName(u"l_comment")
        self.l_comment.setMinimumSize(QSize(40, 0))
        self.l_comment.setMaximumSize(QSize(95, 16777215))

        self.horizontalLayout_19.addWidget(self.l_comment)

        self.horizontalSpacer_8 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_19.addItem(self.horizontalSpacer_8)

        self.e_comment = QLineEdit(self.w_comment)
        self.e_comment.setObjectName(u"e_comment")

        self.horizontalLayout_19.addWidget(self.e_comment)


        self.verticalLayout_2.addWidget(self.w_comment)

        self.w_context = QWidget(self.gb_imageRender)
        self.w_context.setObjectName(u"w_context")
        self.horizontalLayout_11 = QHBoxLayout(self.w_context)
        self.horizontalLayout_11.setObjectName(u"horizontalLayout_11")
        self.horizontalLayout_11.setContentsMargins(9, 0, 9, 0)
        self.l_contextName = QLabel(self.w_context)
        self.l_contextName.setObjectName(u"l_contextName")

        self.horizontalLayout_11.addWidget(self.l_contextName)

        self.horizontalSpacer_5 = QSpacerItem(37, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_11.addItem(self.horizontalSpacer_5)

        self.l_context = QLabel(self.w_context)
        self.l_context.setObjectName(u"l_context")

        self.horizontalLayout_11.addWidget(self.l_context)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_11.addItem(self.horizontalSpacer_3)

        self.b_context = QPushButton(self.w_context)
        self.b_context.setObjectName(u"b_context")

        self.horizontalLayout_11.addWidget(self.b_context)

        self.cb_context = QComboBox(self.w_context)
        self.cb_context.setObjectName(u"cb_context")

        self.horizontalLayout_11.addWidget(self.cb_context)


        self.verticalLayout_2.addWidget(self.w_context)

        self.f_taskname = QWidget(self.gb_imageRender)
        self.f_taskname.setObjectName(u"f_taskname")
        self.horizontalLayout_10 = QHBoxLayout(self.f_taskname)
        self.horizontalLayout_10.setObjectName(u"horizontalLayout_10")
        self.horizontalLayout_10.setContentsMargins(9, 0, 9, 0)
        self.l_identifier = QLabel(self.f_taskname)
        self.l_identifier.setObjectName(u"l_identifier")

        self.horizontalLayout_10.addWidget(self.l_identifier)

        self.l_taskName = QLabel(self.f_taskname)
        self.l_taskName.setObjectName(u"l_taskName")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.l_taskName.sizePolicy().hasHeightForWidth())
        self.l_taskName.setSizePolicy(sizePolicy)
        self.l_taskName.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.horizontalLayout_10.addWidget(self.l_taskName)

        self.b_changeTask = QPushButton(self.f_taskname)
        self.b_changeTask.setObjectName(u"b_changeTask")
        self.b_changeTask.setEnabled(True)
        self.b_changeTask.setFocusPolicy(Qt.FocusPolicy.NoFocus)

        self.horizontalLayout_10.addWidget(self.b_changeTask)


        self.verticalLayout_2.addWidget(self.f_taskname)

        self.lo_renderType = QHBoxLayout()
        self.lo_renderType.setObjectName(u"lo_renderType")
        self.lo_renderType.setContentsMargins(9, -1, 9, -1)
        self.l_renderType = QLabel(self.gb_imageRender)
        self.l_renderType.setObjectName(u"l_renderType")

        self.lo_renderType.addWidget(self.l_renderType)

        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.lo_renderType.addItem(self.horizontalSpacer_4)

        self.rb_renderType_single = QRadioButton(self.gb_imageRender)
        self.rb_renderType_single.setObjectName(u"rb_renderType_single")
        self.rb_renderType_single.setLayoutDirection(Qt.LayoutDirection.RightToLeft)
        self.rb_renderType_single.setChecked(True)

        self.lo_renderType.addWidget(self.rb_renderType_single)

        self.horizontalSpacer_6 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.lo_renderType.addItem(self.horizontalSpacer_6)

        self.rb_renderType_seq = QRadioButton(self.gb_imageRender)
        self.rb_renderType_seq.setObjectName(u"rb_renderType_seq")
        self.rb_renderType_seq.setLayoutDirection(Qt.LayoutDirection.RightToLeft)

        self.lo_renderType.addWidget(self.rb_renderType_seq)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.lo_renderType.addItem(self.horizontalSpacer_2)


        self.verticalLayout_2.addLayout(self.lo_renderType)

        self.w_format = QWidget(self.gb_imageRender)
        self.w_format.setObjectName(u"w_format")
        self.horizontalLayout_6 = QHBoxLayout(self.w_format)
        self.horizontalLayout_6.setSpacing(0)
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.horizontalLayout_6.setContentsMargins(9, 0, 9, 0)
        self.l_format = QLabel(self.w_format)
        self.l_format.setObjectName(u"l_format")

        self.horizontalLayout_6.addWidget(self.l_format)

        self.horizontalSpacer_12 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_6.addItem(self.horizontalSpacer_12)

        self.cb_format = QComboBox(self.w_format)
        self.cb_format.setObjectName(u"cb_format")
        self.cb_format.setMinimumSize(QSize(150, 0))

        self.horizontalLayout_6.addWidget(self.cb_format)


        self.verticalLayout_2.addWidget(self.w_format)

        self.f_cam = QWidget(self.gb_imageRender)
        self.f_cam.setObjectName(u"f_cam")
        self.horizontalLayout_2 = QHBoxLayout(self.f_cam)
        self.horizontalLayout_2.setSpacing(0)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(9, 0, 9, 0)
        self.l_camera = QLabel(self.f_cam)
        self.l_camera.setObjectName(u"l_camera")

        self.horizontalLayout_2.addWidget(self.l_camera)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer)

        self.cb_cam = QComboBox(self.f_cam)
        self.cb_cam.setObjectName(u"cb_cam")
        self.cb_cam.setMinimumSize(QSize(150, 0))

        self.horizontalLayout_2.addWidget(self.cb_cam)


        self.verticalLayout_2.addWidget(self.f_cam)

        self.f_resolution = QWidget(self.gb_imageRender)
        self.f_resolution.setObjectName(u"f_resolution")
        self.horizontalLayout_9 = QHBoxLayout(self.f_resolution)
        self.horizontalLayout_9.setSpacing(6)
        self.horizontalLayout_9.setObjectName(u"horizontalLayout_9")
        self.horizontalLayout_9.setContentsMargins(9, 0, 9, 0)
        self.l_rezOverride = QLabel(self.f_resolution)
        self.l_rezOverride.setObjectName(u"l_rezOverride")
        self.l_rezOverride.setEnabled(True)

        self.horizontalLayout_9.addWidget(self.l_rezOverride)

        self.horizontalSpacer_9 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_9.addItem(self.horizontalSpacer_9)

        self.chb_resOverride = QCheckBox(self.f_resolution)
        self.chb_resOverride.setObjectName(u"chb_resOverride")

        self.horizontalLayout_9.addWidget(self.chb_resOverride)

        self.sp_resWidth = QSpinBox(self.f_resolution)
        self.sp_resWidth.setObjectName(u"sp_resWidth")
        self.sp_resWidth.setEnabled(False)
        self.sp_resWidth.setMinimum(1)
        self.sp_resWidth.setMaximum(99999)
        self.sp_resWidth.setValue(1280)

        self.horizontalLayout_9.addWidget(self.sp_resWidth)

        self.sp_resHeight = QSpinBox(self.f_resolution)
        self.sp_resHeight.setObjectName(u"sp_resHeight")
        self.sp_resHeight.setEnabled(False)
        self.sp_resHeight.setMinimum(1)
        self.sp_resHeight.setMaximum(99999)
        self.sp_resHeight.setValue(720)

        self.horizontalLayout_9.addWidget(self.sp_resHeight)

        self.b_resPresets = QPushButton(self.f_resolution)
        self.b_resPresets.setObjectName(u"b_resPresets")
        self.b_resPresets.setEnabled(False)
        self.b_resPresets.setMinimumSize(QSize(23, 23))
        self.b_resPresets.setMaximumSize(QSize(23, 23))
        self.b_resPresets.setFocusPolicy(Qt.FocusPolicy.NoFocus)

        self.horizontalLayout_9.addWidget(self.b_resPresets)


        self.verticalLayout_2.addWidget(self.f_resolution)

        self.w_renderPreset = QWidget(self.gb_imageRender)
        self.w_renderPreset.setObjectName(u"w_renderPreset")
        self.horizontalLayout_14 = QHBoxLayout(self.w_renderPreset)
        self.horizontalLayout_14.setObjectName(u"horizontalLayout_14")
        self.horizontalLayout_14.setContentsMargins(-1, 0, -1, 0)
        self.l_renderPreset = QLabel(self.w_renderPreset)
        self.l_renderPreset.setObjectName(u"l_renderPreset")

        self.horizontalLayout_14.addWidget(self.l_renderPreset)

        self.horizontalSpacer_7 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_14.addItem(self.horizontalSpacer_7)

        self.chb_renderPreset = QCheckBox(self.w_renderPreset)
        self.chb_renderPreset.setObjectName(u"chb_renderPreset")

        self.horizontalLayout_14.addWidget(self.chb_renderPreset)

        self.cb_renderPreset = QComboBox(self.w_renderPreset)
        self.cb_renderPreset.setObjectName(u"cb_renderPreset")
        self.cb_renderPreset.setEnabled(False)
        self.cb_renderPreset.setMinimumSize(QSize(150, 0))

        self.horizontalLayout_14.addWidget(self.cb_renderPreset)


        self.verticalLayout_2.addWidget(self.w_renderPreset)

        self.w_master = QWidget(self.gb_imageRender)
        self.w_master.setObjectName(u"w_master")
        self.horizontalLayout_17 = QHBoxLayout(self.w_master)
        self.horizontalLayout_17.setSpacing(0)
        self.horizontalLayout_17.setObjectName(u"horizontalLayout_17")
        self.horizontalLayout_17.setContentsMargins(9, 0, 9, 0)
        self.l_outPath_2 = QLabel(self.w_master)
        self.l_outPath_2.setObjectName(u"l_outPath_2")

        self.horizontalLayout_17.addWidget(self.l_outPath_2)

        self.horizontalSpacer_28 = QSpacerItem(113, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_17.addItem(self.horizontalSpacer_28)

        self.cb_master = QComboBox(self.w_master)
        self.cb_master.setObjectName(u"cb_master")
        self.cb_master.setMinimumSize(QSize(150, 0))

        self.horizontalLayout_17.addWidget(self.cb_master)


        self.verticalLayout_2.addWidget(self.w_master)

        self.w_outPath = QWidget(self.gb_imageRender)
        self.w_outPath.setObjectName(u"w_outPath")
        self.horizontalLayout_16 = QHBoxLayout(self.w_outPath)
        self.horizontalLayout_16.setSpacing(0)
        self.horizontalLayout_16.setObjectName(u"horizontalLayout_16")
        self.horizontalLayout_16.setContentsMargins(9, 0, 9, 0)
        self.l_outPath = QLabel(self.w_outPath)
        self.l_outPath.setObjectName(u"l_outPath")

        self.horizontalLayout_16.addWidget(self.l_outPath)

        self.horizontalSpacer_27 = QSpacerItem(113, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_16.addItem(self.horizontalSpacer_27)

        self.cb_outPath = QComboBox(self.w_outPath)
        self.cb_outPath.setObjectName(u"cb_outPath")
        self.cb_outPath.setMinimumSize(QSize(150, 0))

        self.horizontalLayout_16.addWidget(self.cb_outPath)


        self.verticalLayout_2.addWidget(self.w_outPath)

        self.w_version = QWidget(self.gb_imageRender)
        self.w_version.setObjectName(u"w_version")
        self.horizontalLayout_12 = QHBoxLayout(self.w_version)
        self.horizontalLayout_12.setSpacing(6)
        self.horizontalLayout_12.setObjectName(u"horizontalLayout_12")
        self.horizontalLayout_12.setContentsMargins(9, 0, 9, 0)
        self.label_8 = QLabel(self.w_version)
        self.label_8.setObjectName(u"label_8")
        self.label_8.setEnabled(True)

        self.horizontalLayout_12.addWidget(self.label_8)

        self.horizontalSpacer_10 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_12.addItem(self.horizontalSpacer_10)

        self.chb_version = QCheckBox(self.w_version)
        self.chb_version.setObjectName(u"chb_version")

        self.horizontalLayout_12.addWidget(self.chb_version)

        self.sp_version = QSpinBox(self.w_version)
        self.sp_version.setObjectName(u"sp_version")
        self.sp_version.setEnabled(False)
        self.sp_version.setMinimum(1)
        self.sp_version.setMaximum(99999)

        self.horizontalLayout_12.addWidget(self.sp_version)

        self.b_version = QPushButton(self.w_version)
        self.b_version.setObjectName(u"b_version")
        self.b_version.setEnabled(False)
        self.b_version.setMinimumSize(QSize(23, 23))
        self.b_version.setMaximumSize(QSize(23, 23))
        self.b_version.setFocusPolicy(Qt.FocusPolicy.NoFocus)

        self.horizontalLayout_12.addWidget(self.b_version)


        self.verticalLayout_2.addWidget(self.w_version)


        self.verticalLayout.addWidget(self.gb_imageRender)

        self.gb_previous = QGroupBox(wg_Synth_Render_StMap)
        self.gb_previous.setObjectName(u"gb_previous")
        self.gb_previous.setCheckable(False)
        self.gb_previous.setChecked(False)
        self.horizontalLayout_18 = QHBoxLayout(self.gb_previous)
        self.horizontalLayout_18.setObjectName(u"horizontalLayout_18")
        self.horizontalLayout_18.setContentsMargins(9, 9, 9, 9)
        self.scrollArea = QScrollArea(self.gb_previous)
        self.scrollArea.setObjectName(u"scrollArea")
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 349, 241))
        self.verticalLayout_3 = QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.l_pathLast = QLabel(self.scrollAreaWidgetContents)
        self.l_pathLast.setObjectName(u"l_pathLast")

        self.verticalLayout_3.addWidget(self.l_pathLast)

        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        self.horizontalLayout_18.addWidget(self.scrollArea)

        self.b_pathLast = QToolButton(self.gb_previous)
        self.b_pathLast.setObjectName(u"b_pathLast")
        self.b_pathLast.setEnabled(True)
        self.b_pathLast.setArrowType(Qt.ArrowType.DownArrow)

        self.horizontalLayout_18.addWidget(self.b_pathLast)


        self.verticalLayout.addWidget(self.gb_previous)

        QWidget.setTabOrder(self.e_name, self.b_context)
        QWidget.setTabOrder(self.b_context, self.cb_context)
        QWidget.setTabOrder(self.cb_context, self.cb_cam)
        QWidget.setTabOrder(self.cb_cam, self.chb_resOverride)
        QWidget.setTabOrder(self.chb_resOverride, self.sp_resWidth)
        QWidget.setTabOrder(self.sp_resWidth, self.sp_resHeight)
        QWidget.setTabOrder(self.sp_resHeight, self.chb_renderPreset)
        QWidget.setTabOrder(self.chb_renderPreset, self.cb_renderPreset)
        QWidget.setTabOrder(self.cb_renderPreset, self.cb_master)
        QWidget.setTabOrder(self.cb_master, self.cb_outPath)
        QWidget.setTabOrder(self.cb_outPath, self.cb_format)
        QWidget.setTabOrder(self.cb_format, self.scrollArea)
        QWidget.setTabOrder(self.scrollArea, self.b_pathLast)

        self.retranslateUi(wg_Synth_Render_StMap)

        QMetaObject.connectSlotsByName(wg_Synth_Render_StMap)
    # setupUi

    def retranslateUi(self, wg_Synth_Render_StMap):
        wg_Synth_Render_StMap.setWindowTitle(QCoreApplication.translate("wg_Synth_Render_StMap", u"Image Render", None))
        self.l_name.setText(QCoreApplication.translate("wg_Synth_Render_StMap", u"Name:", None))
        self.l_class.setText(QCoreApplication.translate("wg_Synth_Render_StMap", u"ImageRender", None))
        self.gb_imageRender.setTitle(QCoreApplication.translate("wg_Synth_Render_StMap", u"General", None))
        self.l_comment.setText(QCoreApplication.translate("wg_Synth_Render_StMap", u"Comment:", None))
        self.l_contextName.setText(QCoreApplication.translate("wg_Synth_Render_StMap", u"Context:", None))
        self.l_context.setText("")
        self.b_context.setText(QCoreApplication.translate("wg_Synth_Render_StMap", u"Select", None))
        self.l_identifier.setText(QCoreApplication.translate("wg_Synth_Render_StMap", u"Identifier:", None))
        self.l_taskName.setText("")
        self.b_changeTask.setText(QCoreApplication.translate("wg_Synth_Render_StMap", u"change", None))
        self.l_renderType.setText(QCoreApplication.translate("wg_Synth_Render_StMap", u"Render Type:", None))
        self.rb_renderType_single.setText(QCoreApplication.translate("wg_Synth_Render_StMap", u"Single Image  ", None))
        self.rb_renderType_seq.setText(QCoreApplication.translate("wg_Synth_Render_StMap", u"Sequence  ", None))
        self.l_format.setText(QCoreApplication.translate("wg_Synth_Render_StMap", u"Format:", None))
        self.l_camera.setText(QCoreApplication.translate("wg_Synth_Render_StMap", u"Camera:", None))
        self.l_rezOverride.setText(QCoreApplication.translate("wg_Synth_Render_StMap", u"Resolution override:", None))
        self.chb_resOverride.setText("")
        self.b_resPresets.setText(QCoreApplication.translate("wg_Synth_Render_StMap", u"\u25bc", None))
        self.l_renderPreset.setText(QCoreApplication.translate("wg_Synth_Render_StMap", u"Rendersettings preset:", None))
        self.chb_renderPreset.setText("")
        self.l_outPath_2.setText(QCoreApplication.translate("wg_Synth_Render_StMap", u"Master Version:", None))
        self.l_outPath.setText(QCoreApplication.translate("wg_Synth_Render_StMap", u"Location:", None))
        self.label_8.setText(QCoreApplication.translate("wg_Synth_Render_StMap", u"Version override:", None))
        self.chb_version.setText("")
        self.b_version.setText(QCoreApplication.translate("wg_Synth_Render_StMap", u"\u25bc", None))
        self.gb_previous.setTitle(QCoreApplication.translate("wg_Synth_Render_StMap", u"Previous render", None))
        self.l_pathLast.setText(QCoreApplication.translate("wg_Synth_Render_StMap", u"None", None))
        self.b_pathLast.setText(QCoreApplication.translate("wg_Synth_Render_StMap", u"...", None))
    # retranslateUi

