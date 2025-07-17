import { Editor } from "@monaco-editor/react";
import type { Monaco } from "@monaco-editor/react";
import { GLSL_LANGUAGE_ID, setupGLSL } from "../../../monaco-glsl/setup";

export const CodeEditorPanel = () => {

    const handleEditorDidMount = (editor: any, monaco: Monaco) => {
        setupGLSL(monaco);
    }
    return (
        <div style={{ height: '100%', width: '100%' }}>
            <Editor
                height="100%"
                theme="vs-dark"
                options={{
                    minimap: {
                        enabled: false,
                    },
                }}
                language={GLSL_LANGUAGE_ID}
                value={`#version 430
void main() {
    gl_Position = vec4(0.0, 0.0, 0.0, 1.0);
}`}
                onMount={handleEditorDidMount}
                onChange={(value) => {
                    console.log(value);
                }}
            />
        </div>
    );
};
