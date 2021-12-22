import AsyncLocalStorage from '@react-native-async-storage/async-storage';
import Loading from './Loading';

async function sentVerification(): Promise<boolean> {
  const n = await AsyncLocalStorage.getItem('@Display');
  if (n) {
    return true;
  } else {
    return false;
  }
}

export const UnverifiedUser = () => {
  const wasSentVerification = sentVerification();
  return (wasSentVerification ?  
   <>
    <div className="text-center">
     Thank you for creating an account with us. You will be redirected to the login screen once you have confirmed your email address.
    </div>
   </>
   : <Loading />
  )
}

