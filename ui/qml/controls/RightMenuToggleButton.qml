import QtQuick 2.15
import QtQuick.Controls 2.15
import QtGraphicalEffects 1.15
import "../images"
import "../fonts"

RadioDelegate {
    id: control
    width: initialWidth
    height: initialHeight
    checked: false
    state: if (control.checked == true) "active"; else "inactive"
    onClicked: {
        buttonOpacity: 1
        console.log("Hi")
    }

    property color bgColor: "#1a1b1e"
    property string buttonText: ""
    property color initialColor: "#979898"
    property int initialWidth: 60
    property int initialHeight: 40
    property int lowerFontSize: 10
    property real buttonOpacity: 0.25
    transitions: [
        Transition {
            from: "active"
            to: "inactive"
            PropertyAnimation {
                target: textLower
                properties: "color"
                to: "#979898"
                duration: 250
            }
            PropertyAnimation {
                target: bg
                property: "opacity"
                to: 0.25
                duration: 250
            }
        },
        Transition {
            from: "inactive"
            to: "active"
            PropertyAnimation {
                target: textLower
                properties: "color"
                to: "#ffffff"
                duration: 250
            }
            PropertyAnimation {
                target: bg
                property: "opacity"
                to: 1
                duration: 250
            }
        }
    ]

    indicator: Rectangle {
        implicitWidth: 0
        implicitHeight: 0
        visible: false
        color: "#00000000"
    }

    background: Rectangle {
        id: bg
        visible: true
        color: bgColor
        opacity: buttonOpacity
        radius: 5
        anchors.fill: parent
        z: 1

        DropShadow{
            opacity: 0.5
            visible: true
            anchors.fill: bg
            horizontalOffset: 1
            verticalOffset: 1
            radius: 10
            samples: 16
            color: "#80000000"
            source: bg
            z: -1
        }

        Text {
            id: textLower
            opacity: enabled ? 1.0 : 0.3
            color: control.initialColor
            text: buttonText
            elide: Text.ElideRight
            anchors.verticalCenter: parent.verticalCenter
            horizontalAlignment: Text.AlignHCenter
            verticalAlignment: Text.AlignVCenter
            rightPadding: 0
            anchors.horizontalCenter: parent.horizontalCenter
            font.pointSize: lowerFontSize
            font.family: "Open Sans"
        }
    }

}
