import useAuth from '../Auth/useAuth';

function ModForm() {
  const { authData, 
          modeHandler: { setMode }
        } = useAuth();
  const superUser = !!authData?.verificationStatus;
  const admin_link = authData?.verificationStatus?.admin_link;
  const button_id = document.location.pathname.split('/')[2];
  const reported = authData?.reports || '';
  const report_made = reported.match(button_id) ? 'success' : '';
  return (
  <>
   {superUser &&
    <div className="d-flex fixed-top flex-column text-muted">
      <a href={admin_link}>
       <i className="fa fa-external-link-square p-2 small">
       </i>
      </a>
      <i className={"fa fa-shield-check pl-2 small " + report_made} 
         id={button_id} 
         onClick={() => setMode(11)}
      >
      </i> 
    </div>
    }
  </>
 )
}

export default ModForm;
