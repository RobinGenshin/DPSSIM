import QtQuick 2.15
import QtQuick.Controls 2.15
import QtGraphicalEffects 1.15
import "../images"
import "../fonts"

RadioDelegate {
    id: control
    width: initialWidth
    height: initialHeight
    checked: true
    state: if (control.checked == true) "active"; else "inactive"
    property string textUpper: "Team DPS"
    property color initialColor: "#979898"
    property int initialWidth: 140
    property int initialHeight: 85
    property int lowerFontSize: 20
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
        color: "#1a1b1e"
        radius: 10
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
            id: textUpperID
            y: 8
            width: 122
            height: 37
            rightPadding: control.indicator.width + control.spacing
            opacity: enabled ? 1.0 : 0.3
            color: "#979898"
            text: control.textUpper
            elide: Text.ElideRight
            anchors.left: parent.left
            anchors.bottom: parent.bottom
            verticalAlignment: Text.AlignVCenter
            font.pointSize: 10
            font.family: "Open Sans"
            style: Text.Normal
            anchors.bottomMargin: 40
            anchors.leftMargin: 15
        }

        Text {
            id: textLower
            rightPadding: control.indicator.width + control.spacing
            opacity: enabled ? 1.0 : 0.3
            color: control.initialColor
            text: if (control.checked == true) "On"; else "Off"
            elide: Text.ElideRight
            anchors.verticalCenter: parent.verticalCenter
            anchors.left: parent.left
            verticalAlignment: Text.AlignVCenter
            anchors.verticalCenterOffset: 10
            font.pointSize: lowerFontSize
            font.family: "Open Sans"
            anchors.leftMargin: 15
        }
    }

}
