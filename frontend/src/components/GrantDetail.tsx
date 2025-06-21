import React, { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import {
  Box,
  Button,
  Card,
  CardContent,
  Chip,
  CircularProgress,
  Container,
  Divider,
  Grid,
  IconButton,
  LinearProgress,
  Paper,
  Typography,
  Alert,
} from '@mui/material';
import {
  ArrowBack as ArrowBackIcon,
  Launch as LaunchIcon,
  AccessTime as AccessTimeIcon,
  AttachMoney as AttachMoneyIcon,
  Analytics as AnalyticsIcon,
} from '@mui/icons-material';
import { colors, transitions } from '../styles/tokens';

interface Grant {
  id: number;
  name: string;
  funder: string;
  source_url: string;
  due_date: string;
  amount_string: string;
  description: string;
  status: 'urgent' | 'eligible' | 'potential';
  eligibility_analysis: {
    score: number;
    criteria: Array<{
      name: string;
      met: boolean;
      description: string;
    }>;
    summary: string;
  } | null;
}

const GrantDetail: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const [grant, setGrant] = useState<Grant | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [analyzing, setAnalyzing] = useState(false);

  useEffect(() => {
    const fetchGrantDetails = async () => {
      try {
        setLoading(true);
        const response = await fetch(`/api/grants/${id}`);
        if (!response.ok) {
          throw new Error('Failed to fetch grant details');
        }
        const data = await response.json();
        setGrant(data.data);
      } catch (err) {
        setError(err instanceof Error ? err.message : 'An error occurred');
      } finally {
        setLoading(false);
      }
    };

    fetchGrantDetails();
  }, [id]);

  const handleRunEligibilityScan = async () => {
    try {
      setAnalyzing(true);
      const response = await fetch(`/api/grants/${id}/analyze-eligibility`, {
        method: 'POST',
      });
      if (!response.ok) {
        throw new Error('Failed to analyze eligibility');
      }
      const data = await response.json();
      setGrant(prev => prev ? { ...prev, eligibility_analysis: data.analysis } : null);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to analyze eligibility');
    } finally {
      setAnalyzing(false);
    }
  };

  if (loading) {
    return (
      <Box sx={{ display: 'flex', justifyContent: 'center', py: 8 }}>
        <CircularProgress />
      </Box>
    );
  }

  if (error || !grant) {
    return (
      <Container maxWidth="lg" sx={{ py: 4 }}>
        <Alert severity="error" sx={{ mb: 3 }}>
          {error || 'Grant not found'}
        </Alert>
        <Button
          startIcon={<ArrowBackIcon />}
          onClick={() => navigate(-1)}
        >
          Back to Grants
        </Button>
      </Container>
    );
  }

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'urgent':
        return colors.urgent;
      case 'eligible':
        return colors.eligible;
      default:
        return colors.gray400;
    }
  };

  return (
    <Container maxWidth="lg" sx={{ py: 4 }}>
      {/* Header */}
      <Box sx={{ mb: 4, display: 'flex', alignItems: 'flex-start', justifyContent: 'space-between' }}>
        <Box>
          <Button
            startIcon={<ArrowBackIcon />}
            onClick={() => navigate(-1)}
            sx={{ mb: 2 }}
          >
            Back to Grants
          </Button>
          <Typography variant="h3" component="h1" sx={{ mb: 1 }}>
            {grant.name}
          </Typography>
          <Typography variant="h5" color="text.secondary" sx={{ mb: 2 }}>
            {grant.funder}
          </Typography>
          <Box sx={{ display: 'flex', gap: 1, flexWrap: 'wrap' }}>
            <Chip
              label={grant.status.toUpperCase()}
              sx={{
                backgroundColor: getStatusColor(grant.status),
                color: 'white',
              }}
            />
            <Chip
              icon={<AccessTimeIcon />}
              label={new Date(grant.due_date).toLocaleDateString()}
            />
            <Chip
              icon={<AttachMoneyIcon />}
              label={grant.amount_string}
            />
          </Box>
        </Box>
        {grant.source_url && (
          <IconButton
            href={grant.source_url}
            target="_blank"
            rel="noopener noreferrer"
            sx={{ ml: 2 }}
          >
            <LaunchIcon />
          </IconButton>
        )}
      </Box>

      <Grid container spacing={4}>
        {/* Main Content */}
        <Grid item xs={12} md={8}>
          <Card sx={{ mb: 4 }}>
            <CardContent>
              <Typography variant="h6" sx={{ mb: 2 }}>
                Description
              </Typography>
              <Typography variant="body1" sx={{ whiteSpace: 'pre-wrap' }}>
                {grant.description}
              </Typography>
            </CardContent>
          </Card>
        </Grid>

        {/* Eligibility Analysis */}
        <Grid item xs={12} md={4}>
          <Paper sx={{ p: 3, mb: 4 }}>
            <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
              <AnalyticsIcon sx={{ mr: 1 }} />
              <Typography variant="h6">
                Eligibility Analysis
              </Typography>
            </Box>
            
            {analyzing ? (
              <Box sx={{ textAlign: 'center', py: 4 }}>
                <CircularProgress size={24} sx={{ mb: 2 }} />
                <Typography>Analyzing eligibility...</Typography>
              </Box>
            ) : grant.eligibility_analysis ? (
              <>
                <Box sx={{ mb: 3 }}>
                  <Typography variant="body2" color="text.secondary" sx={{ mb: 1 }}>
                    Match Score
                  </Typography>
                  <LinearProgress
                    variant="determinate"
                    value={grant.eligibility_analysis.score * 100}
                    sx={{
                      height: 8,
                      borderRadius: 4,
                      backgroundColor: colors.gray200,
                      '& .MuiLinearProgress-bar': {
                        backgroundColor: colors.eligible,
                      },
                    }}
                  />
                  <Typography variant="h4" sx={{ mt: 1 }}>
                    {Math.round(grant.eligibility_analysis.score * 100)}%
                  </Typography>
                </Box>

                <Divider sx={{ my: 2 }} />

                <Typography variant="body2" sx={{ mb: 2 }}>
                  {grant.eligibility_analysis.summary}
                </Typography>

                <Typography variant="subtitle2" sx={{ mb: 2 }}>
                  Criteria Analysis:
                </Typography>
                {grant.eligibility_analysis.criteria.map((criterion, index) => (
                  <Box key={index} sx={{ mb: 2 }}>
                    <Box sx={{ display: 'flex', alignItems: 'center', mb: 1 }}>
                      <Chip
                        label={criterion.met ? 'Met' : 'Not Met'}
                        size="small"
                        sx={{
                          backgroundColor: criterion.met ? colors.eligible : colors.urgent,
                          color: 'white',
                          mr: 1,
                        }}
                      />
                      <Typography variant="body2" fontWeight="medium">
                        {criterion.name}
                      </Typography>
                    </Box>
                    <Typography variant="body2" color="text.secondary">
                      {criterion.description}
                    </Typography>
                  </Box>
                ))}
              </>
            ) : (
              <Box sx={{ textAlign: 'center', py: 4 }}>
                <Button
                  variant="contained"
                  onClick={handleRunEligibilityScan}
                  startIcon={<AnalyticsIcon />}
                >
                  Run Smart Eligibility Scan
                </Button>
              </Box>
            )}
          </Paper>
        </Grid>
      </Grid>
    </Container>
  );
};

export default GrantDetail; 