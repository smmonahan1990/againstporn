import Form from 'react-bootstrap/Form';
import Button from 'react-bootstrap/Button';
import React, { useState } from 'react'; 
import useAuth from '../Auth/useAuth'; 
import { useForm, FormProvider } from 'react-hook-form'; 
import AsyncLocalStorage from '@react-native-async-storage/async-storage';

async function reportArchive(data: any) {
  
  var url = 'https://againstporn.org/api'+document.location.pathname;
  url = process.env.NODE_ENV === 'production' 
        ? url
        : 'http://34.225.127.212:8000/api'+document.location.pathname;
  const auth = await AsyncLocalStorage.getItem('@AuthData');
  const token = JSON.parse(auth).token; 
  const headers = new Headers();
  headers.set('Authorization','Token ' + token);
  headers.set('Content-Type','application/json');
  return fetch(url, {
    method: 'POST', 
    headers: headers,
    body: JSON.stringify(data)
  })
  .then((data) => data.json())
  .catch((err) => console.log(err));
}
  
function ModerationForm() { 
  const { setLoading, 
          modeHandler } = useAuth(); 
  const [error, setError] = useState(''); 
  const [show, setShow] = useState(false); 
  const methods = useForm(); 
  const Flair = React.lazy(() => import('./Flair'));
  const onSubmit = async (data, event) => {
    event.preventDefault(); 
    setLoading(true); 
    if (data.action === "0") 
        setError('input required.') 
    else {
      const _data = data?.flair || data.action;
      const response = await reportArchive({action :_data}); 
      console.log(response);
      if (response.hasOwnProperty('success')) {
          modeHandler.setMode(12); 
          const button = document.getElementById(document.location.pathname.split('/')[2]); 
          const reports = await AsyncLocalStorage.getItem('@Reports') || ''; 
          const combined = reports.match(button) ? reports: reports.concat(','+button.id); 
          button.setAttribute('style','color:var(--success)!important'); 
          await AsyncLocalStorage.setItem('@Reports',combined);
      }
      else if (response.hasOwnProperty('detail')) { 
        setError(response.detail);
      }
     }
   setLoading(false); 
   return {error: error};
 };

  return (
  <FormProvider {...methods}>
   <Form className="offset-2 col-8" onSubmit={methods.handleSubmit(onSubmit)}>
    <Form.Group className="d-flex flex-column" 
     controlId="formGridModerate">
      <Form.Label visuallyHidden className="mr-2 visually-hidden">Moderate</Form.Label>
      <Form.Select {...methods.register('action')}
        onChange={(e) => setShow(e.target.value === '3')}
        className="mt-3 mb-3 p-1 form-control select" 
        defaultValue="Choose moderation action..."
      > 
        <option value={0}>Choose moderation action...</option> 
        <option value={1}>toggle nsfw</option> 
        <option value={2}>remove</option> 
        <option value={3}>set flair</option>
      </Form.Select>
      {error && <Form.Control.Feedback className="d-flex justify-content-center mb-3 mt-n3 invalid-feedback">{error}</Form.Control.Feedback>}
      {!!show && 
       <React.Suspense fallback={<div className="d-flex align-items-center flex-column">Loading...</div>}>
        <Flair />
       </React.Suspense>
       }
     <Button className="mb-3" variant="danger" type="submit">Submit form</Button> 
    </Form.Group> 
   </Form> 
  </FormProvider>
  );
}

export default ModerationForm;
