import { createTheme, Theme } from '@mui/material/styles';
import { colors, typography, shadows } from '../styles/tokens';

declare module '@mui/material/styles' {
  interface Palette {
    status: {
      urgent: string;
      eligible: string;
      highValue: string;
    };
    neutral: Palette['primary'];
  }
  interface PaletteOptions {
    status: {
      urgent: string;
      eligible: string;
      highValue: string;
    };
    neutral: PaletteOptions['primary'];
  }
}

export const theme: Theme = createTheme({
  palette: {
    primary: {
      main: colors.charcoal,
      light: colors.gray600,
      dark: colors.black,
      contrastText: colors.concrete,
    },
    secondary: {
      main: colors.bloodOrange,
      light: colors.teal,
      dark: colors.mustard,
      contrastText: colors.black,
    },
    neutral: {
      main: '#64748b',
      light: '#94a3b8',
      dark: '#475569',
      contrastText: '#ffffff',
    },
    error: {
      main: '#dc2626',
      light: '#ef4444',
      dark: '#b91c1c',
      contrastText: '#ffffff',
    },
    warning: {
      main: '#d97706',
      light: '#f59e0b',
      dark: '#b45309',
      contrastText: '#ffffff',
    },
    info: {
      main: '#0891b2',
      light: '#06b6d4',
      dark: '#0e7490',
      contrastText: '#ffffff',
    },
    success: {
      main: '#059669',
      light: '#10b981',
      dark: '#047857',
      contrastText: '#ffffff',
    },
    background: {
      default: colors.concrete,
      paper: colors.gray100,
    },
    text: {
      primary: colors.black,
      secondary: colors.gray700,
    },
    status: {
      urgent: colors.urgent,
      eligible: colors.eligible,
      highValue: colors.highValue,
    },
  },
  typography: {
    fontFamily: typography.body,
    h1: {
      fontFamily: typography.heading,
      fontWeight: typography.weights.bold,
      fontSize: typography.sizes['5xl'],
      letterSpacing: '-0.02em',
    },
    h2: {
      fontFamily: typography.heading,
      fontWeight: typography.weights.bold,
      fontSize: typography.sizes['4xl'],
      letterSpacing: '-0.01em',
    },
    h3: {
      fontFamily: typography.heading,
      fontWeight: typography.weights.semibold,
      fontSize: typography.sizes['3xl'],
    },
    h4: {
      fontFamily: typography.heading,
      fontWeight: typography.weights.semibold,
      fontSize: typography.sizes['2xl'],
    },
    h5: {
      fontFamily: typography.heading,
      fontWeight: typography.weights.medium,
      fontSize: typography.sizes.xl,
    },
    h6: {
      fontFamily: typography.heading,
      fontWeight: typography.weights.medium,
      fontSize: typography.sizes.lg,
    },
    body1: {
      fontSize: typography.sizes.base,
      lineHeight: 1.6,
    },
    body2: {
      fontSize: typography.sizes.sm,
      lineHeight: 1.5,
    },
  },
  components: {
    MuiCard: {
      styleOverrides: {
        root: {
          borderRadius: '8px',
          boxShadow: shadows.md,
          transition: 'transform 0.2s ease-in-out, box-shadow 0.2s ease-in-out',
          '&:hover': {
            transform: 'translateY(-2px)',
            boxShadow: shadows.lg,
          },
        },
      },
    },
    MuiButton: {
      styleOverrides: {
        root: {
          textTransform: 'none',
          borderRadius: '6px',
          fontWeight: typography.weights.medium,
          padding: '8px 16px',
        },
        contained: {
          boxShadow: 'none',
          '&:hover': {
            boxShadow: shadows.sm,
          },
        },
      },
    },
    MuiChip: {
      styleOverrides: {
        root: {
          borderRadius: '6px',
          fontWeight: typography.weights.medium,
        },
      },
    },
  },
});

export default theme; 