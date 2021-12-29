import useAuth from '../Auth/useAuth';

export default function Report() {
  const { authData, 
          modeHandler: { setMode } } = useAuth();
  const superUser = !!authData?.verificationStatus;
  return (
   <>
    {superUser && <i className="fa fa-flag small text-muted mt-n4" onClick={() => setMode(11)}></i>}
   </>
  )
}
