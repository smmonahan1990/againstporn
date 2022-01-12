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
        : url.replace('https://againstporn.org', 'http://34.225.127.212:8000');
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
    const url = 'https://againstporn.org/api' + path;
    const api_url = 
        process.env.NODE_ENV === 'production'
        ? url 
        : url.replace('https://againstporn.org', 'http://34.225.127.212:8000');
    const headers = new Headers();
    headers.set('Content-Type', "application/json");
    if (JSON.parse(data)?.token)
        headers.set('Authorization', 'Token ' + `${JSON.parse(data)?.token || ''}`);
    return fetch(api_url, {
        method: 'POST',
        headers: headers,
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
           const status = await checkStatus('/accounts/signup/verify/', data || '');
           if (status && status.success !== undefined) {
               setMode(1);
            };    
         } else if (serializedData?.verificationStatus === 'pendingPasswordReset') {
           const status = await checkStatus('/accounts/password/reset/verify/', data || '');
           if (!!status && !!status?.success) {
               setMode(6);
               setAuthData({ ...serializedData,
                             email: serializedData.email,
                             token: '',
                             verificationStatus: status.success });
           } else if (!!status && !!status?.failure) {
               await AsyncLocalStorage.removeItem('@AuthData');
           }
         }       
      };
      if (!serializedData?.email) 
          setAuthData(undefined);

      else if (!!serializedData?.email 
               && !serializedData.verificationStatus 
               && !!serializedData.token
               ) 
               { 
                 const status = await checkStatus(document.location.pathname, data);
                 if (!!status && status.hasOwnProperty('success')) {  
                   if (document.location.pathname.match(/\/\w+\/\w{6}\//g)) {
                     const reports = await AsyncLocalStorage.getItem("@Reports");
                     const flair_choices = await AsyncLocalStorage.getItem("@flair");
                     const flair = JSON.parse(flair_choices);
                     const path = document.location.pathname.split('/')[1];
                     const choices = flair.hasOwnProperty(path) ? flair[path] : [];
                     setAuthData({ ...serializedData, 
                                   verificationStatus: {
                                   admin_link: status.success, 
                                   flair_choices: choices
                                   }, reports: reports
                                });
                                      
                   } else setAuthData({...serializedData, verificationStatus: status.success, reports: ''});
                 }
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

 const signIn = async (authData: AuthData) => {
    setLoading(true);
    await AsyncLocalStorage.setItem('@AuthData',JSON.stringify({...authData, verificationStatus: ''}));
    await AsyncLocalStorage.setItem('@flair', authData.verificationStatus);
    window.location.reload();
  };

  const signOut = async () => {
    setLoading(true);
    const authData: string | null = await AsyncLocalStorage.getItem('@AuthData');
    const logOut = await logoutUser(authData || "");
    if (logOut)
        await AsyncLocalStorage.removeItem('@AuthData');
    window.location.reload();
  };

  const signUp = async (authData: AuthData) => {
    setMode(5);
    await AsyncLocalStorage.setItem('@AuthData',JSON.stringify(authData));
    setLoading(false);
  }
  const confirmPasswordReset = async (authData: AuthData) => {
    setMode(4);
    await AsyncLocalStorage.setItem('@AuthData', JSON.stringify(authData));
    setLoading(false);
  }

  const resetPassword = async (authData: AuthData) => {
    setMode(7);
    await AsyncLocalStorage.setItem('@AuthData', JSON.stringify(authData));
    setLoading(false);
  }

  const confirmPasswordChange = async () => {
    setMode(9);
    setLoading(false);
  }

  const changePassword = async() => {
    setMode(10);
    setLoading(false);
  };

  return (
    <AuthContext.Provider 
     value={{ authData,
              loading,
              setLoading,
              signIn,
              signOut,
              signUp,
              confirmPasswordReset,
              confirmPasswordChange,
              resetPassword,
              changePassword,
              modeHandler,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
};
