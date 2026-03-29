# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'synth_StMap.ui'
##
## Created by: Qt User Interface Compiler version 6.10.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QCheckBox, QComboBox, QGridLayout,
    QGroupBox, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QRadioButton, QScrollArea, QSizePolicy,
    QSpacerItem, QSpinBox, QToolButton, QVBoxLayout,
    QWidget)

class Ui_wg_synth_StMap(object):
    def setupUi(self, wg_synth_StMap):
        if not wg_synth_StMap.objectName():
            wg_synth_StMap.setObjectName(u"wg_synth_StMap")
        wg_synth_StMap.resize(427, 982)
        self.verticalLayout = QVBoxLayout(wg_synth_StMap)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 9, 0, 9)
        self.f_name = QWidget(wg_synth_StMap)
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

        self.gb_imageRender = QGroupBox(wg_synth_StMap)
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

        self.f_frame = QWidget(self.gb_imageRender)
        self.f_frame.setObjectName(u"f_frame")
        self.f_range = QHBoxLayout(self.f_frame)
        self.f_range.setObjectName(u"f_range")
        self.f_range.setContentsMargins(9, -1, 9, -1)
        self.l_framerange = QLabel(self.f_frame)
        self.l_framerange.setObjectName(u"l_framerange")

        self.f_range.addWidget(self.l_framerange)

        self.horizontalSpacer_16 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.f_range.addItem(self.horizontalSpacer_16)

        self.cb_rangeType = QComboBox(self.f_frame)
        self.cb_rangeType.setObjectName(u"cb_rangeType")
        self.cb_rangeType.setMinimumSize(QSize(150, 0))

        self.f_range.addWidget(self.cb_rangeType)


        self.verticalLayout_2.addWidget(self.f_frame)

        self.w_frameRangeValues = QWidget(self.gb_imageRender)
        self.w_frameRangeValues.setObjectName(u"w_frameRangeValues")
        self.gridLayout = QGridLayout(self.w_frameRangeValues)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(9, -1, 9, -1)
        self.l_rangeStart = QLabel(self.w_frameRangeValues)
        self.l_rangeStart.setObjectName(u"l_rangeStart")

        self.gridLayout.addWidget(self.l_rangeStart, 0, 2, 1, 1)

        self.sp_rangeStart = QSpinBox(self.w_frameRangeValues)
        self.sp_rangeStart.setObjectName(u"sp_rangeStart")
        self.sp_rangeStart.setMaximum(99999)
        self.sp_rangeStart.setValue(1000)

        self.gridLayout.addWidget(self.sp_rangeStart, 0, 3, 1, 1)

        self.l_end = QLabel(self.w_frameRangeValues)
        self.l_end.setObjectName(u"l_end")

        self.gridLayout.addWidget(self.l_end, 1, 0, 1, 1)

        self.sp_rangeEnd = QSpinBox(self.w_frameRangeValues)
        self.sp_rangeEnd.setObjectName(u"sp_rangeEnd")
        self.sp_rangeEnd.setMaximum(99999)
        self.sp_rangeEnd.setValue(1001)

        self.gridLayout.addWidget(self.sp_rangeEnd, 1, 3, 1, 1)

        self.l_rangeEnd = QLabel(self.w_frameRangeValues)
        self.l_rangeEnd.setObjectName(u"l_rangeEnd")

        self.gridLayout.addWidget(self.l_rangeEnd, 1, 2, 1, 1)

        self.l_start = QLabel(self.w_frameRangeValues)
        self.l_start.setObjectName(u"l_start")

        self.gridLayout.addWidget(self.l_start, 0, 0, 1, 1)

        self.horizontalSpacer_17 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer_17, 0, 1, 1, 1)


        self.verticalLayout_2.addWidget(self.w_frameRangeValues)

        self.w_master = QWidget(self.gb_imageRender)
        self.w_master.setObjectName(u"w_master")
        self.horizontalLayout_17 = QHBoxLayout(self.w_master)
        self.horizontalLayout_17.setSpacing(0)
        self.horizontalLayout_17.setObjectName(u"horizontalLayout_17")
        self.horizontalLayout_17.setContentsMargins(9, 0, 9, 0)
        self.l_master = QLabel(self.w_master)
        self.l_master.setObjectName(u"l_master")

        self.horizontalLayout_17.addWidget(self.l_master)

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

        self.gb_options = QGroupBox(wg_synth_StMap)
        self.gb_options.setObjectName(u"gb_options")
        self.verticalLayout_14 = QVBoxLayout(self.gb_options)
        self.verticalLayout_14.setObjectName(u"verticalLayout_14")
        self.verticalLayout_14.setContentsMargins(9, 9, 9, 9)
        self.f_cam = QWidget(self.gb_options)
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


        self.verticalLayout_14.addWidget(self.f_cam)

        self.f_renderScale = QWidget(self.gb_options)
        self.f_renderScale.setObjectName(u"f_renderScale")
        self.horizontalLayout_14 = QHBoxLayout(self.f_renderScale)
        self.horizontalLayout_14.setObjectName(u"horizontalLayout_14")
        self.horizontalLayout_14.setContentsMargins(-1, 0, -1, 0)
        self.l_renderScale = QLabel(self.f_renderScale)
        self.l_renderScale.setObjectName(u"l_renderScale")

        self.horizontalLayout_14.addWidget(self.l_renderScale)

        self.horizontalSpacer_7 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_14.addItem(self.horizontalSpacer_7)

        self.chb_scaleOverride = QCheckBox(self.f_renderScale)
        self.chb_scaleOverride.setObjectName(u"chb_scaleOverride")

        self.horizontalLayout_14.addWidget(self.chb_scaleOverride)

        self.horizontalSpacer_9 = QSpacerItem(10, 20, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_14.addItem(self.horizontalSpacer_9)

        self.cb_renderScale = QComboBox(self.f_renderScale)
        self.cb_renderScale.setObjectName(u"cb_renderScale")
        self.cb_renderScale.setEnabled(False)
        self.cb_renderScale.setMinimumSize(QSize(150, 0))

        self.horizontalLayout_14.addWidget(self.cb_renderScale)


        self.verticalLayout_14.addWidget(self.f_renderScale)

        self.f_renderFilter = QWidget(self.gb_options)
        self.f_renderFilter.setObjectName(u"f_renderFilter")
        self.horizontalLayout_15 = QHBoxLayout(self.f_renderFilter)
        self.horizontalLayout_15.setObjectName(u"horizontalLayout_15")
        self.horizontalLayout_15.setContentsMargins(-1, 0, -1, 0)
        self.l_renderFilter = QLabel(self.f_renderFilter)
        self.l_renderFilter.setObjectName(u"l_renderFilter")

        self.horizontalLayout_15.addWidget(self.l_renderFilter)

        self.horizontalSpacer_15 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_15.addItem(self.horizontalSpacer_15)

        self.cb_renderFilter = QComboBox(self.f_renderFilter)
        self.cb_renderFilter.setObjectName(u"cb_renderFilter")
        self.cb_renderFilter.setEnabled(False)
        self.cb_renderFilter.setMinimumSize(QSize(150, 0))

        self.horizontalLayout_15.addWidget(self.cb_renderFilter)


        self.verticalLayout_14.addWidget(self.f_renderFilter)

        self.verticalSpacer = QSpacerItem(20, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)

        self.verticalLayout_14.addItem(self.verticalSpacer)

        self.w_format = QWidget(self.gb_options)
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


        self.verticalLayout_14.addWidget(self.w_format)

        self.f_codecOptions_EXR = QWidget(self.gb_options)
        self.f_codecOptions_EXR.setObjectName(u"f_codecOptions_EXR")
        self.horizontalLayout_5 = QHBoxLayout(self.f_codecOptions_EXR)
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.horizontalLayout_5.setContentsMargins(9, -1, 9, -1)
        self.l_exr_Compression = QLabel(self.f_codecOptions_EXR)
        self.l_exr_Compression.setObjectName(u"l_exr_Compression")

        self.horizontalLayout_5.addWidget(self.l_exr_Compression)

        self.horizontalSpacer_18 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_5.addItem(self.horizontalSpacer_18)

        self.cb_exrCompression = QComboBox(self.f_codecOptions_EXR)
        self.cb_exrCompression.setObjectName(u"cb_exrCompression")
        self.cb_exrCompression.setMinimumSize(QSize(150, 0))

        self.horizontalLayout_5.addWidget(self.cb_exrCompression)


        self.verticalLayout_14.addWidget(self.f_codecOptions_EXR)

        self.f_codecOptions_MOV = QWidget(self.gb_options)
        self.f_codecOptions_MOV.setObjectName(u"f_codecOptions_MOV")
        self.horizontalLayout_7 = QHBoxLayout(self.f_codecOptions_MOV)
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.horizontalLayout_7.setContentsMargins(9, -1, 9, -1)
        self.l_movCodec = QLabel(self.f_codecOptions_MOV)
        self.l_movCodec.setObjectName(u"l_movCodec")

        self.horizontalLayout_7.addWidget(self.l_movCodec)

        self.horizontalSpacer_19 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_7.addItem(self.horizontalSpacer_19)

        self.cb_movCodec = QComboBox(self.f_codecOptions_MOV)
        self.cb_movCodec.setObjectName(u"cb_movCodec")
        self.cb_movCodec.setMinimumSize(QSize(150, 0))

        self.horizontalLayout_7.addWidget(self.cb_movCodec)


        self.verticalLayout_14.addWidget(self.f_codecOptions_MOV)

        self.f_codecOptions_MP4 = QWidget(self.gb_options)
        self.f_codecOptions_MP4.setObjectName(u"f_codecOptions_MP4")
        self.verticalLayout_4 = QVBoxLayout(self.f_codecOptions_MP4)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.lo_mp4Codec = QWidget(self.f_codecOptions_MP4)
        self.lo_mp4Codec.setObjectName(u"lo_mp4Codec")
        self.horizontalLayout_8 = QHBoxLayout(self.lo_mp4Codec)
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.horizontalLayout_8.setContentsMargins(9, -1, 9, -1)
        self.l_mp4Codec = QLabel(self.lo_mp4Codec)
        self.l_mp4Codec.setObjectName(u"l_mp4Codec")

        self.horizontalLayout_8.addWidget(self.l_mp4Codec)

        self.horizontalSpacer_20 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_8.addItem(self.horizontalSpacer_20)

        self.cb_mp4Codec = QComboBox(self.lo_mp4Codec)
        self.cb_mp4Codec.setObjectName(u"cb_mp4Codec")
        self.cb_mp4Codec.setMinimumSize(QSize(150, 0))

        self.horizontalLayout_8.addWidget(self.cb_mp4Codec)


        self.verticalLayout_4.addWidget(self.lo_mp4Codec)

        self.lo_mp4Qual = QWidget(self.f_codecOptions_MP4)
        self.lo_mp4Qual.setObjectName(u"lo_mp4Qual")
        self.horizontalLayout_9 = QHBoxLayout(self.lo_mp4Qual)
        self.horizontalLayout_9.setObjectName(u"horizontalLayout_9")
        self.horizontalLayout_9.setContentsMargins(9, -1, 9, -1)
        self.l_mp4Qual = QLabel(self.lo_mp4Qual)
        self.l_mp4Qual.setObjectName(u"l_mp4Qual")

        self.horizontalLayout_9.addWidget(self.l_mp4Qual)

        self.horizontalSpacer_21 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_9.addItem(self.horizontalSpacer_21)

        self.cb_mp4Qual = QComboBox(self.lo_mp4Qual)
        self.cb_mp4Qual.setObjectName(u"cb_mp4Qual")
        self.cb_mp4Qual.setMinimumSize(QSize(150, 0))

        self.horizontalLayout_9.addWidget(self.cb_mp4Qual)


        self.verticalLayout_4.addWidget(self.lo_mp4Qual)


        self.verticalLayout_14.addWidget(self.f_codecOptions_MP4)

        self.f_renderType = QWidget(self.gb_options)
        self.f_renderType.setObjectName(u"f_renderType")
        self.horizontalLayout_3 = QHBoxLayout(self.f_renderType)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_3.setContentsMargins(9, -1, 9, -1)
        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer_4)

        self.rb_renderType_single = QRadioButton(self.f_renderType)
        self.rb_renderType_single.setObjectName(u"rb_renderType_single")
        self.rb_renderType_single.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        self.rb_renderType_single.setChecked(True)

        self.horizontalLayout_3.addWidget(self.rb_renderType_single)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer_2)

        self.rb_renderType_seq = QRadioButton(self.f_renderType)
        self.rb_renderType_seq.setObjectName(u"rb_renderType_seq")
        self.rb_renderType_seq.setLayoutDirection(Qt.LayoutDirection.LeftToRight)

        self.horizontalLayout_3.addWidget(self.rb_renderType_seq)

        self.horizontalSpacer_6 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer_6)


        self.verticalLayout_14.addWidget(self.f_renderType)


        self.verticalLayout.addWidget(self.gb_options)

        self.gb_mapTypes = QGroupBox(wg_synth_StMap)
        self.gb_mapTypes.setObjectName(u"gb_mapTypes")
        self.verticalLayout_5 = QVBoxLayout(self.gb_mapTypes)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.verticalLayout_5.setContentsMargins(9, 9, 9, 9)
        self.widget = QWidget(self.gb_mapTypes)
        self.widget.setObjectName(u"widget")
        self.horizontalLayout = QHBoxLayout(self.widget)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(9, -1, 9, -1)
        self.horizontalSpacer_11 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_11)

        self.chb_undistort = QCheckBox(self.widget)
        self.chb_undistort.setObjectName(u"chb_undistort")

        self.horizontalLayout.addWidget(self.chb_undistort)

        self.horizontalSpacer_14 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_14)

        self.chb_redistort = QCheckBox(self.widget)
        self.chb_redistort.setObjectName(u"chb_redistort")

        self.horizontalLayout.addWidget(self.chb_redistort)

        self.horizontalSpacer_13 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_13)


        self.verticalLayout_5.addWidget(self.widget)


        self.verticalLayout.addWidget(self.gb_mapTypes)

        self.gb_previous = QGroupBox(wg_synth_StMap)
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
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 376, 69))
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
        QWidget.setTabOrder(self.cb_cam, self.chb_scaleOverride)
        QWidget.setTabOrder(self.chb_scaleOverride, self.cb_renderScale)
        QWidget.setTabOrder(self.cb_renderScale, self.cb_master)
        QWidget.setTabOrder(self.cb_master, self.cb_outPath)
        QWidget.setTabOrder(self.cb_outPath, self.cb_format)
        QWidget.setTabOrder(self.cb_format, self.scrollArea)
        QWidget.setTabOrder(self.scrollArea, self.b_pathLast)

        self.retranslateUi(wg_synth_StMap)

        QMetaObject.connectSlotsByName(wg_synth_StMap)
    # setupUi

    def retranslateUi(self, wg_synth_StMap):
        wg_synth_StMap.setWindowTitle(QCoreApplication.translate("wg_synth_StMap", u"Image Render", None))
        self.l_name.setText(QCoreApplication.translate("wg_synth_StMap", u"Name:", None))
        self.l_class.setText(QCoreApplication.translate("wg_synth_StMap", u"STMap", None))
        self.gb_imageRender.setTitle(QCoreApplication.translate("wg_synth_StMap", u"General", None))
        self.l_comment.setText(QCoreApplication.translate("wg_synth_StMap", u"Comment:", None))
        self.l_contextName.setText(QCoreApplication.translate("wg_synth_StMap", u"Context:", None))
        self.l_context.setText("")
        self.b_context.setText(QCoreApplication.translate("wg_synth_StMap", u"Select", None))
        self.l_identifier.setText(QCoreApplication.translate("wg_synth_StMap", u"Identifier:", None))
        self.l_taskName.setText("")
        self.b_changeTask.setText(QCoreApplication.translate("wg_synth_StMap", u"change", None))
        self.l_framerange.setText(QCoreApplication.translate("wg_synth_StMap", u"Framerange:", None))
        self.l_rangeStart.setText(QCoreApplication.translate("wg_synth_StMap", u"1000", None))
        self.l_end.setText(QCoreApplication.translate("wg_synth_StMap", u"End:", None))
        self.l_rangeEnd.setText(QCoreApplication.translate("wg_synth_StMap", u"1001", None))
        self.l_start.setText(QCoreApplication.translate("wg_synth_StMap", u"Start:", None))
        self.l_master.setText(QCoreApplication.translate("wg_synth_StMap", u"Master Version:", None))
        self.l_outPath.setText(QCoreApplication.translate("wg_synth_StMap", u"Location:", None))
        self.label_8.setText(QCoreApplication.translate("wg_synth_StMap", u"Version override:", None))
        self.chb_version.setText("")
        self.b_version.setText(QCoreApplication.translate("wg_synth_StMap", u"\u25bc", None))
        self.gb_options.setTitle(QCoreApplication.translate("wg_synth_StMap", u"Render Options", None))
        self.l_camera.setText(QCoreApplication.translate("wg_synth_StMap", u"Camera:", None))
        self.l_renderScale.setText(QCoreApplication.translate("wg_synth_StMap", u"Output Scale Overide: ", None))
        self.chb_scaleOverride.setText("")
        self.l_renderFilter.setText(QCoreApplication.translate("wg_synth_StMap", u"Scaling Filter: ", None))
        self.l_format.setText(QCoreApplication.translate("wg_synth_StMap", u"Format:", None))
        self.l_exr_Compression.setText(QCoreApplication.translate("wg_synth_StMap", u"EXR Compression:", None))
        self.l_movCodec.setText(QCoreApplication.translate("wg_synth_StMap", u"Codec: ", None))
        self.l_mp4Codec.setText(QCoreApplication.translate("wg_synth_StMap", u"Codec: ", None))
        self.l_mp4Qual.setText(QCoreApplication.translate("wg_synth_StMap", u"Quality: ", None))
        self.rb_renderType_single.setText(QCoreApplication.translate("wg_synth_StMap", u"Single Image  ", None))
        self.rb_renderType_seq.setText(QCoreApplication.translate("wg_synth_StMap", u"Sequence  ", None))
        self.gb_mapTypes.setTitle(QCoreApplication.translate("wg_synth_StMap", u"Map Types", None))
        self.chb_undistort.setText(QCoreApplication.translate("wg_synth_StMap", u"Un-Distort", None))
        self.chb_redistort.setText(QCoreApplication.translate("wg_synth_StMap", u"Re-Distort", None))
        self.gb_previous.setTitle(QCoreApplication.translate("wg_synth_StMap", u"Previous render", None))
        self.l_pathLast.setText(QCoreApplication.translate("wg_synth_StMap", u"None", None))
        self.b_pathLast.setText(QCoreApplication.translate("wg_synth_StMap", u"...", None))
    # retranslateUi

