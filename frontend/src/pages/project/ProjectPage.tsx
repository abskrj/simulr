import { ReflexContainer, ReflexSplitter, ReflexElement } from 'react-reflex';
import 'react-reflex/styles.css';
import { ProjectHeader } from './components/ProjectHeader';
import { ChatPanel } from './components/ChatPanel';
import { CanvasPanel } from './components/CanvasPanel';
import { CodeEditorPanel } from './components/CodeEditorPanel';
import { Box } from '@radix-ui/themes';

const ProjectPage = () => {
    return (
        <Box style={{ display: 'flex', flexDirection: 'column', height: '100%' }}>
            <ProjectHeader />
            <ReflexContainer orientation="vertical">
                <ReflexElement className="left-pane" minSize={200}>
                    <ReflexContainer orientation="horizontal">
                        <ReflexElement className="canvas-pane" minSize={100}>
                            <CanvasPanel />
                        </ReflexElement>

                        <ReflexSplitter />

                        <ReflexElement className="editor-pane" minSize={100}>
                            <CodeEditorPanel />
                        </ReflexElement>
                    </ReflexContainer>
                </ReflexElement>

                <ReflexSplitter />

                <ReflexElement className="right-pane" minSize={370}>
                    <ChatPanel />
                </ReflexElement>
            </ReflexContainer>
        </Box>
    );
};

export default ProjectPage;
