export interface SecurityConfig {
  passwordMinLength: number;
  passwordRequireUppercase: boolean;
  passwordRequireLowercase: boolean;
  passwordRequireNumbers: boolean;
  passwordRequireSpecialChars: boolean;
  passwordHistoryCount: number;
  preventDictionaryWords: boolean;
  dictionaryWords: string[];
  maxLoginAttempts: number;
  lockoutDurationMinutes: number;
}

export const securityConfig: SecurityConfig = {
  passwordMinLength: 10,
  passwordRequireUppercase: true,
  passwordRequireLowercase: true,
  passwordRequireNumbers: true,
  passwordRequireSpecialChars: true,
  passwordHistoryCount: 3,
  preventDictionaryWords: true,
  dictionaryWords: [
    'password',
    '12345678',
    '123456789',
    '1234567890',
    'qwerty',
    'abc123',
    'monkey',
    '1234567',
    'letmein',
    'trustno1',
    'dragon',
    'baseball',
    'iloveyou',
    'master',
    'sunshine',
    'ashley',
    'bailey',
    'passw0rd',
    'shadow',
    '123123',
    '654321',
    'superman',
    'qazwsx',
    'michael',
    'football',
    'welcome',
    'jesus',
    'ninja',
    'mustang',
    'password1',
    'admin',
    'root',
    'user',
    'test',
    'guest',
    'login',
    'welcome123',
    'password123',
    'admin123',
  ],
  maxLoginAttempts: 3,
  lockoutDurationMinutes: 15,
};

