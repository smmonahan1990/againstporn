import { useForm } from "react-hook-form";
import Form from "react-bootstrap/Form";
import Button from "react-bootstrap/Button";
import React, { useState } from 'react';
import useAuth from './useAuth';

async function resetPassword(data: any) {
  const url = "https://againstporn.org/api/accounts/password/reset/";
  const api_url =
    process.env.NODE_ENV === "production"
      ? url
      : url.replace("https://againstporn.org", "http://34.225.127.212:8000");
  return fetch(api_url,{
    method: 'POST',
    headers: {
     'Content-Type': 'application/json'
    },
    body: JSON.stringify(data)
  })
   .then((data) => data.json())
   .catch((err) => console.log(err));
}

const PasswordResetConfirmForm = () => {
  const { authData,
          confirmPasswordReset,
          setLoading
  } = useAuth();
  const { register, handleSubmit } = useForm();
  const [failure, setFailure] = useState('');
  const onSubmit = async (data: any, e: any) => {
    e.preventDefault();
    const response = await resetPassword(data);
    if (typeof response?.detail !== 'undefined') {
      setFailure(response.detail);
    }
    else if (typeof response?.email === 'object') {
      setFailure(response.email[0]);
    }
    else {
      setLoading(true);
      await confirmPasswordReset({ ...authData, email: data.email, token: '', verificationStatus: 'pendingPasswordReset'}) 
    }
    return {failure: failure};
  } 
  return (
     <>
      <div className="col-8 offset-2 text-center mb-3">Enter your email address below, and we'll email instructions for setting a new one.</div>
      <Form onSubmit={handleSubmit(onSubmit)}>
       <Form.Group className="mb-3 mt-3 offset-3 w-50 d-flex flex-wrap" controlId="formBasicEmail">
         <Form.Label className="visually-hidden">Email address</Form.Label>
          <Form.Control
            {...register("email")}
            type="email"
            placeholder="Email address"
            autoComplete="email"
            className="mb-3 mt-3" 
          />
          {failure && 
             <>
              <Form.Control.Feedback type="invalid" className="d-flex mt-n3 mb-3 justify-content-center">
               {failure}
              </Form.Control.Feedback>
             </>
           }
         <Button variant="success" className="flex-grow-1 mt-2" type="submit">
           Send me instructions!
         </Button>
       </Form.Group>
      </Form>
     </>
  );
};

export default PasswordResetConfirmForm;
