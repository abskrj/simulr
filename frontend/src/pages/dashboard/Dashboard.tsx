import { Box, Flex } from '@radix-ui/themes';
import { DashboardHeader } from './components/DashboardHeader';
import { ProjectList } from './components/ProjectList';
import { Sidebar } from './components/Sidebar';

function Dashboard() {
  return (
    <Flex height="100vh">
      <Sidebar />
      {/* Main Content */}
      <Box style={{ flexGrow: 1, padding: 'var(--space-5)', overflow: 'auto' }}>
        <DashboardHeader />
        <ProjectList />
      </Box>
    </Flex>
  );
}

export default Dashboard;
