import QtQuick 2.15
import QtGraphicalEffects 1.15
import QtQuick.Controls 2.15

Item {
    Connections {
        target: backend

        function onSetCharUiImages(img_list) {
            var x = slot*6
            image1.source = img_list[x]
            character = img_list[x].replace(".png","").replace("../images/chars/","")
//            constellation = img_list[x+2]
            weaponImage.source = img_list[x+3]
            weapon = img_list[x+3].replace(".png","").replace("../images/weapons/","").replace("_"," ")
            refinement = img_list[x+4]
            artifact = img_list[x+5].replace(".png","").replace("../images/artifacts/","").replace("_"," ")
            artifactImage.source = img_list[x+5]
        }
    }

    z: 0
    width: 140
    height: 140
    id: characterUIID
    property int slot: 0
    property bool characterChosen: if (image1.source != "") true; else false
    property string character: ""
    property string weapon: ""
    property string artifact: ""
    property string constellation: constellationTextArea.text
    property string level: levelTextArea.text
    property string refinement: ""
    property bool ready: if(character != "" && weapon != "" && artifact != "" && level != "" && level != "0") true; else false
    property bool complete: if (character != "" && (weapon == "" || artifact == "" || level == "")) false; else true
    state: if (characterChosen == true) "full"; else "character"
    transitions: [
        Transition {
            from: "full"
            to: "character"
            PropertyAnimation {
                target: characterSquare
                properties: "width,height"
                to: 140
                duration: 450
            }
            PropertyAnimation {
                targets: [weaponSquare, artifactSquare]
                property: "y"
                from: 100
                to: 140
                duration: 450
                easing.type: Easing.InQuad
            }
            PropertyAnimation {
                targets: [levelSquare, constellationSquare]
                property: "x"
                from: 100
                to: 140
                duration: 450
                easing.type: Easing.InQuad
            }
            PropertyAnimation {
                targets: [weaponSquare, artifactSquare, levelSquare, constellationSquare]
                property: "opacity"
                from: 1
                to: 0
                duration: 450
            }
        },

        Transition {
            id: startAnimation
            from: "character"
            to: "full"
            SequentialAnimation {

                PauseAnimation {
                    duration: 200
                }

                ParallelAnimation {
                    PropertyAnimation {
                        target: characterSquare
                        properties: "width,height"
                        to: 90
                        duration: 300
                    }
                    PropertyAnimation {
                        targets: [weaponSquare, artifactSquare]
                        property: "y"
                        from: 140
                        to: 100
                        duration: 300
                        easing.type: Easing.OutQuad
                    }
                    PropertyAnimation {
                        targets: [levelSquare, constellationSquare]
                        property: "x"
                        from: 140
                        to: 100
                        duration: 300
                        easing.type: Easing.InQuad
                    }
                    PropertyAnimation {
                        targets: [weaponSquare, artifactSquare, levelSquare, constellationSquare]
                        property: "opacity"
                        from: 0
                        to: 1
                        duration: 300
                    }
                }
            }
        }
    ]

    Rectangle {
        id: characterSquare
        height: 140
        visible: true
        width: 140
        color: "#1a1b1e"
        radius: 10
        z: 1

        Image {
            id: image1
            anchors.fill: characterSquare
            source: ""
            mipmap: true
            fillMode: Image.PreserveAspectFit
            anchors.rightMargin: if (character == "") 10; else 4
            anchors.leftMargin: if (character == "") 10; else 4
            anchors.bottomMargin: if (character == "") 10; else 4
            anchors.topMargin: if (character == "") 10; else 4
            antialiasing: true

            ColorOverlay {
                id: overlay1
                visible: false
                source: image1
                anchors.fill: parent
                color: "#979898"
            }

            Label {
                id: label
                color: "#979898"
                text: if (image1.source == "") qsTr("+"); else ""
                anchors.fill: parent
                horizontalAlignment: Text.AlignHCenter
                verticalAlignment: Text.AlignVCenter
                font.weight: Font.Normal
                font.pointSize: 100
                font.family: "Open Sans"
            }
        }

        Button {
            anchors.fill: parent
            onClicked: rightMenu.activeMenu = "character"
            onDoubleClicked: {
                backend.add_character(character)
            }
            background: Rectangle {
                color: "#00000000"
            }
        }

    }

    Rectangle {
        id: weaponSquare
        y: 140
        height: 40
        opacity: 0
        width: 40
        color: "#1a1b1e"
        radius: 10
        z: 1

        Image {
            id: weaponImage
            anchors.fill: parent
            source: "../images/svg_images/sword_icon.svg"
            onSourceChanged: if (source == "") {
                                 source = "../images/svg_images/sword_icon.svg"
                             }
            mipmap: true
            antialiasing: true
            anchors.rightMargin: if (weapon == "") 10; else 2
            anchors.leftMargin: if (weapon == "") 10; else 2
            anchors.bottomMargin: if (weapon == "") 10; else 2
            anchors.topMargin: if (weapon == "") 10; else 2

            ColorOverlay {
                source: weaponImage
                anchors.fill: parent
                color: "#979898"
                visible: if (weapon == "") true; else false
            }
        }

        Button {
            id: weaponBtn
            anchors.fill: parent
            onClicked: {
                rightMenu.activeMenu = "weapon"
                rightMenu.activeSlot = slot
            }
            onDoubleClicked: {
                backend.add_weapon(weapon)
            }
            background: Rectangle {
                color: "#00000000"
            }
            ToolTip {
                parent: weaponImage
                visible: weaponBtn.hovered
                text: weapon
                font.family: "Open Sans"
            }
        }
    }

    Rectangle {
        id: artifactSquare
        x: 50
        y: 140
        height: 40
        opacity: 0
        width: 40
        color: "#1a1b1e"
        radius: 10
        z: 1

        Image {
            id: artifactImage
            anchors.fill: parent
            source: "../images/svg_images/hourglass-svgrepo-com (1).svg"
            onSourceChanged: if (source == "") {
                                 source = "../images/svg_images/hourglass-svgrepo-com (1).svg"
                             }
            mipmap: true
            antialiasing: true
            anchors.rightMargin: if (artifact == "") 10; else 2
            anchors.leftMargin: if (artifact == "") 10; else 2
            anchors.bottomMargin: if (artifact == "") 10; else 2
            anchors.topMargin: if (artifact == "") 10; else 2
        }
        ColorOverlay {
            source: artifactImage
            anchors.fill: artifactImage
            color: "#979898"
            visible: if (artifact == "") true; else false
        }

        Button {
            id: artifactBtn
            anchors.fill: parent
            onClicked: {
                rightMenu.activeMenu = "artifact"
                rightMenu.activeSlot = slot
            }
            onDoubleClicked: {
                backend.add_artifact(artifact)
            }
            background: Rectangle {
                color: "#00000000"
            }
            ToolTip {
                parent: artifactImage
                visible: artifactBtn.hovered
                text: artifact
                font.family: "Open Sans"
            }
        }

    }

    Rectangle {
        id: levelSquare
        x: 140
        y: 0
        height: 40
        opacity: 0
        width: 40
        color: "#1a1b1e"
        radius: 10
        z: 1

        Text {
            id: levelText
            font.family: "Open Sans"
            color: "#979898"
            text: if (levelTextArea.text == "") "Lv"; else ""
            anchors.fill: parent
            horizontalAlignment: Text.AlignHCenter
            verticalAlignment: Text.AlignVCenter
            minimumPointSize: 0
            minimumPixelSize: 0
            fontSizeMode: Text.VerticalFit
            font.bold: true
            font.pointSize: 15
        }

        TextArea {
            id: levelTextArea
            font.family: "Open Sans"
            color: "#979898"
            anchors.fill: parent
            font.bold: true
            font.pointSize: 15
            horizontalAlignment: Text.AlignHCenter
            verticalAlignment: Text.AlignVCenter
            placeholderText: ""
            text: ""
        }
    }

    DropShadow{
        opacity: 0.5
        visible: true
        anchors.fill: characterSquare
        horizontalOffset: 0
        verticalOffset: 0
        radius: 10
        samples: 16
        color: if (rightMenu.activeSlot == slot && (rightMenu.activeMenu == "weapon" || rightMenu.activeMenu == "artifact")) "#80FFFFFF" ;else "#80000000"
        source: characterSquare
        z: 0
    }

    Rectangle {
        id: constellationSquare
        x: 140
        y: 50
        width: 40
        height: 40
        opacity: 0
        color: "#1a1b1e"
        radius: 10
        z: 1

        Image {
            visible: if (constellationTextArea.text == "") true; else false
            id: constellationImage
            anchors.fill: parent
            source: "../images/svg_images/stars-svgrepo-com (1).svg"
            mipmap: true
            anchors.leftMargin: 8
            anchors.rightMargin: 8
            anchors.topMargin: 8
            anchors.bottomMargin: 8

            ColorOverlay {
                color: "#979898"
                anchors.fill: parent
                source: constellationImage
            }
        }
        TextArea {
            id: constellationTextArea
            font.family: "Open Sans"
            color: "#979898"
            anchors.fill: parent
            font.bold: true
            font.pointSize: 15
            horizontalAlignment: Text.AlignHCenter
            verticalAlignment: Text.AlignVCenter
            placeholderText: ""
            text: ""

            IntValidator {
                bottom: 0
                top: 6
            }
        }
    }


}


