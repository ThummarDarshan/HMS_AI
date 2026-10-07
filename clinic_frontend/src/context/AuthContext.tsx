import React, { createContext, useContext, useState, useEffect, ReactNode } from 'react';
import { User, authService } from '@/services/authService';

interface AuthContextType {
  user: User | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  login: (email: string, password: string) => Promise<void>;
  googleLogin: (token: string) => Promise<void>;
  register: (data: {
    email: string;
    password: string;
    confirm_password: string;
    first_name: string;
    last_name: string;
    phone: string;
    role: string;
  }) => Promise<void>;
  logout: () => Promise<void>;
  refreshUser: () => Promise<void>;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};

export const AuthProvider: React.FC<{ children: ReactNode }> = ({ children }) => {
  const [user, setUser] = useState<User | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    const initAuth = async () => {
      try {
        await authService.initCsrf();

        // Silently obtain fresh access token from HttpOnly cookie if in-memory token is absent
        const token = await authService.refreshToken();
        if (token) {
          try {
            const freshUser = await authService.getProfile();
            setUser(freshUser);
          } catch {
            setUser(null);
          }
        } else {
          setUser(null);
        }
      } catch (error) {
        console.error('Auth initialization error:', error);
      } finally {
        setIsLoading(false);
      }
    };

    initAuth();
  }, []);

  const login = async (email: string, password: string) => {
    const response = await authService.login({ email, password });
    authService.setAuthData(response);
    setUser(response.user);
  };

  const googleLogin = async (token: string) => {
    const response = await authService.googleLogin(token);
    authService.setAuthData(response);
    setUser(response.user);
  };

  const register = async (data: {
    email: string;
    password: string;
    confirm_password: string;
    first_name: string;
    last_name: string;
    phone: string;
    role: string;
  }) => {
    const response = await authService.register(data);
    authService.setAuthData(response);
    setUser(response.user);
  };

  const logout = async () => {
    await authService.logout();
    setUser(null);
  };

  const refreshUser = async () => {
    try {
      const freshUser = await authService.getProfile();
      setUser(freshUser);
    } catch (error) {
      console.error('Failed to refresh user:', error);
      setUser(null);
    }
  };

  return (
    <AuthContext.Provider
      value={{
        user,
        isAuthenticated: !!user,
        isLoading,
        login,
        googleLogin,
        register,
        logout,
        refreshUser,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
};
