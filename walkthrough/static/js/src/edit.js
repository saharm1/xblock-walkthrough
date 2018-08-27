/* Javascript for editing walkthrough XBlock. */
function WalkthroughXBlockEdit(runtime, element) {

    var xmlEditorTextarea = $('.block-xml-editor', element),
        xmlEditor = CodeMirror.fromTextArea(xmlEditorTextarea[0], { mode: 'xml', lineWrapping: true });

    $(element).find('.action-cancel').bind('click', function() {
        runtime.notify('cancel', {});
    });

    $(element).find('.action-save').bind('click', function() {
        var data = {
            'button_label': $('#walkthrough_edit_button_label').val(),
            'intro': $('#walkthrough_edit_intro').val(),
            'steps': xmlEditor.getValue(),
        };
        runtime.notify('save', {state: 'start'});
        var handlerUrl = runtime.handlerUrl(element, 'studio_submit');
        $.post(handlerUrl, JSON.stringify(data)).done(function(response) {
            if (response.result === 'success') {
                runtime.notify('save', {state: 'end'});
                //Reload the page
                //window.location.reload(false);
            } else {
                runtime.notify('error', {msg: response.message})
            }
        });
    });
}
