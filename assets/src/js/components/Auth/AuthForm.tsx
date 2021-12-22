import React from 'react';
import useAuth from './useAuth';

const AppStack = React.lazy(() => import('./AppStack'));
const AuthStack = React.lazy(() => import('./AuthStack'));

const AuthForm = () => {
  const { authData } = useAuth();
  const Default = !authData?.token ? AuthStack : AppStack;
  return (
    <React.Suspense fallback={<div>Loading...</div>}> 
      <Default />
    </React.Suspense>
  )
};

export default AuthForm;
