export const colors = {
  // Core neutrals
  black: '#1A1A1A',
  charcoal: '#2C2C2C',
  concrete: '#F5F5F5',
  sand: '#E5DDD3',
  clay: '#C4B5A5',
  ochre: '#D6A162',
  
  // Accent colors
  bloodOrange: '#FF4D4D',
  mustard: '#FFB800',
  teal: '#00B2A9',
  
  // Status colors
  urgent: '#FF4D4D',
  eligible: '#4CAF50',
  highValue: '#FFB800',
  
  // Monochrome scale
  gray100: '#F7F7F7',
  gray200: '#E1E1E1',
  gray300: '#CFCFCF',
  gray400: '#B1B1B1',
  gray500: '#9E9E9E',
  gray600: '#7E7E7E',
  gray700: '#626262',
  gray800: '#515151',
  gray900: '#3B3B3B',
} as const;

export const typography = {
  // Font families
  heading: "'GT America', 'Söhne', 'Public Sans', system-ui, sans-serif",
  body: "'Inter', 'IBM Plex Sans', system-ui, sans-serif",
  
  // Font sizes
  sizes: {
    xs: '0.75rem',
    sm: '0.875rem',
    base: '1rem',
    lg: '1.125rem',
    xl: '1.25rem',
    '2xl': '1.5rem',
    '3xl': '1.875rem',
    '4xl': '2.25rem',
    '5xl': '3rem',
  },
  
  // Font weights
  weights: {
    normal: 400,
    medium: 500,
    semibold: 600,
    bold: 700,
  },
} as const;

export const spacing = {
  xs: '0.25rem',
  sm: '0.5rem',
  md: '1rem',
  lg: '1.5rem',
  xl: '2rem',
  '2xl': '2.5rem',
  '3xl': '3rem',
} as const;

export const breakpoints = {
  sm: '640px',
  md: '768px',
  lg: '1024px',
  xl: '1280px',
  '2xl': '1536px',
} as const;

export const shadows = {
  sm: '0 1px 2px 0 rgba(0, 0, 0, 0.05)',
  md: '0 4px 6px -1px rgba(0, 0, 0, 0.1)',
  lg: '0 10px 15px -3px rgba(0, 0, 0, 0.1)',
} as const;

export const transitions = {
  default: 'all 0.3s ease',
  fast: 'all 0.15s ease',
  slow: 'all 0.45s ease',
} as const;

// Textures
export const textures = {
  paper: `url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='100' height='100' viewBox='0 0 100 100'%3E%3Cfilter id='noise'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.15' numOctaves='3' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100' height='100' filter='url(%23noise)' opacity='0.1'/%3E%3C/svg%3E")`,
  concrete: `url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='100' height='100' viewBox='0 0 100 100'%3E%3Cfilter id='noise'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.25' numOctaves='2' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100' height='100' filter='url(%23noise)' opacity='0.15'/%3E%3C/svg%3E")`,
} as const; 