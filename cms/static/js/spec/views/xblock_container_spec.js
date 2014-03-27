define([ "jquery", "js/spec/create_sinon", "URI", "js/views/xblock_container", "js/models/xblock_info",
    "xmodule", "coffee/src/main", "xblock/cms.runtime.v1"],
    function ($, create_sinon, URI, XBlockContainerView, XBlockInfo) {

        describe("XBlockContainerView", function() {
            var model, containerView, respondWithMockXBlockEditorFragment, mockContainerView,
                editXBlockModalTemplate, editorModeButtonTemplate, feedbackTemplate;

            mockContainerView = readFixtures('mock/mock-container-view.underscore');
            editXBlockModalTemplate = readFixtures('edit-xblock-modal.underscore');
            editorModeButtonTemplate = readFixtures('editor-mode-button.underscore');
            feedbackTemplate = readFixtures('system-feedback.underscore');

            beforeEach(function () {
                setFixtures(mockContainerView);
                appendSetFixtures($("<script>", { id: "edit-xblock-modal-tpl", type: "text/template" }).text(editXBlockModalTemplate));
                appendSetFixtures($("<script>", { id: "editor-mode-button-tpl", type: "text/template" }).text(editorModeButtonTemplate));
                appendSetFixtures($("<script>", { id: "system-feedback-tpl", type: "text/template" }).text(feedbackTemplate));

                model = new XBlockInfo({
                    id: 'testCourse/branch/published/block/verticalFFF',
                    display_name: 'Test Unit',
                    category: 'vertical'
                });
                containerView = new XBlockContainerView({
                    model: model,
                    el: $('#content')
                });
            });

            respondWithMockXBlockEditorFragment = function(requests, response) {
                var requestIndex = requests.length - 1;
                create_sinon.respondWithJson(requests, response, requestIndex);
            };

            describe("Editing an xblock", function() {
                var mockContainerXBlockHtml;

                beforeEach(function () {
                    window.MockXBlock = function(runtime, element) {
                        return { };
                    };
                });

                afterEach(function() {
                    window.MockXBlock = null;
                });

                mockContainerXBlockHtml = readFixtures('mock/mock-container-xblock.underscore');

                it('can render itself', function() {
                    var requests = create_sinon.requests(this);
                    containerView.render();
                    respondWithMockXBlockEditorFragment(requests, {
                        html: mockContainerXBlockHtml,
                        "resources": []
                    });

                    expect(containerView.$el.select('.xblock-header')).toBeTruthy();
                });


                it('can show an edit modal for a child xblock', function() {
                    var requests = create_sinon.requests(this),
                        editButtons;
                    containerView.render();
                    respondWithMockXBlockEditorFragment(requests, {
                        html: mockContainerXBlockHtml,
                        "resources": []
                    });
                    editButtons = containerView.$('.edit-button');
                    expect(editButtons.length).toBe(3);
                });
            });
        });
    });
