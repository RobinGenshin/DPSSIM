import QtQuick 2.15
import QtQuick.Controls 2.15
import QtGraphicalEffects 1.15
import Qt.labs.folderlistmodel 2.15
import QtQml.Models 2.3

Rectangle {
    id: artifactGrid
    x: 0
    color: "#00000000"
    radius: 10
    width: 240
    height: 480
    clip: false
    property bool active: if (parent.activeMenu === "artifact") true; else false
    state: if (active === true) "active"; else "inactive"

    transitions: [
        Transition {
            from: "active"
            to: "inactive"
            ParallelAnimation {
                id: closeMenu
                PropertyAnimation {
                    target: artifactGrid
                    property: "width"
                    duration: 500
                    easing.type: Easing.InOutQuad
                    to: 0
                }

                PropertyAnimation {
                    target: artifactGrid
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
                    target: artifactGrid
                    property: "width"
                    duration: 500
                    easing.type: Easing.InOutQuad
                    to: if(artifactGrid.width == 0) return 240; else return 0
                }

                PropertyAnimation {
                    target: artifactGrid
                    property: "opacity"
                    duration: 0
                    to: 0
                }

                SequentialAnimation {
                    PauseAnimation {
                        duration: 200
                    }

                    PropertyAnimation {
                        target: artifactGrid
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

        Text {
            width: 180
            color: "#ffffff"
            text: "Artifacts"
            anchors.left: parent.left
            anchors.top: parent.top
            anchors.bottom: parent.bottom
            horizontalAlignment: Text.AlignHCenter
            verticalAlignment: Text.AlignBottom
            font.pointSize: 12
            font.family: "Open Sans"
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
                        folder: "../images/artifacts"
                        nameFilters: ["*.png"]
                        property string type: "All"
                    }

                    delegate: SelectorButton {
                        objectName: "selectorButton"
                        btnIconSource: "../images/artifacts/" + fileName
                        onClicked: {
                            backend.add_artifact(fileName.replace(".png","").replace(/_/g," "), rightMenu.activeSlot)
                        }
                        charElement: ""
                        visible: true
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


