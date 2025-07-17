import { Button, Flex, Heading, IconButton, TextField } from '@radix-ui/themes';
import { ArrowLeftIcon, CheckIcon } from '@radix-ui/react-icons';
import React from 'react';

export const ProjectHeader = () => {
    const [projectName, setProjectName] = React.useState('My GLSL Project');
    return (
        <Flex align="center" justify="between" p="3" style={{ borderBottom: '1px solid var(--gray-a5)' }}>
            <Flex align="center" gap="3">
                <IconButton>
                    <ArrowLeftIcon width="18" height="18" />
                </IconButton>
                <Heading>
                    <TextField.Root
                        value={projectName}
                        onChange={(e) => setProjectName(e.target.value)}
                        size="3"
                        variant="soft"
                    />
                </Heading>
            </Flex>

            <Button>
                <CheckIcon width="16" height="16" /> Save
            </Button>
        </Flex>
    );
};
