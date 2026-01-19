import { createContext, useContext, useState, useEffect, ReactNode } from 'react';

interface ApiModeContextType {
  isValidated: boolean;
  toggleApiMode: () => void;
  routeMode: 'validated' | 'unvalidated';
}

const ApiModeContext = createContext<ApiModeContextType | undefined>(undefined);

export const ApiModeProvider = ({ children }: { children: ReactNode }) => {
  const [isValidated, setIsValidated] = useState<boolean>(() => {
    const saved = localStorage.getItem('apiMode');
    return saved ? saved === 'validated' : true;
  });

  useEffect(() => {
    localStorage.setItem('apiMode', isValidated ? 'validated' : 'unvalidated');
  }, [isValidated]);

  const toggleApiMode = () => {
    setIsValidated((prev) => !prev);
  };

  const routeMode = isValidated ? 'validated' : 'unvalidated';

  return (
    <ApiModeContext.Provider value={{ isValidated, toggleApiMode, routeMode }}>
      {children}
    </ApiModeContext.Provider>
  );
};

export const useApiMode = () => {
  const context = useContext(ApiModeContext);
  if (context === undefined) {
    throw new Error('useApiMode must be used within an ApiModeProvider');
  }
  return context;
};

// Helper function to get route mode from localStorage (for use outside React components)
export const getRouteMode = (): 'validated' | 'unvalidated' => {
  const saved = localStorage.getItem('apiMode');
  return saved === 'unvalidated' ? 'unvalidated' : 'validated';
};
