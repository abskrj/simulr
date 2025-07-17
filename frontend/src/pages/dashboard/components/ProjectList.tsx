import { Card, Flex, Text } from "@radix-ui/themes";

export const ProjectList = () => {
    return (
        <Flex wrap="wrap" gap="4">
            {Array.from({ length: 6 }).map((_, i) => (
                <Card key={i} style={{ width: '300px' }}>
                    <Text as="div" size="3" weight="bold" mb="1">
                        Project {i + 1}
                    </Text>
                    <Text as="div" color="gray">
                        This is a short description of the project.
                    </Text>
                </Card>
            ))}
        </Flex>
    )
} 