import React from 'react';

declare type AuthData = {
  token: string;
  email: string;
  verificationStatus: string;
};

declare type ModeHandler = {
  mode: number;
  setMode: React.Dispatch<React.SetStateAction<number>>;
}

declare type AuthContextData = {
  authData?: AuthData;
  loading: boolean;
  setLoading: React.Dispatch<React.SetStateAction<boolean>>;
  signIn(authData: AuthData): Promise<void>;
  signOut(): Promise<void>;
  signUp(authData: AuthData): Promise<void>;
  confirmPasswordReset(authData: AuthData): Promise<void>;
  confirmPasswordChange(): Promise<void>;
  resetPassword(authData: AuthData): Promise<void>;
  changePassword(authData: AuthData): Promise<void>;
  modeHandler?: ModeHandler;
};
    
export type { AuthData };
export type { ModeHandler };
export type { AuthContextData };
