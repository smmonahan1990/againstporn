import { useState, useEffect, createContext } from "react";
import type { AuthData, ModeHandler, AuthContextData } from "./AuthContext"; 
import AsyncLocalStorage from "@react-native-async-storage/async-storage";

export const AuthContext = createContext<AuthContextData>(
  {} as AuthContextData
);
async function logoutUser(token: string) {
    const url = "https://againstporn.org/api/accounts/logout/";
    const api_url = 
        process.env.NODE_ENV === 'production' 
        ? url 
        : url.replace('/api', ':8000/api');
    return fetch(api_url, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': 'Token ' + JSON.parse(token).token
        },
    })
    .then((data) => data.json())
    .catch((err) => console.log(err));
}

async function checkStatus(path: string, data: string): Promise<any> {
    const url = 'https://againstporn.org/api/accounts/' + path;
    const api_url = 
        process.env.NODE_ENV === 'production'
        ? url 
        : url.replace('/api', ':8000/api');
    return fetch(api_url, {
        method: 'POST',
        headers: {
           'Content-Type': 'application/json',
        }, 
        body: data
    })
     .then((response) => response.json())
     .catch((err) => console.log(err));
}

export const AuthProvider: React.FC = ({ children }) => {
  const [authData, setAuthData] = useState<AuthData>();
  const [loading, setLoading] = useState(true);
  const [mode, setMode] = useState(0);
  const modeHandler: ModeHandler = { mode: mode, setMode: setMode };
  async function loadData(): Promise<any> {
    try {
      const data: string | null = await AsyncLocalStorage.getItem('@AuthData');
      const serializedData = JSON.parse(data || '{"":""}');
      if (serializedData?.verificationStatus && !serializedData?.token) {
        if (serializedData?.verificationStatus === 'created') {
           const status = await checkStatus('signup/verify/', data || '');
           if (status && status.success !== undefined) {
               setMode(1);
            };    
         } else if (serializedData?.verificationStatus === 'pendingPasswordReset') {
           const status = await checkStatus('password/reset/verify/', data || '');
           if (!!status && !!status?.success) {
               setMode(6);
               setAuthData({ email: serializedData.email,
                             token: '',
                             verificationStatus: status.success });
           } else if (!!status && !!status?.failure) {
               await AsyncLocalStorage.removeItem('@AuthData');
           }
         }       
      };
      if (!serializedData?.email) {
          setAuthData(undefined);
      } else if (!!serializedData?.email && !serializedData.verificationStatus && !!serializedData.token) { 
          setAuthData(serializedData);
      }
    } catch (error) {
      console.log(error);
    } finally {
      setLoading(false);
    }
    return;
  }

  useEffect(() => {
    loadData();
  },[]);

  const signIn = async (_authData: AuthData) => {
    setLoading(true);
    await AsyncLocalStorage.setItem('@AuthData',JSON.stringify(_authData));
    window.location.reload();
  };

  const signOut = async () => {
    setLoading(true);
    const _authData: string | null = await AsyncLocalStorage.getItem('@AuthData');
    const logOut = await logoutUser(_authData || "");
    if (logOut)
        await AsyncLocalStorage.removeItem('@AuthData');
    window.location.reload();
  };

  const signUp = async (_authData: AuthData) => {
    setMode(5);
    await AsyncLocalStorage.setItem('@AuthData',JSON.stringify(_authData));
    setLoading(false);
  }
  const confirmPasswordReset = async (_authData: AuthData) => {
    setMode(4);
    await AsyncLocalStorage.setItem('@AuthData', JSON.stringify(_authData));
    setLoading(false);
  }

  const resetPassword = async (_authData: AuthData) => {
    setMode(7);
    await AsyncLocalStorage.setItem('@AuthData', JSON.stringify(_authData));
    setLoading(false);
  }
  return (
    <AuthContext.Provider 
     value={{ authData,
              loading,
              setLoading,
              signIn,
              signOut,
              signUp,
              confirmPasswordReset,
              resetPassword,
              modeHandler
      }}
    >
      {children}
    </AuthContext.Provider>
  );
};
