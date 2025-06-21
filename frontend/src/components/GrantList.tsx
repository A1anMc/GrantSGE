import React, { useEffect, useState } from 'react';
import {
  Grid,
  Box,
  TextField,
  InputAdornment,
  CircularProgress,
  Alert,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  Stack,
  Typography,
  Collapse,
  IconButton,
  Button,
  Slider,
  Fade,
} from '@mui/material';
import { AdapterDateFns } from '@mui/x-date-pickers/AdapterDateFns';
import { LocalizationProvider, DatePicker } from '@mui/x-date-pickers';
import SearchIcon from '@mui/icons-material/Search';
import FilterListIcon from '@mui/icons-material/FilterList';
import ExpandMoreIcon from '@mui/icons-material/ExpandMore';
import ExpandLessIcon from '@mui/icons-material/ExpandLess';
import SortIcon from '@mui/icons-material/Sort';
import { useNavigate } from 'react-router-dom';
import { motion, AnimatePresence } from 'framer-motion';
import GrantCard from './GrantCard';
import { colors, transitions } from '../styles/tokens';

interface Grant {
  id: number;
  name: string;
  funder: string;
  due_date: string;
  amount_string: string;
  amount_number: number;
  status: 'urgent' | 'eligible' | 'potential';
  description?: string;
  eligibility_analysis?: any;
  source_url?: string;
}

interface GrantListProps {
  initialStatus?: string;
}

interface Filters {
  nameQuery: string;
  funderQuery: string;
  status: string;
  sortBy: string;
  sortDirection: 'asc' | 'desc';
  startDate: Date | null;
  endDate: Date | null;
  minAmount: number;
  maxAmount: number;
  page: number;
  perPage: number;
}

const ITEMS_PER_PAGE = 12;

