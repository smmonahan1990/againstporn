import { useForm } from "react-hook-form";
import Form from "react-bootstrap/Form";
import Button from "react-bootstrap/Button";
import React, { useState } from 'react';
import useAuth from './useAuth';

async function passwordChangeVerified(data: any) {
  const url = "https://againstporn.org/api/accounts/password/change/";
  const api_url =
    process.env.NODE_ENV === "production"
      ? url
      : url.replace("https://againstporn.org", "http://34.225.127.212:8000");
  return fetch(api_url,{
    method: 'POST',
    headers: {
     'Content-Type': 'application/json',
     'Authorization': 'Token ' + data?.token
    },
    body: JSON.stringify(data)
  })
   .then((data) => data.json())
   .catch((err) => console.log(err));
}

const PasswordChangeForm = () => {
  const { changePassword,
          authData,
          setLoading } = useAuth();
  const { register, handleSubmit } = useForm();
  const [error, setError] = useState('');
  const [empty, setEmpty] = useState(0);
  const [failure, setFailure] = useState('');
  const onSubmit = async (data: any, e: any) => {
    e.preventDefault();
    setError('');
    setFailure('');
    setEmpty(0);
    if (!data.password || !data.password2) {
        setError('This field cannot be blank.')
        setEmpty(!data.password ? 1 : 2)
    }
    else if (data.password !== data.password2) {
      setError("Passwords don't match.")
    } 
    else {
      const response = await passwordChangeVerified(data);
//      const response = await passwordChangeVerified({password: data?.password, token: authData?.token});
      if (typeof response?.detail !== 'undefined') {
        setFailure(response.detail);
      }
      else if (!!response?.success) {
        setLoading(true);
        await changePassword();
      }
      else {
        setFailure('There was an error.');
      }
    }
    return {empty: empty, error: error, failure: failure};
  } 
  return (
     <>
      <div className="text-center mb-3">Set your new password below.</div>
      <Form onSubmit={handleSubmit(onSubmit)}>
       <Form.Group className="mb-3 mt-3 offset-3 w-50 d-flex flex-wrap" controlId="formBasicPassword">
         <Form.Label className="visually-hidden">Password</Form.Label>
          <Form.Control
            {...register("password")}
            type="password"
            placeholder="Password"
            autoComplete="new-password"
            className="mb-3 mt-3" 
          />
          {failure && 
             <>
              <Form.Control.Feedback type="invalid" className="mt-n3 mb-3 d-flex justify-content-center">
               {failure}
              </Form.Control.Feedback>
             </>
           }
          {(empty === 1) && 
             <>
              <Form.Control.Feedback type="invalid" className="d-flex mt-n3 mb-3 justify-content-center">
               {error}
              </Form.Control.Feedback>
             </>
           }
         <Form.Label className="visually-hidden">Confirm Password</Form.Label>
          <Form.Control
            {...register("password2")}
            type="password"
            placeholder="Confirm Password"
            autoComplete="new-password"
            className="mb-3 mt-3" 
          />
          {((error && !empty) || empty === 2) &&
             <>
              <Form.Control.Feedback type="invalid" className="d-flex mt-n3 mb-3 justify-content-center">
               {error}
              </Form.Control.Feedback>
             </>
           }
          <input type="hidden" {...register("token")} value={authData?.token} />
         <Button variant="success" className="flex-grow-1 mt-2" type="submit">
           Change my password!
         </Button>
       </Form.Group>
      </Form>
     </>
  );
};

export default PasswordChangeForm;
