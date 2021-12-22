import Router from './Router';
import { AuthProvider } from './../Auth/AuthProvider';

const App = () => {
  return (
    <AuthProvider>
      <Router />
    </AuthProvider>
  );
};

export default App;
