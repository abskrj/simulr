import type { Monaco } from '@monaco-editor/react';
import { language } from './glsl';
import { configuration } from './language-configuration';

export const GLSL_LANGUAGE_ID = 'glsl';

export function setupGLSL(monaco: Monaco) {
    monaco.languages.register({ id: GLSL_LANGUAGE_ID });
    monaco.languages.setMonarchTokensProvider(GLSL_LANGUAGE_ID, language);
    monaco.languages.setLanguageConfiguration(GLSL_LANGUAGE_ID, configuration);
} 