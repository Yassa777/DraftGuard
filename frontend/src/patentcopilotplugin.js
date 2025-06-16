import { Plugin } from 'ckeditor5/src/core';

export default class PatentCopilotPlugin extends Plugin {
    static get pluginName() {
        return 'PatentCopilotPlugin';
    }

    init() {
        console.log('PatentCopilotPlugin was initialized.');
    }
}
