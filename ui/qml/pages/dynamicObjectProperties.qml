import QtQuick 2.15

Item {
   id: container
   width: 500
   height: 200
   property bool caller:false //This property is visible in the dynamic object
   property string test:"import QtQuick 1.1;
       Rectangle {
           id:abc;
           color:\"red\";
           width: 40;
           height: 20;
           x:100;
           y:50
           Component.onCompleted: {
               caller = true;
               console.log('New value to the property caller was assigned')
           }
       }"
   Rectangle {
       id:second
       width:50
       height:50
       x:70
       color:'green'
       Component.onCompleted: {
           var dynamicObject = Qt.createQmlObject(test, container, 'firstObject');
           console.log("The value of caller was changed in the dynamic object")
       }
   } //end second
}
