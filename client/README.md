# Frontend - Communication_LTD

## Setup

1. Install dependencies:
```bash
npm install
```

2. Start the development server:
```bash
npm run dev
```

The application will be available at `http://localhost:5173`

## Pages

- **Register** (`/register`) - User registration
- **Login** (`/login`) - User login
- **Change Password** (`/change-password`) - Change user password
- **Forgot Password** (`/forgot-password`) - Request password reset
- **Reset Password** (`/reset-password`) - Reset password with token
- **Customer Management** (`/customers`) - Add and view customers

## Security Notes

### Secure Version
- Uses React's automatic HTML escaping
- No `dangerouslySetInnerHTML`
- All user input is safely rendered

### Vulnerable Version
- `CustomerManagement.vulnerable.tsx` demonstrates XSS vulnerabilities
- Uses `dangerouslySetInnerHTML` for demonstration purposes
- **DO NOT USE IN PRODUCTION**

