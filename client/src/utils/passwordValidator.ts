import { securityConfig } from '../config/securityConfig';

export interface PasswordValidationResult {
  isValid: boolean;
  errors: string[];
}

export const validatePassword = (
  password: string,
  previousPasswords: string[] = []
): PasswordValidationResult => {
  const errors: string[] = [];

  if (password.length < securityConfig.passwordMinLength) {
    errors.push(
      `Password must contain at least ${securityConfig.passwordMinLength} characters`
    );
  }

  if (securityConfig.passwordRequireUppercase) {
    if (!/[A-Z]/.test(password)) {
      errors.push('Password must contain at least one uppercase letter');
    }
  }

  if (securityConfig.passwordRequireLowercase) {
    if (!/[a-z]/.test(password)) {
      errors.push('Password must contain at least one lowercase letter');
    }
  }

  if (securityConfig.passwordRequireNumbers) {
    if (!/[0-9]/.test(password)) {
      errors.push('Password must contain at least one number');
    }
  }

  if (securityConfig.passwordRequireSpecialChars) {
    if (!/[!@#$%^&*()_+\-=\[\]{};':"\\|,.<>\/?]/.test(password)) {
      errors.push('Password must contain at least one special character');
    }
  }

  if (previousPasswords.length > 0) {
    const historyToCheck = previousPasswords.slice(
      0,
      securityConfig.passwordHistoryCount
    );
    if (historyToCheck.includes(password)) {
      errors.push(
        `Cannot use one of the last ${securityConfig.passwordHistoryCount} passwords`
      );
    }
  }

  if (securityConfig.preventDictionaryWords) {
    const passwordLower = password.toLowerCase();
    for (const word of securityConfig.dictionaryWords) {
      if (passwordLower.includes(word.toLowerCase())) {
        errors.push('Password cannot contain common dictionary words');
        break;
      }
    }
  }

  return {
    isValid: errors.length === 0,
    errors,
  };
};

export const getPasswordRequirements = (): string => {
  const requirements: string[] = [];

  requirements.push(
    `At least ${securityConfig.passwordMinLength} characters`
  );

  if (securityConfig.passwordRequireUppercase) {
    requirements.push('uppercase letters');
  }

  if (securityConfig.passwordRequireLowercase) {
    requirements.push('lowercase letters');
  }

  if (securityConfig.passwordRequireNumbers) {
    requirements.push('numbers');
  }

  if (securityConfig.passwordRequireSpecialChars) {
    requirements.push('special characters');
  }

  if (securityConfig.passwordHistoryCount > 0) {
    requirements.push(
      `Cannot use the last ${securityConfig.passwordHistoryCount} passwords`
    );
  }

  if (securityConfig.preventDictionaryWords) {
    requirements.push('Cannot use common words');
  }

  return requirements.join(', ');
};

