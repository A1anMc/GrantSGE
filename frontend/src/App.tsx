import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { CssBaseline, ThemeProvider } from '@mui/material';
import Layout from './components/Layout';
import theme from './theme';
import { textures } from './styles/tokens';

// Import pages here
import Dashboard from './pages/Dashboard';

function App() {
  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <div
        style={{
          background: `${theme.palette.background.default} ${textures.concrete}`,
          minHeight: '100vh',
        }}
      >
        <Router>
          <Layout>
            <Routes>
              <Route path="/" element={<Dashboard />} />
              {/* Add more routes here */}
            </Routes>
          </Layout>
        </Router>
      </div>
    </ThemeProvider>
  );
}

export default App;
