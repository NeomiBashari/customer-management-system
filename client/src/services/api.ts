import axios from 'axios';
import { mockAuthApi, mockCustomerApi } from './mockData';

const USE_MOCKS = true;

const API_BASE_URL = '/api';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export interface RegisterData {
  username: string;
  email: string;
  password: string;
}

export interface LoginData {
  username: string;
  password: string;
}

export interface ChangePasswordData {
  userId: number;
  currentPassword: string;
  newPassword: string;
}

export interface ForgotPasswordData {
  email: string;
}

export interface ResetPasswordData {
  token: string;
  newPassword: string;
}

export interface CustomerData {
  name: string;
  email: string;
  phone: string;
  address: string;
  sector: string;
  packageId: number;
}

export const authApi = {
  register: async (data: RegisterData) => {
    if (USE_MOCKS) {
      return await mockAuthApi.register(data);
    }
    const response = await api.post('/auth/register', data);
    return response.data;
  },

  login: async (data: LoginData) => {
    if (USE_MOCKS) {
      return await mockAuthApi.login(data);
    }
    const response = await api.post('/auth/login', data);
    return response.data;
  },

  changePassword: async (data: ChangePasswordData) => {
    if (USE_MOCKS) {
      return await mockAuthApi.changePassword(data);
    }
    const response = await api.post('/auth/change-password', data);
    return response.data;
  },

  forgotPassword: async (data: ForgotPasswordData) => {
    if (USE_MOCKS) {
      return await mockAuthApi.forgotPassword(data);
    }
    const response = await api.post('/auth/forgot-password', data);
    return response.data;
  },

  resetPassword: async (data: ResetPasswordData) => {
    if (USE_MOCKS) {
      return await mockAuthApi.resetPassword(data);
    }
    const response = await api.post('/auth/reset-password', data);
    return response.data;
  },
};

export const customerApi = {
  create: async (data: CustomerData) => {
    if (USE_MOCKS) {
      return await mockCustomerApi.create(data);
    }
    const response = await api.post('/customers', data);
    return response.data;
  },

  getAll: async () => {
    if (USE_MOCKS) {
      return await mockCustomerApi.getAll();
    }
    const response = await api.get('/customers');
    return response.data;
  },

  getById: async (id: number) => {
    if (USE_MOCKS) {
      return await mockCustomerApi.getById(id);
    }
    const response = await api.get(`/customers/${id}`);
    return response.data;
  },

  searchByName: async (name: string) => {
    if (USE_MOCKS) {
      return await mockCustomerApi.searchByName(name);
    }
    const response = await api.get(`/customers/search/${name}`);
    return response.data;
  },
};

