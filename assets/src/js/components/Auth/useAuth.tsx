import { useContext } from 'react';
import { AuthContext } from './AuthProvider';
import type { AuthContextData } from './AuthContext';

function useAuth(): AuthContextData {
  return useContext(AuthContext);
}

export default useAuth;
