export const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

export const ROUTES = {
  HOME: '/',
  AUTH: {
    LOGIN: '/auth/login',
    REGISTER: '/auth/register',
  },
  DASHBOARD: '/dashboard',
  DONATIONS: {
    INDEX: '/donations',
    CREATE: '/donations/create',
    DETAIL: (id: string) => `/donations/${id}`,
  },
  FUNDS: {
    INDEX: '/funds',
    DETAIL: (id: string) => `/funds/${id}`,
  },
  PROFILE: '/profile',
  ADMIN: {
    DASHBOARD: '/admin/dashboard',
    USERS: '/admin/users',
    DONATIONS: '/admin/donations',
    FUNDS: '/admin/funds',
  },
}

export const PAYMENT_METHODS = {
  BANK_TRANSFER: 'bank_transfer',
  QR_CODE: 'qr_code',
}

export const CURRENCIES = {
  MYR: 'MYR',
  HKD: 'HKD',
  AUD: 'AUD',
  USD: 'USD',
  CNY: 'CNY',
  SGD: 'SGD',
}
