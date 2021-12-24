import { useForm } from "react-hook-form";
import Form from "react-bootstrap/Form";
import Button from "react-bootstrap/Button";
import React, { useState } from 'react';
import useAuth from './useAuth';

async function changePassword(data: any) {
  const { authData }  = useAuth();
  const url = "https://againstporn.org/api/accounts/password/change/";
  const api_url =
    process.env.NODE_ENV === "production"
      ? url
      : url.replace("https://againstporn.org", "http://34.225.127.212:8000");
  return fetch(api_url,{
    method: 'POST',
    headers: {
     'Content-Type': 'application/json',
     'Authorization': 'Token ' + authData?.token
    },
    body: JSON.stringify(data)
  })
   .then((data) => data.json())
   .catch((err) => console.log(err));
}

const PasswordChangeConfirmForm = () => {
  const { confirmPasswordChange,
          setLoading,
  } = useAuth();
  const { register, handleSubmit } = useForm();
  const [failure, setFailure] = useState('');
  const onSubmit = async (data: any, e: any) => {
    e.preventDefault();
    const response = await changePassword(data);
    if (typeof response?.detail !== 'undefined') {
      setFailure(response.detail);
    }
    else {
      setLoading(true);
      await confirmPasswordChange(); 
    }
    return {failure: failure};
  } 
  return (
     <>
      <div className="col-8 offset-2 text-center mb-3">
	<h6>You are about to change your password.</h6>
	<p>Please enter your current password to verify your identity.</p>
      </div>
      <Form onSubmit={handleSubmit(onSubmit)}>
       <Form.Group className="mb-3 mt-3 offset-3 w-50 d-flex flex-wrap" controlId="formBasicEmail">
         <Form.Label className="visually-hidden">Email address</Form.Label>
          <Form.Control
            {...register("verify")}
            type="email"
            placeholder="Password"
            autoComplete="password"
            className="mb-3 mt-3" 
          />
          {failure && 
             <>
              <Form.Control.Feedback type="invalid" className="d-flex mt-n3 mb-3 justify-content-center">
               {failure}
              </Form.Control.Feedback>
             </>
           }
         <Button variant="info" className="flex-grow-1 mt-2" type="submit">
           Submit
         </Button>
       </Form.Group>
      </Form>
     </>
  );
};

export default PasswordChangeConfirmForm;
