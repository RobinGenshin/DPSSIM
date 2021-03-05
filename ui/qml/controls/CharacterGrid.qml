import QtQuick 2.15
import QtQuick.Controls 2.15
import QtGraphicalEffects 1.15
import Qt.labs.folderlistmodel 2.15
import QtQml.Models 2.3

Rectangle {
    id: rightMenu
    x: 0
    color: "#00000000"
    radius: 10
    width: 240
    height: 480
    clip: false
    property bool active: if (parent.activeMenu === "character") true; else false
    state: if (active == true) "active"; else "inactive"

    transitions: [
        Transition {
            from: "active"
            to: "inactive"
            ParallelAnimation {
                id: closeMenu
                PropertyAnimation {
                    target: characterGrid
                    property: "width"
                    duration: 500
                    easing.type: Easing.InOutQuad
                    to: 0
                }

                PropertyAnimation {
                    target: characterGrid
                    property: "opacity"
                    duration: 225
                    to: 0
                    from: 1
                }
            }
        },
        Transition {
            from: "inactive"
            to: "active"
            ParallelAnimation {
                id: openMenu
                PropertyAnimation {
                    target: characterGrid
                    property: "width"
                    duration: 500
                    easing.type: Easing.InOutQuad
                    to: if(characterGrid.width == 0) return 240; else return 0
                }

                PropertyAnimation {
                    target: characterGrid
                    property: "opacity"
                    duration: 0
                    to: 0
                }

                SequentialAnimation {
                    PauseAnimation {
                        duration: 200
                    }

                    PropertyAnimation {
                        target: characterGrid
                        property: "opacity"
                        duration: 225
                        to: 1
                        from: 0
                    }
                }
            }
        }
    ]


    Rectangle {
        id: buttons
        height: 60
        visible: true
        color: "#00000000"
        anchors.left: parent.left
        anchors.right: parent.right
        anchors.top: parent.top
        anchors.topMargin: 0
        anchors.rightMargin: 0
        anchors.leftMargin: 0
        RightMenuToggleButton {
            x: 139
            y: 29
            width: 25
            height: 25
            anchors.verticalCenter: parent.verticalCenter
            anchors.verticalCenterOffset: 14
            bgColor: "#e65558"
            onClicked: {
                folderModel.type = "Pyro"
            }
        }
        RightMenuToggleButton {
            x: 108
            y: 29
            width: 25
            height: 25
            anchors.verticalCenter: parent.verticalCenter
            anchors.verticalCenterOffset: 14
            bgColor: "#9dd3fc"
            onClicked: {
                folderModel.type = "Cryo"
            }
        }
        RightMenuToggleButton {
            x: 77
            y: 29
            width: 25
            height: 25
            anchors.verticalCenter: parent.verticalCenter
            anchors.verticalCenterOffset: 14
            bgColor: "#0d6ce8"
            onClicked: {
                folderModel.type = "Hydro"
            }
        }
        RightMenuToggleButton {
            x: 77
            width: 25
            height: 25
            anchors.verticalCenter: parent.verticalCenter
            anchors.verticalCenterOffset: -14
            bgColor: "#ffcd05"
            onClicked: {
                folderModel.type = "Geo"
            }
        }
        RightMenuToggleButton {
            x: 139
            width: 25
            height: 25
            anchors.verticalCenter: parent.verticalCenter
            anchors.verticalCenterOffset: -14
            bgColor: "#673ab7"
            onClicked: {
                folderModel.type = "Electro"
            }
        }
        RightMenuToggleButton {
            x: 108
            width: 25
            height: 25
            anchors.verticalCenter: parent.verticalCenter
            anchors.verticalCenterOffset: -14
            bgColor: "#2dcb6f"
            onClicked: {
                folderModel.type = "Anemo"
            }
        }

        RightMenuToggleButton {
            y: 3
            width: 54
            height: 54
            anchors.verticalCenter: parent.verticalCenter
            anchors.left: parent.left
            anchors.leftMargin: 10
            anchors.verticalCenterOffset: 0
            buttonText: "All"
            onClicked: {
                folderModel.type = "All"
            }
        }
    }

    Rectangle {
        id: gridBox
        color: "#00000000"
        anchors.left: parent.left
        anchors.right: parent.right
        anchors.top: buttons.bottom
        anchors.bottom: parent.bottom
        anchors.topMargin: 20
        anchors.bottomMargin: 50
        clip: true

        Rectangle {
            id: opacityBox
            color: "#101010"
            anchors.fill: parent
            opacity: 1
            visible: false
        }

        Flickable {

            id: flick
            x: 0
            anchors.fill: gridBox
            boundsMovement: Flickable.StopAtBounds
            flickableDirection: Flickable.VerticalFlick
            anchors.rightMargin: 0
            contentWidth: gridBox.width
            contentHeight: grid.height
            clip: false
            boundsBehavior: Flickable.DragAndOvershootBounds
            opacity: Math.max(0.5, 1.0 - Math.abs(verticalOvershoot) / height)
            interactive: if (folderModel.type === "All") true; else false

            Grid {
                id: grid
                anchors.top: parent.top
                width: parent.width
                height: childrenRect.height
                columns: 3

                add: Transition {
                    NumberAnimation { properties: "opacity"; from: 0; to: 1 ; duration: 500}
                }

                move: Transition {
                    NumberAnimation { properties: "opacity"; from: 1; to: 0 ; duration: 500}
                    NumberAnimation { properties: "opacity"; from: 0; to: 1 ; duration: 500}
                }

                Repeater {

                    id: rep
                    model: FolderListModel {

                        id: folderModel
                        objectName: "folderModel"
                        folder: "../images/chars"
                        nameFilters: ["*.png"]
                        property string type: "All"
                    }

                    delegate: SelectorButton {
                        objectName: "selectorButton"
                        btnIconSource: "../images/chars/" + fileName
                        onClicked: {
                            backend.add_character(fileName.replace(".png",""))
                        }
                        charElement: if (["Albedo.png", "Ningguang.png", "Zhongli.png", "Traveler (Geo).png", "Noelle.png"].indexOf(fileName) != -1) {
                                         return "Geo"
                                     } else if (["Traveler (Anemo).png", "Venti.png", "Sucrose.png", "Xiao.png", "Jean.png"].indexOf(fileName) != -1) {
                                         return "Anemo"
                                     } else if (["Diluc.png", "Amber.png", "Xinyan.png", "Xiangling.png", "Bennett.png", "Klee.png"].indexOf(fileName) != -1) {
                                         return "Pyro"
                                     } else if (["Diona.png", "Chongyun.png", "Kaeya.png", "Ganyu.png", "Qiqi.png"].indexOf(fileName) != -1) {
                                         return "Cryo"
                                     } else if (["Keqing.png", "Beidou.png", "Lisa.png", "Fischl.png", "Razor.png"].indexOf(fileName) != -1) {
                                         return "Electro"
                                     } else if (["Tartaglia.png", "Xingqiu.png", "Mona.png", "Barbara.png"].indexOf(fileName) != -1) {
                                         return "Hydro"
                                     }
                        visible: if (folderModel.type == "All") {
                                    return 60
                                }
                                else {
                                    if (folderModel.type == charElement) {
                                        return 60
                                    } else {
                                        flick.contentY = 0
                                        return 0
                                    }
                                }
                    }
                }
            }
        }

        LinearGradient {
            id: mask
            anchors.fill: opacityBox
            gradient: Gradient {
                GradientStop {
                    position: 0
                    color: "white"
                }
                GradientStop {
                    position: 0.05
                    color: "transparent"
                }

                GradientStop {
                    position: 0.95
                    color: "transparent"
                }
                GradientStop {
                    position: 1
                    color: "white"
                }
            }
            visible: false
        }

        OpacityMask {
            anchors.fill: parent
            source: opacityBox
            maskSource: mask
        }
    }
    Connections {
        target: backend
    }
}

