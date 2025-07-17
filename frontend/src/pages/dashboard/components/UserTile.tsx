import { Avatar, Box, Flex, Text } from "@radix-ui/themes";

export const UserTile = () => {
    return (
        <Flex gap="3" align="center">
            <Avatar
                size="3"
                src="https://images.unsplash.com/photo-1502823403499-6ccfcf4fb453?&w=256&h=256&q=70&crop=focalpoint&fp-x=0.5&fp-y=0.3&fp-z=1&fit=crop"
                radius="full"
                fallback="T"
            />
            <Box>
                <Text as="div" size="2" weight="bold">
                    Teodros Girmay
                </Text>
                <Text as="div" size="2" color="gray">
                    teodros@example.com
                </Text>
            </Box>
        </Flex>
    )
} 