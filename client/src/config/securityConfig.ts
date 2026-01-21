export interface SecurityConfig {
  passwordMinLength: number;
  passwordRequireUppercase: boolean;
  passwordRequireLowercase: boolean;
  passwordRequireNumbers: boolean;
  passwordRequireSpecialChars: boolean;
  passwordHistoryCount: number;
  preventDictionaryWords: boolean;
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
  preventDictionaryWords: true, // Uses zxcvbn library
  maxLoginAttempts: 3,
  lockoutDurationMinutes: 15,
};
