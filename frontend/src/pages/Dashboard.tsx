import React, { useState } from 'react';
import {
  Container,
  Typography,
  Box,
  Tabs,
  Tab,
} from '@mui/material';
import GrantList from '../components/GrantList';

const Dashboard: React.FC = () => {
  const [tabValue, setTabValue] = useState(0);

  const handleTabChange = (event: React.SyntheticEvent, newValue: number) => {
    setTabValue(newValue);
  };

  // Map tab index to status
  const getStatusFromTab = (tabIndex: number): string => {
    switch (tabIndex) {
      case 1:
        return 'eligible';
      case 2:
        return 'urgent';
      case 3:
        return 'tracked';
      default:
        return 'all';
    }
  };

  return (
    <Container maxWidth="lg" sx={{ py: 4 }}>
      {/* Header Section */}
      <Box sx={{ mb: 6 }}>
        <Typography variant="h2" component="h1" sx={{ mb: 2 }}>
          Grant Dashboard
        </Typography>
        <Typography variant="body1" color="text.secondary" sx={{ mb: 4 }}>
          Track and manage grant opportunities that align with your organization's mission.
        </Typography>

        {/* Tabs */}
        <Tabs
          value={tabValue}
          onChange={handleTabChange}
          sx={{
            mb: 4,
            '& .MuiTab-root': {
              textTransform: 'none',
              fontSize: '1rem',
            },
          }}
        >
          <Tab label="All Grants" />
          <Tab label="Eligible" />
          <Tab label="Urgent" />
          <Tab label="Tracked" />
        </Tabs>
      </Box>

      {/* Grant List */}
      <GrantList initialStatus={getStatusFromTab(tabValue)} />
    </Container>
  );
};

export default Dashboard; 