const GrantList: React.FC<GrantListProps> = ({ initialStatus = 'all' }) => {
  const navigate = useNavigate();
  const [showAdvancedFilters, setShowAdvancedFilters] = useState(false);
  const [grants, setGrants] = useState<Grant[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [totalGrants, setTotalGrants] = useState(0);
  const [amountRange, setAmountRange] = useState<[number, number]>([0, 1000000]);
  
  const [filters, setFilters] = useState<Filters>({
    nameQuery: '',
    funderQuery: '',
    status: initialStatus,
    sortBy: 'due_date',
    sortDirection: 'asc',
    startDate: null,
    endDate: null,
    minAmount: 0,
    maxAmount: 1000000,
    page: 1,
    perPage: ITEMS_PER_PAGE,
  });

  // Fetch grants from API
  useEffect(() => {
    const fetchGrants = async () => {
      try {
        setLoading(true);
        const queryParams = new URLSearchParams();
        
        // Basic filters
        if (filters.status !== 'all') {
          queryParams.append('status', filters.status);
        }
        if (filters.nameQuery) {
          queryParams.append('name', filters.nameQuery);
        }
        if (filters.funderQuery) {
          queryParams.append('funder', filters.funderQuery);
        }

        // Advanced filters
        if (filters.startDate) {
          queryParams.append('start_date', filters.startDate.toISOString());
        }
        if (filters.endDate) {
          queryParams.append('end_date', filters.endDate.toISOString());
        }
        if (filters.minAmount > 0) {
          queryParams.append('min_amount', filters.minAmount.toString());
        }
        if (filters.maxAmount < 1000000) {
          queryParams.append('max_amount', filters.maxAmount.toString());
        }

        // Sorting and pagination
        queryParams.append('sort', filters.sortBy);
        queryParams.append('direction', filters.sortDirection);
        queryParams.append('page', filters.page.toString());
        queryParams.append('per_page', filters.perPage.toString());

        const response = await fetch(`/api/grants?${queryParams.toString()}`);
        if (!response.ok) {
          throw new Error('Failed to fetch grants');
        }
        
        const data = await response.json();
        setGrants(data.data);
        setTotalGrants(data.total);
        setError(null);
      } catch (err) {
        setError(err instanceof Error ? err.message : 'An error occurred');
      } finally {
        setLoading(false);
      }
    };

    fetchGrants();
  }, [filters]);

  // Handle filter changes
  const handleFilterChange = (field: keyof Filters) => (
    event: React.ChangeEvent<HTMLInputElement | { value: unknown }> | null | [number, number]
  ) => {
    setFilters(prev => {
      const newFilters = { ...prev };
      
      if (Array.isArray(event)) {
        // Handle amount range slider
        newFilters.minAmount = event[0];
        newFilters.maxAmount = event[1];
      } else if (event === null) {
        // Handle date picker null case
        newFilters[field as 'startDate' | 'endDate'] = null;
      } else if (event instanceof Date) {
        // Handle date picker date case
        newFilters[field as 'startDate' | 'endDate'] = event;
      } else {
        // Handle regular input changes
        newFilters[field as keyof Filters] = event.target.value as never;
      }

      // Reset to page 1 when filters change
      if (field !== 'page') {
        newFilters.page = 1;
      }

      return newFilters;
    });
  };

  const handleSortChange = (newSortBy: string) => {
    setFilters(prev => ({
      ...prev,
      sortBy: newSortBy,
      sortDirection: prev.sortBy === newSortBy && prev.sortDirection === 'asc' ? 'desc' : 'asc',
      page: 1,
    }));
  };

  const handleGrantClick = (grantId: number) => {
    navigate(`/grants/${grantId}`);
  };

  const totalPages = Math.ceil(totalGrants / filters.perPage);

  return (
    <LocalizationProvider dateAdapter={AdapterDateFns}>
      <Box>
        {/* Filters Section */}
        <Stack spacing={3} sx={{ mb: 4 }}>
          <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
            <Typography variant="h6" color="text.secondary">
              Filter Grants
            </Typography>
            <Button
              startIcon={showAdvancedFilters ? <ExpandLessIcon /> : <ExpandMoreIcon />}
              onClick={() => setShowAdvancedFilters(!showAdvancedFilters)}
            >
              Advanced Filters
            </Button>
          </Box>
          
          <Grid container spacing={2}>
            <Grid item xs={12} md={4}>
              <TextField
                fullWidth
                label="Search by Name"
                value={filters.nameQuery}
                onChange={handleFilterChange('nameQuery')}
                InputProps={{
                  startAdornment: (
                    <InputAdornment position="start">
                      <SearchIcon />
                    </InputAdornment>
                  ),
                }}
                sx={{ backgroundColor: 'background.paper' }}
              />
            </Grid>
            
            <Grid item xs={12} md={4}>
              <TextField
                fullWidth
                label="Search by Funder"
                value={filters.funderQuery}
                onChange={handleFilterChange('funderQuery')}
                InputProps={{
                  startAdornment: (
                    <InputAdornment position="start">
                      <FilterListIcon />
                    </InputAdornment>
                  ),
                }}
                sx={{ backgroundColor: 'background.paper' }}
              />
            </Grid>
            
            <Grid item xs={12} md={4}>
              <FormControl fullWidth sx={{ backgroundColor: 'background.paper' }}>
                <InputLabel>Status</InputLabel>
                <Select
                  value={filters.status}
                  label="Status"
                  onChange={handleFilterChange('status')}
                >
                  <MenuItem value="all">All Grants</MenuItem>
                  <MenuItem value="urgent">Urgent</MenuItem>
                  <MenuItem value="eligible">Eligible</MenuItem>
                  <MenuItem value="potential">Potential</MenuItem>
                </Select>
              </FormControl>
            </Grid>
          </Grid>

          <Collapse in={showAdvancedFilters}>
            <Grid container spacing={2} sx={{ mt: 1 }}>
              <Grid item xs={12} md={6}>
                <DatePicker
                  label="Start Date"
                  value={filters.startDate}
                  onChange={(date) => handleFilterChange('startDate')(date)}
                  sx={{ width: '100%' }}
                />
              </Grid>
              <Grid item xs={12} md={6}>
                <DatePicker
                  label="End Date"
                  value={filters.endDate}
                  onChange={(date) => handleFilterChange('endDate')(date)}
                  sx={{ width: '100%' }}
                />
              </Grid>
              <Grid item xs={12}>
                <Typography gutterBottom>
                  Amount Range: ${amountRange[0].toLocaleString()} - ${amountRange[1].toLocaleString()}
                </Typography>
                <Slider
                  value={amountRange}
                  onChange={(_, newValue) => {
                    setAmountRange(newValue as [number, number]);
                    handleFilterChange('minAmount')(newValue as [number, number]);
                  }}
                  min={0}
                  max={1000000}
                  step={5000}
                  valueLabelDisplay="auto"
                  valueLabelFormat={(value) => `$${value.toLocaleString()}`}
                />
              </Grid>
            </Grid>
          </Collapse>

          {/* Sorting Options */}
          <Box sx={{ display: 'flex', gap: 1, flexWrap: 'wrap' }}>
            <Button
              startIcon={<SortIcon />}
              variant={filters.sortBy === 'due_date' ? 'contained' : 'outlined'}
              onClick={() => handleSortChange('due_date')}
              size="small"
            >
              Due Date {filters.sortBy === 'due_date' && (filters.sortDirection === 'asc' ? '↑' : '↓')}
            </Button>
            <Button
              startIcon={<SortIcon />}
              variant={filters.sortBy === 'amount' ? 'contained' : 'outlined'}
              onClick={() => handleSortChange('amount')}
              size="small"
            >
              Amount {filters.sortBy === 'amount' && (filters.sortDirection === 'asc' ? '↑' : '↓')}
            </Button>
            <Button
              startIcon={<SortIcon />}
              variant={filters.sortBy === 'name' ? 'contained' : 'outlined'}
              onClick={() => handleSortChange('name')}
              size="small"
            >
              Name {filters.sortBy === 'name' && (filters.sortDirection === 'asc' ? '↑' : '↓')}
            </Button>
          </Box>
        </Stack>

        {/* Results Section */}
        {error && (
          <Alert severity="error" sx={{ mb: 3 }}>
            {error}
          </Alert>
        )}

        <AnimatePresence mode="wait">
          {loading ? (
            <Fade in={loading}>
              <Box sx={{ display: 'flex', justifyContent: 'center', py: 8 }}>
                <CircularProgress />
              </Box>
            </Fade>
          ) : grants.length === 0 ? (
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
            >
              <Box
                sx={{
                  textAlign: 'center',
                  py: 8,
                  backgroundColor: 'background.paper',
                  borderRadius: 1,
                }}
              >
                <Typography variant="h6" color="text.secondary">
                  No grants found matching your criteria
                </Typography>
              </Box>
            </motion.div>
          ) : (
            <>
              <motion.div
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                exit={{ opacity: 0 }}
              >
                <Grid container spacing={3}>
                  {grants.map((grant) => (
                    <Grid item xs={12} sm={6} md={4} key={grant.id}>
                      <motion.div
                        initial={{ opacity: 0, y: 20 }}
                        animate={{ opacity: 1, y: 0 }}
                        transition={{ duration: 0.3 }}
                      >
                        <GrantCard
                          title={grant.name}
                          funder={grant.funder}
                          dueDate={new Date(grant.due_date).toLocaleDateString()}
                          amount={grant.amount_string}
                          status={grant.status}
                          eligibilityScore={
                            grant.eligibility_analysis?.score
                              ? Math.round(grant.eligibility_analysis.score * 100)
                              : undefined
                          }
                          onClick={() => handleGrantClick(grant.id)}
                        />
                      </motion.div>
                    </Grid>
                  ))}
                </Grid>
              </motion.div>

              {/* Pagination */}
              <Box sx={{ display: 'flex', justifyContent: 'center', mt: 4, gap: 1 }}>
                <Button
                  disabled={filters.page === 1}
                  onClick={() => handleFilterChange('page')({ target: { value: filters.page - 1 } })}
                >
                  Previous
                </Button>
                <Typography sx={{ alignSelf: 'center' }}>
                  Page {filters.page} of {totalPages}
                </Typography>
                <Button
                  disabled={filters.page === totalPages}
                  onClick={() => handleFilterChange('page')({ target: { value: filters.page + 1 } })}
                >
                  Next
                </Button>
              </Box>
            </>
          )}
        </AnimatePresence>
      </Box>
    </LocalizationProvider>
  );
};

export default GrantList; 