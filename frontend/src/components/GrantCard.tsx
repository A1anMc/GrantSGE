import React from 'react';
import {
  Card,
  CardContent,
  Typography,
  Chip,
  Box,
  LinearProgress,
  styled,
} from '@mui/material';
import { colors, transitions } from '../styles/tokens';

interface GrantCardProps {
  title: string;
  funder: string;
  dueDate: string;
  amount: string;
  status: 'urgent' | 'eligible' | 'potential';
  eligibilityScore?: number;
  imageUrl?: string;
  onClick?: () => void;
}

// Styled components
const StyledCard = styled(Card)(({ theme }) => ({
  position: 'relative',
  overflow: 'hidden',
  cursor: 'pointer',
  backgroundColor: theme.palette.background.paper,
  '&::before': {
    content: '""',
    position: 'absolute',
    top: 0,
    left: 0,
    right: 0,
    height: '4px',
    background: (props: any) => {
      switch (props.status) {
        case 'urgent':
          return colors.urgent;
        case 'eligible':
          return colors.eligible;
        default:
          return colors.gray400;
      }
    },
    transition: transitions.default,
  },
}));

const ImageOverlay = styled(Box)({
  position: 'relative',
  height: '160px',
  backgroundSize: 'cover',
  backgroundPosition: 'center',
  '&::after': {
    content: '""',
    position: 'absolute',
    top: 0,
    left: 0,
    right: 0,
    bottom: 0,
    background: `linear-gradient(180deg, rgba(0,0,0,0) 0%, rgba(0,0,0,0.7) 100%)`,
  },
});

const StatusChip = styled(Chip)(({ theme, status }: { theme: any; status: string }) => ({
  position: 'absolute',
  top: '12px',
  right: '12px',
  zIndex: 1,
  backgroundColor: theme.palette.background.paper,
  color: (() => {
    switch (status) {
      case 'urgent':
        return colors.urgent;
      case 'eligible':
        return colors.eligible;
      default:
        return colors.gray700;
    }
  })(),
}));

const EligibilityBar = styled(LinearProgress)(({ theme }) => ({
  height: 4,
  borderRadius: 2,
  backgroundColor: colors.gray200,
  '.MuiLinearProgress-bar': {
    backgroundColor: colors.eligible,
  },
}));

const GrantCard: React.FC<GrantCardProps> = ({
  title,
  funder,
  dueDate,
  amount,
  status,
  eligibilityScore = 0,
  imageUrl,
  onClick,
}) => {
  return (
    <StyledCard status={status} onClick={onClick}>
      {imageUrl && (
        <ImageOverlay
          sx={{
            backgroundImage: `url(${imageUrl})`,
          }}
        />
      )}
      <StatusChip
        label={status.charAt(0).toUpperCase() + status.slice(1)}
        status={status}
        size="small"
      />
      <CardContent>
        <Typography
          variant="overline"
          color="text.secondary"
          sx={{ mb: 1, display: 'block' }}
        >
          {funder}
        </Typography>
        <Typography variant="h5" component="h2" sx={{ mb: 2 }}>
          {title}
        </Typography>
        <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 2 }}>
          <Typography variant="body2" color="text.secondary">
            Due: {dueDate}
          </Typography>
          <Typography variant="body2" fontWeight="medium" color="text.primary">
            {amount}
          </Typography>
        </Box>
        {eligibilityScore > 0 && (
          <Box sx={{ mt: 2 }}>
            <Typography variant="body2" color="text.secondary" sx={{ mb: 1 }}>
              Eligibility Match
            </Typography>
            <EligibilityBar
              variant="determinate"
              value={eligibilityScore}
            />
          </Box>
        )}
      </CardContent>
    </StyledCard>
  );
};

export default GrantCard; 