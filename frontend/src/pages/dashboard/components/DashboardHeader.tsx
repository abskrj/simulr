import { Button, Flex, Text } from "@radix-ui/themes";
import { useNavigate } from "react-router";

export const DashboardHeader = () => {
    const navigate = useNavigate();

    const handleCreateProject = () => {
        navigate('/project/new');
    }
    return (
        <Flex justify="between" align="center" mb="5">
            <Text size="6" weight="bold">
                Projects
            </Text>
            <Button onClick={handleCreateProject}>Create Project</Button>
        </Flex>
    )
} 