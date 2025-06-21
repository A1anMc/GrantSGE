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
  Card,
  CardContent,
  Chip,
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
import { useQuery } from '@tanstack/react-query';
import { supabase, type Grant } from '../lib/supabase';
import { format } from 'date-fns';

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

export const GrantList = () => {
  const [searchTerm, setSearchTerm] = useState('');

  const { data: grants, isLoading, error } = useQuery({
    queryKey: ['grants'],
    queryFn: async () => {
      const { data, error } = await supabase
        .from('grants')
        .select('*')
        .order('due_date', { ascending: true });

      if (error) throw error;
      return data as Grant[];
    },
  });

  const filteredGrants = grants?.filter((grant) =>
    grant.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
    grant.funder.toLowerCase().includes(searchTerm.toLowerCase()) ||
    grant.description?.toLowerCase().includes(searchTerm.toLowerCase())
  );

  const formatAmount = (amount: any) => {
    if (!amount) return 'Amount not specified';
    if (amount.fixed) return `$${amount.fixed.toLocaleString()}`;
    if (amount.max && amount.min) return `$${amount.min.toLocaleString()} - $${amount.max.toLocaleString()}`;
    if (amount.max) return `Up to $${amount.max.toLocaleString()}`;
    if (amount.description) return amount.description;
    return 'Amount not specified';
  };

  if (error) {
    return <Alert severity="error">Error loading grants</Alert>;
  }

  return (
    <Box sx={{ p: 3 }}>
      <TextField
        fullWidth
        variant="outlined"
        placeholder="Search grants..."
        value={searchTerm}
        onChange={(e) => setSearchTerm(e.target.value)}
        sx={{ mb: 3 }}
        InputProps={{
          startAdornment: (
            <InputAdornment position="start">
              <SearchIcon />
            </InputAdornment>
          ),
        }}
      />

      {isLoading ? (
        <Box display="flex" justifyContent="center">
          <CircularProgress />
        </Box>
      ) : (
        <Grid container spacing={3}>
          {filteredGrants?.map((grant) => (
            <Grid item xs={12} sm={6} md={4} key={grant.id}>
              <Card sx={{ height: '100%' }}>
                <CardContent>
                  <Typography variant="h6" gutterBottom>
                    {grant.title}
                  </Typography>
                  
                  <Typography color="textSecondary" gutterBottom>
                    {grant.funder}
                  </Typography>

                  <Typography variant="body2" sx={{ mb: 2 }}>
                    {grant.description?.slice(0, 150)}
                    {grant.description && grant.description.length > 150 ? '...' : ''}
                  </Typography>

                  <Box sx={{ mb: 1 }}>
                    <Chip
                      label={formatAmount(grant.amount_range)}
                      size="small"
                      sx={{ mr: 1 }}
                    />
                    {grant.due_date && (
                      <Chip
                        label={`Due: ${format(new Date(grant.due_date), 'dd MMM yyyy')}`}
                        size="small"
                        color="primary"
                      />
                    )}
                  </Box>
                </CardContent>
              </Card>
            </Grid>
          ))}
        </Grid>
      )}
    </Box>
  );
};

export default GrantList; 