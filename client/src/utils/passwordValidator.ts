import PasswordValidator from 'password-validator';
import zxcvbn from 'zxcvbn';
import { securityConfig } from '../config/securityConfig';

export const validatePassword = (password: string, previousPasswords: string[] = []) => {
  const schema = new PasswordValidator();
  const errors: string[] = [];

  schema.is().min(securityConfig.passwordMinLength, `Password must contain at least ${securityConfig.passwordMinLength} characters`);

  if (securityConfig.passwordRequireUppercase) {
    schema.has().uppercase(1, 'Password must contain at least one uppercase letter');
  }

  if (securityConfig.passwordRequireLowercase) {
    schema.has().lowercase(1, 'Password must contain at least one lowercase letter');
  }

  if (securityConfig.passwordRequireNumbers) {
    schema.has().digits(1, 'Password must contain at least one number');
  }

  if (securityConfig.passwordRequireSpecialChars) {
    schema.has().symbols(1, 'Password must contain at least one special character');
  }

  const failedRules = schema.validate(password, { list: true }) as string[];
  errors.push(...failedRules);

  if (previousPasswords.length > 0) {
    const historyToCheck = previousPasswords.slice(0, securityConfig.passwordHistoryCount);
    if (historyToCheck.includes(password)) {
      errors.push(`Cannot use one of the last ${securityConfig.passwordHistoryCount} passwords`);
    }
  }

  if (securityConfig.preventDictionaryWords) {
    const zxcvbnResult = zxcvbn(password);
    if (zxcvbnResult.score < 2) {
      errors.push('Password is too weak or too common');
    }
  }

  return {
    isValid: errors.length === 0,
    errors,
  };
};

export const getPasswordRequirements = () => {
  const requirements: string[] = [];

  requirements.push(`At least ${securityConfig.passwordMinLength} characters`);

  if (securityConfig.passwordRequireUppercase) requirements.push('uppercase letters');
  if (securityConfig.passwordRequireLowercase) requirements.push('lowercase letters');
  if (securityConfig.passwordRequireNumbers) requirements.push('numbers');
  if (securityConfig.passwordRequireSpecialChars) requirements.push('special characters');
  
  if (securityConfig.passwordHistoryCount > 0) {
    requirements.push(`Cannot use the last ${securityConfig.passwordHistoryCount} passwords`);
  }

  if (securityConfig.preventDictionaryWords) {
    requirements.push('Cannot use common words');
  }

  return requirements.join(', ');
};
