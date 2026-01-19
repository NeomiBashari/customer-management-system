import { validatePassword } from '../utils/passwordValidator';
import { securityConfig } from '../config/securityConfig';

export interface MockUser {
  id: number;
  username: string;
  email: string;
  password: string;
  passwordHistory: string[];
  loginAttempts: number;
  lockedUntil?: Date;
}

export interface MockCustomer {
  id: number;
  firstname: string;
  lastname: string;
  email: string;
}

export const mockUsers: MockUser[] = [
  {
    id: 1,
    username: 'a',
    email: 'a',
    password: 'a',
    passwordHistory: [],
    loginAttempts: 0,
  },
  {
    id: 2,
    username: 'john.doe',
    email: 'john.doe@example.com',
    password: 'Password123!',
    passwordHistory: [],
    loginAttempts: 0,
  },
  {
    id: 3,
    username: 'jane.smith',
    email: 'jane.smith@example.com',
    password: 'SecurePass456!',
    passwordHistory: [],
    loginAttempts: 0,
  },
];

export const mockCustomers: MockCustomer[] = [
  {
    id: 1,
    firstname: 'Acme',
    lastname: 'Corporation',
    email: 'contact@acme.com',
  },
  {
    id: 2,
    firstname: 'Global',
    lastname: 'Industries',
    email: 'info@global.com',
  },
];

const delay = (ms: number) => new Promise((resolve) => setTimeout(resolve, ms));

export const mockAuthApi = {
  register: async (data: { username: string; email: string; password: string }) => {
    await delay(500);
    
    if (mockUsers.find((u) => u.username === data.username || u.email === data.email)) {
      throw {
        response: {
          data: { error: 'Username or email already exists' },
        },
      };
    }

    const validation = validatePassword(data.password);
    if (!validation.isValid) {
      throw {
        response: {
          data: { error: validation.errors.join(', ') },
        },
      };
    }

    const newUser: MockUser = {
      id: mockUsers.length + 1,
      username: data.username,
      email: data.email,
      password: data.password,
      passwordHistory: [],
      loginAttempts: 0,
    };

    mockUsers.push(newUser);

    return {
      user: {
        id: newUser.id,
        username: newUser.username,
        email: newUser.email,
      },
    };
  },

  login: async (data: { username: string; password: string }) => {
    await delay(500);

    const user = mockUsers.find((u) => u.username === data.username);

    if (!user) {
      throw {
        response: {
          data: { error: 'Invalid username or password' },
        },
      };
    }

    if (user.lockedUntil && user.lockedUntil > new Date()) {
      const minutesLeft = Math.ceil(
        (user.lockedUntil.getTime() - new Date().getTime()) / 60000
      );
      throw {
        response: {
          data: {
            error: `Account is locked. Try again in ${minutesLeft} minutes`,
          },
        },
      };
    }

    if (user.password !== data.password) {
      user.loginAttempts += 1;

      if (user.loginAttempts >= securityConfig.maxLoginAttempts) {
        user.lockedUntil = new Date(
          Date.now() + securityConfig.lockoutDurationMinutes * 60 * 1000
        );
        throw {
          response: {
            data: {
              error: `Too many failed attempts. Account locked for ${securityConfig.lockoutDurationMinutes} minutes`,
            },
          },
        };
      }

      throw {
        response: {
          data: {
            error: `Invalid username or password. ${securityConfig.maxLoginAttempts - user.loginAttempts} attempts remaining`,
          },
        },
      };
    }

    user.loginAttempts = 0;
    user.lockedUntil = undefined;

    return {
      user: {
        id: user.id,
        username: user.username,
        email: user.email,
      },
    };
  },

  changePassword: async (data: {
    userId: number;
    currentPassword: string;
    newPassword: string;
  }) => {
    await delay(500);

    const user = mockUsers.find((u) => u.id === data.userId);

    if (!user) {
      throw {
        response: {
          data: { error: 'User not found' },
        },
      };
    }

    if (user.password !== data.currentPassword) {
      throw {
        response: {
          data: { error: 'Current password is incorrect' },
        },
      };
    }

    const validation = validatePassword(data.newPassword, user.passwordHistory);
    if (!validation.isValid) {
      throw {
        response: {
          data: { error: validation.errors.join(', ') },
        },
      };
    }

    user.passwordHistory.unshift(user.password);
    if (user.passwordHistory.length > securityConfig.passwordHistoryCount) {
      user.passwordHistory = user.passwordHistory.slice(
        0,
        securityConfig.passwordHistoryCount
      );
    }

    user.password = data.newPassword;

    return { message: 'Password changed successfully' };
  },

  forgotPassword: async (data: { email: string }) => {
    await delay(500);

    const user = mockUsers.find((u) => u.email === data.email);

    if (!user) {
      throw {
        response: {
          data: { error: 'Email not found' },
        },
      };
    }

    return { message: 'Password reset email sent' };
  },

  resetPassword: async (data: { token: string; newPassword: string }) => {
    await delay(500);

    const validation = validatePassword(data.newPassword);
    if (!validation.isValid) {
      throw {
        response: {
          data: { error: validation.errors.join(', ') },
        },
      };
    }

    return { message: 'Password reset successfully' };
  },
};

let customerIdCounter = mockCustomers.length + 1;

export const mockCustomerApi = {
  create: async (data: {
    firstname: string;
    lastname: string;
    email: string;
  }) => {
    await delay(500);

    const newCustomer: MockCustomer = {
      id: customerIdCounter++,
      ...data,
    };

    mockCustomers.push(newCustomer);

    return {
      customer: newCustomer,
    };
  },

  getAll: async () => {
    await delay(300);
    return mockCustomers;
  },

  getById: async (id: number) => {
    await delay(300);
    const customer = mockCustomers.find((c) => c.id === id);
    if (!customer) {
      throw {
        response: {
          data: { error: 'Customer not found' },
        },
      };
    }
    return customer;
  },

  searchByName: async (name: string) => {
    await delay(300);
    return mockCustomers.filter((c) =>
      `${c.firstname} ${c.lastname}`.toLowerCase().includes(name.toLowerCase())
    );
  },
};

