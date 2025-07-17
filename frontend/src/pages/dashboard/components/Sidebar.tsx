import { Box, Flex, Text } from "@radix-ui/themes";
import { UserTile } from "./UserTile";

export const Sidebar = () => {
    return (
        <Box
            style={{
                width: '280px',
                borderRight: '1px solid var(--gray-a5)',
                padding: 'var(--space-4)',
                flexShrink: 0,
            }}
        >
            <Flex direction="column" justify="between" height="100%">
                <Box>
                    <Text size="5" weight="bold" mb="4">
                        My Dashboard
                    </Text>
                    {/* Navigation items can go here */}
                    <Flex direction="column" gap="2">
                        <Text>Home</Text>
                        <Text>Analytics</Text>
                        <Text>Settings</Text>
                    </Flex>
                </Box>

                <UserTile />
            </Flex>
        </Box>
    )
} 