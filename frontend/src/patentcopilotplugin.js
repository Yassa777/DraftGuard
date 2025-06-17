import { Plugin } from 'ckeditor5/src/core';
import { ButtonView } from 'ckeditor5/src/ui';
import copilotIcon from './icons/copilot.svg';

export default class PatentCopilotPlugin extends Plugin {
    static get pluginName() {
        return 'PatentCopilotPlugin';
    }

    init() {
        const editor = this.editor;

        editor.ui.componentFactory.add('patentCopilot', locale => {
            const view = new ButtonView(locale);

            view.set({
                label: 'Patent Copilot',
                icon: copilotIcon,
                tooltip: true
            });

            // Callback executed once the button is clicked.
            view.on('execute', () => {
                console.log('Patent Copilot button clicked!');
                // Here we will trigger the AI suggestion logic.
            });

            return view;
        });
    }
}
