import Loading from './Loading';
import React, { Suspense } from 'react';
import useAuth from '../Auth/useAuth';
import { Modal, ModalHeader, ModalBody, ModalFooter } from "reactstrap";

const CustomModal = () => {
  const { loading, 
          modeHandler : { mode, setMode }
  } = useAuth();
  const LoginForm = React.lazy(() => import('../Auth/LoginForm'));
  const SignupForm = React.lazy(() => import('../Auth/SignupForm'));
  const PasswordResetConfirmForm = React.lazy(() => import('../Auth/PasswordResetConfirm'));
  const PasswordResetForm = React.lazy(() => import("../Auth/PasswordResetForm"));
  const PasswordResetEmailSent = React.lazy(() => import("../Auth/PasswordResetEmailSent"));
  const PasswordResetComplete = React.lazy(() => import("../Auth/PasswordResetComplete"));
  const PasswordChangeConfirmForm = React.lazy(() => import('../Auth/PasswordChangeConfirm'));
  const PasswordChangeForm = React.lazy(() => import('../Auth/PasswordChangeForm'));
  const PasswordChangeDone = React.lazy(() => import('../Auth/PasswordChangeDone'));
  const ModerationForm = React.lazy(() => import('../Archives/ModerationForm'));
  const PostModerated = React.lazy(() => import('../Archives/PostModerated'));
  const UnverifiedUser = React.lazy(() => import('./DefaultExport'));
  function swapForm(init: number) {
    if (init === 1) 
      setMode(2);
    else if ([2, 3, 7].includes(init))
      setMode(1);
    else setMode(0);
  }
  function formvars(init: number) {
    if (loading) 
       return {header: '', fragA: "", fragB: ""}
    if (init === 1) {
      return {header: 'Sign In', fragA: "Don't have an account?", fragB: 'Sign up.'}
    } else if (init === 2) {
      return {header: 'Sign Up', fragA: 'Already a member?', fragB: 'Log in.'}
    } else if (init === 3) {
      return {header: 'Forgot your password?', fragA: '...or', fragB:'cancel'}
    } else if (init === 4 || init === 5) {
      return {header: 'Email sent.', fragA: '', fragB: 'Got it.'}
    } else if (init === 6) {
      return {header: 'Reset your password', fragA: '', fragB: ''}
    } else if (init === 7) {
      return {header: "Success.", fragA: '', fragB: 'Log me in!'}
    } else if (init === 8 || init === 9) {
      return {header: "Change your password", fragA: '...or', fragB: 'cancel'}
    } else if (init === 10) {
      return {header: "Password change successful", fragA: '', fragB: 'Great.'}
    } else if (init === 11) {
      return {header: "Moderate "+document.querySelector('.nav-link.active').innerHTML + " Post", fragA: "", fragB: "cancel"}
    } else if (init === 12) {
      return {header: document.querySelector('.nav-link.active').innerHTML + ' post moderated.', fragA: '', fragB: 'Great.'}
    } else { 
      return {header: 'Bye then', fragA: '', fragB: ''}
    }
  }

  const { header, fragA, fragB } = formvars(mode);
  const logIn = mode === 1;
  const signUp = mode === 2;
  const passwordResetConfirm = mode === 3;
  const passwordResetEmailSent = mode === 4;
  const verificationEmailSent = mode === 5;
  const passwordResetCodeVerified = mode === 6;
  const passwordResetComplete = mode === 7;
  const passwordChangeConfirm = mode === 8;
  const passwordChangeVerified = mode === 9;
  const passwordChangeDone = mode === 10;
  const moderate = mode === 11;
  const moderated = mode === 12;
  const color = [3, 8, 9, 11].includes(mode) ? 'var(--secondary)' : 'var(--primary)';
  return (
    
    <Modal isOpen={!!mode}>
     <ModalHeader toggle={() => setMode(0)}>{header}</ModalHeader>
     <ModalBody>
      <Suspense fallback={<Loading />}>
       {loading && <Loading />}
       {!loading &&
        <>
         {logIn && <LoginForm />}
         {signUp && <SignupForm />}
         {passwordResetConfirm && <PasswordResetConfirmForm />} 
         {passwordResetEmailSent && <PasswordResetEmailSent />}
         {verificationEmailSent && <UnverifiedUser />}
         {passwordResetCodeVerified && <PasswordResetForm />}
         {passwordResetComplete && <PasswordResetComplete />}
         {passwordChangeConfirm && <PasswordChangeConfirmForm />}
         {passwordChangeVerified && <PasswordChangeForm />}
         {passwordChangeDone && <PasswordChangeDone />}
         {moderate && <ModerationForm />}
         {moderated && <PostModerated />}
        </>
        }
       </Suspense>
      </ModalBody>
      <ModalFooter>
        <span>
           {fragA}
            <button style={{ color: color,
                             backgroundColor: 'transparent',
                             borderStyle: 'none' 
                          }} 
                          onClick={() => swapForm(mode)}
            >
            {fragB}
          </button>
        </span>
      </ModalFooter>
    </Modal>
  )
}

export default CustomModal;
