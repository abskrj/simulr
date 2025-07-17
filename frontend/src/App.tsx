import { RouterProvider } from 'react-router';
import routes from './routes';
import { Box } from '@radix-ui/themes';

function App() {
  return (
    <Box style={{ height: '100vh', width: '100vw' }}>
      <RouterProvider router={routes} />
    </Box>
  );
}

export default App;
