import axios from 'axios';
import { mockAuthApi, mockCustomerApi } from './mockData';
import { getRouteMode } from '../contexts/ApiModeContext';

const USE_MOCKS = false;

const API_BASE_URL = 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export interface RegisterData {
  email: string;
  password: string;
}

export interface UserResponse {
  id: number;
  email: string;
  message: string;
}

export interface LoginData {
  email: string;
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
  email: string;
  token: string;
  newPassword: string;
}

export interface CustomerData {
  firstname: string;
  lastname: string;
  email: string;
}

export const authApi = {
  register: async (data: RegisterData) => {
    if (USE_MOCKS) {
      return await mockAuthApi.register(data);
    }
    const mode = getRouteMode();
    const response = await api.post(`/users/create/${mode}`, {
      email: data.email,
      password: data.password,
    });
    return {
      user: {
        id: response.data.id,
        email: response.data.email,
      },
    };
  },

  login: async (data: LoginData) => {
    if (USE_MOCKS) {
      return await mockAuthApi.login(data);
    }
    const mode = getRouteMode();
    const response = await api.post(`/users/login/${mode}`, {
      email: data.email,
      password: data.password,
    });
    return {
      user: {
        id: response.data.id || 1,
        email: response.data.email || data.email,
      },
    };
  },

  changePassword: async (data: ChangePasswordData) => {
    if (USE_MOCKS) {
      return await mockAuthApi.changePassword(data);
    }
    const mode = getRouteMode();
    const response = await api.put(`/users/change-password/${mode}`, {
      email: data.userId.toString(),
      old_password: data.currentPassword,
      new_password: data.newPassword,
    });
    return response.data;
  },

  forgotPassword: async (data: ForgotPasswordData) => {
    if (USE_MOCKS) {
      return await mockAuthApi.forgotPassword(data);
    }
    const mode = getRouteMode();
    const response = await api.post(`/users/forgot-password/${mode}`, data);
    return response.data;
  },

  resetPassword: async (data: ResetPasswordData) => {
    if (USE_MOCKS) {
      return await mockAuthApi.resetPassword(data);
    }
    const mode = getRouteMode();
    const response = await api.post(`/users/reset-password/${mode}`, {
      email: data.email,
      old_password: data.token,
      new_password: data.newPassword,
    });
    return response.data;
  },
};

export const customerApi = {
  create: async (data: CustomerData) => {
    if (USE_MOCKS) {
      return await mockCustomerApi.create(data);
    }
    const mode = getRouteMode();
    const response = await api.post(`/customers/create/${mode}`, data);
    return response.data;
  },

  getAll: async () => {
    if (USE_MOCKS) {
      return await mockCustomerApi.getAll();
    }
    // Note: /customers/all has no unvalidated variant, always uses base endpoint
    const response = await api.post('/customers/all');
    return response.data;
  },

  getById: async (id: number) => {
    if (USE_MOCKS) {
      return await mockCustomerApi.getById(id);
    }
    const mode = getRouteMode();
    const response = await api.post(`/customers/${id}/${mode}`, { id: id.toString() });
    return {
      id: response.data.res_id || id,
      name: `${response.data.firstname} ${response.data.lastname}`,
      email: response.data.email,
      firstname: response.data.firstname,
      lastname: response.data.lastname,
    };
  },

  searchByName: async (name: string) => {
    if (USE_MOCKS) {
      return await mockCustomerApi.searchByName(name);
    }
    const allCustomers = await api.post('/customers/all');
    return allCustomers.data.filter((c: any) =>
      `${c.firstname} ${c.lastname}`.toLowerCase().includes(name.toLowerCase())
    );
  },
};
