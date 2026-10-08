import QtQuick 2.9
import MuseScore 3.0
import FileIO 3.0

MuseScore {
    id: root
    menuPath: "Plugins.MCP native smoke"
    requiresScore: true
    FileIO { id: report }
    onRun: {
        var result = {failures: []};
        report.source = Qt.resolvedUrl("native-smoke.json").toString().replace(/^file:\/\/\//, "");
        function stage(name) { result.stage = name; report.write(JSON.stringify(result, null, 2)); }
        function check(ok, message) { if (!ok) result.failures.push(message); }
        try {
            var component = Qt.createComponent("__PLUGIN_URL__");
            if (component.status !== Component.Ready) throw new Error(component.errorString());
            var panel = component.createObject(root);
            if (!panel) throw new Error(component.errorString());
            panel.run();
            stage("started");
            result.capabilities = panel.processCommand({action:"getCapabilities",params:{}});
            var cursor = curScore.newCursor(); cursor.rewind(0);
            while (cursor.element && cursor.element.name !== "Chord" && cursor.next()) {}
            var selected = cursor.element && cursor.element.name === "Chord" ? cursor.element.notes[0] : cursor.element;
            if (!selected) throw new Error("Fixture has no selectable element");
            curScore.selection.select(selected);
            var before = curScore.selection.elements.length;
            var data = panel.processCommand({action:"getScore",params:{}});
            check(data.success && data.analysis.numMeasures > 0, "structured read failed");
            check(curScore.selection.elements.length === before && curScore.selection.elements[0].is(selected), "read changed selection");
            result.analysis = data.analysis;
            stage("read");
            var range = panel.processCommand({action:"selectCustomRange",params:{startTick:0,endTick:480,startStaff:0,endStaff:0}});
            check(range.success && curScore.selection.isRange && curScore.selection.endStaff === 1, "single staff range failed");
            stage("range");
            var tempo = panel.processCommand({action:"setTempo",params:{bpm:88}});
            check(tempo.success, "native tempo failed");
            var tempoCursor = curScore.newCursor(); tempoCursor.rewindToTick(0);
            check(Math.abs(tempoCursor.tempo * 60 - 88) < 0.001, "tempo map did not update");
            stage("tempo");
            panel.goToBeginningOfScore();
            var note = panel.addNote({pitch:60,duration:{numerator:1,denominator:4},advanceCursorAfterAction:true});
            check(note.success, "native note insertion failed");
            var noteCursor = curScore.newCursor(); noteCursor.rewindToTick(0);
            check(noteCursor.element.name === "Chord" && noteCursor.element.notes[0].pitch === 60, "inserted note did not match");
            stage("note");
            var measures = curScore.nmeasures;
            var batch = panel.processCommand({action:"processSequence",params:{sequence:[
                {action:"appendMeasure",params:{count:1}},
                {action:"goToMeasure",params:{measure:9999}},
                {action:"appendMeasure",params:{count:1}}
            ]}});
            check(batch.failedIndex === 1 && batch.completedCount === 1, "batch did not stop on failure");
            check(curScore.nmeasures === measures + 1, "batch applied actions after failure");
            stage("batch");
            panel.undo();
            check(curScore.nmeasures === measures, "native undo failed");
            stage("undo");
            panel.destroy();
        } catch(error) { result.failures.push(String(error)); }
        report.source = Qt.resolvedUrl("native-smoke.json").toString().replace(/^file:\/\/\//, "");
        report.write(JSON.stringify(result, null, 2));
        console.log("MCP_NATIVE_SMOKE " + JSON.stringify(result));
    }
}
